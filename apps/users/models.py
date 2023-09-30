from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_('email'))

    telephone = models.CharField(**NULLABLE, unique=True, max_length=50, verbose_name=_('telephone'))
    town = models.CharField(**NULLABLE, max_length=50, verbose_name=_('town'))
    avatar = models.ImageField(**NULLABLE, upload_to='users/avatars', verbose_name=_('avatar'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
