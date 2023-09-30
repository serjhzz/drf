from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.academy.models import Course, Subscription


@shared_task()
def course_update_notification():
    four_hours_ago = timezone.now() - timedelta(hours=4)
    five_hours_ago = timezone.now() - timedelta(hours=5)

    courses = Course.objects.filter(last_update__gte=five_hours_ago, last_update__lt=four_hours_ago)
    if courses.exists():
        for course in courses:
            subscriptions = Subscription.objects.filter(course=course.id)
            if subscriptions:
                for subscription in subscriptions:
                    user = subscription.user
                    send_mail(
                        subject=f"Course {course.name} information.",
                        message=f"""
                                You are subscribed to course {course.name}, which has been updated.
                                Please visit the site to learn more.
                                """,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email]
                    )

