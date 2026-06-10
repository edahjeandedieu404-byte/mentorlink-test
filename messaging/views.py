from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


def get_non_lus_count(user):
    return Message.objects.filter(
        conversation__participants=user,
        lu=False
    ).exclude(auteur=user).count()


@login_required
def liste_conversations(request):
    conversations = request.user.conversations.all().order_by('-date_creation')

    convs_data = []
    for conv in conversations:
        autre = conv.get_other_participant(request.user)
        dernier_message = conv.messages.last()
        non_lus = conv.messages.filter(lu=False).exclude(auteur=request.user).count()
        convs_data.append({
            'conv': conv,
            'autre': autre,
            'dernier_message': dernier_message,
            'non_lus': non_lus,
        })

    return render(request, 'messaging/liste_conversations.html', {
        'convs_data': convs_data,
        'non_lus_total': get_non_lus_count(request.user),
    })


@login_required
def conversation(request, conversation_id):
    conv = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in conv.participants.all():
        return redirect('liste_conversations')

    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu:
            Message.objects.create(
                conversation=conv,
                auteur=request.user,
                contenu=contenu
            )
            conv.messages.filter(lu=False).exclude(
                auteur=request.user
            ).update(lu=True)
            return redirect('conversation', conversation_id=conv.id)

    # Marquer comme lus automatiquement
    conv.messages.filter(lu=False).exclude(
        auteur=request.user
    ).update(lu=True)

    messages_conv = conv.messages.all()
    autre = conv.get_other_participant(request.user)

    convs_data = []
    for c in request.user.conversations.all():
        non_lus = c.messages.filter(lu=False).exclude(auteur=request.user).count()
        convs_data.append({
            'conv': c,
            'autre': c.get_other_participant(request.user),
            'dernier_message': c.messages.last(),
            'non_lus': non_lus,
        })
    return render(request, 'messaging/conversation.html', {
        'conversation': conv,
        'msgs': messages_conv,
        'autre': autre,
        'convs_data': convs_data,
        'non_lus_total': get_non_lus_count(request.user),
    })


@login_required
def nouvelle_conversation(request, user_id):
    autre_user = get_object_or_404(User, id=user_id)

    conv_existante = request.user.conversations.filter(
        participants=autre_user
    ).first()

    if conv_existante:
        return redirect('conversation', conversation_id=conv_existante.id)

    conv = Conversation.objects.create()
    conv.participants.add(request.user, autre_user)
    return redirect('conversation', conversation_id=conv.id)

@login_required
def supprimer_conversation(request, conversation_id):
    conv = get_object_or_404(Conversation, id=conversation_id)
    if request.user in conv.participants.all():
        conv.delete()
    return redirect('liste_conversations')