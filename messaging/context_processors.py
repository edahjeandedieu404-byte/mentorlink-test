from .models import Message


def non_lus_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__participants=request.user,
            lu=False
        ).exclude(auteur=request.user).count()
        return {'non_lus_total': count}
    return {'non_lus_total': 0}