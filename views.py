from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


@login_required
def liste_conversations(request):
    conversations = request.user.conversations.all().order_by('-date_creation')
    return render(request, 'messaging/liste_conversations.html', {
        'conversations': conversations
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

    messages = conv.messages.all()
    autre = conv.get_other_participant(request.user)

    return render(request, 'messaging/conversation.html', {
        'conversation': conv,
        'messages': messages,
        'autre': autre
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
def messages_non_lus(request):
    count = Message.objects.filter(
        conversation__participants=request.user,
        lu=False
    ).exclude(auteur=request.user).count()
    return render(request, 'messaging/liste_conversations.html', {
        'conversations': request.user.conversations.all(),
        'non_lus': count
    })