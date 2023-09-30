from celery import shared_task
from django.utils import timezone

from apps.users.models import User

@shared_task
def check_user_activity():
    one_mount_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__gte=one_mount_ago)

    for user in inactive_users:
        user.is_active = False
        user.save()
