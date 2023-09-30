from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.users.models import NULLABLE, User


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(**NULLABLE, verbose_name=_('description'))
    preview = models.ImageField(**NULLABLE, upload_to='courses/previews', verbose_name=_('preview'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_('last updated'))

    creator = models.ForeignKey(
        User, related_name='courses', on_delete=models.DO_NOTHING, verbose_name=_('course creator')
    )

    def __str__(self):
        return self.name

    def is_user_subscribed(self, user):
        return Subscription.objects.filter(course=self, user=user).exists()

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    description = models.TextField(**NULLABLE, verbose_name=_('description'))
    video_link = models.CharField(**NULLABLE, max_length=255, verbose_name=_('video link'))
    preview = models.ImageField(**NULLABLE, upload_to='lessons/previews', verbose_name=_('preview'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_('last upload at'))

    course = models.ForeignKey(
        Course, related_name='lessons', on_delete=models.DO_NOTHING, verbose_name=_('course'))
    creator = models.ForeignKey(
        User, related_name='lessons', on_delete=models.DO_NOTHING, verbose_name=_('lesson creator')
    )

    def save(self, *args, **kwargs):
        self.course.last_update = timezone.now()
        self.course.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='subscription', verbose_name=_('user'))
    course = models.ForeignKey(
        to=Course, on_delete=models.CASCADE, related_name='subscription', verbose_name=_('course'))

    def __str__(self):
        return f'User : {self.user} \n Course: {self.course}'

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
