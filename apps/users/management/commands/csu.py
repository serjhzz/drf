from django.core.management import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        superuser = User.objects.create(
            email='superuser@gmail.com',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        superuser.set_password('superuser')
        superuser.save()

        moderator = User.objects.create(
            email='moderator@gmail.com',
            is_active=True,
            is_staff=True,
            is_superuser=False
        )

        moderator.set_password('moderator')
        moderator.save()

        user = User.objects.create(
            email='user@gmail.com',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )

        user.set_password('user')
        user.save()