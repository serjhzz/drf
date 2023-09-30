from django.utils import timezone

from apps.users.models import User


def update_last_login(request):
    user = User.objects.filter(email=request.data.get('email')).first()
    if user:
        user.last_login = timezone.now()
        user.save()
