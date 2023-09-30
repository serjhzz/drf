from rest_framework import serializers

from apps.academy.models import Course, Lesson, Subscription
from apps.academy.validators import OnlyYouTubeUrlAllow


class LessonSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = (
            'id', 'name', 'preview', 'description', 'course', 'creator'
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons_quantity = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(read_only=True, many=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'name', 'preview', 'description', 'price', 'lessons', 'lessons_quantity', 'creator', 'is_subscribed'
        )
        extra_kwargs = {"is_subscribed": {"read_only": True}}
        validators = (OnlyYouTubeUrlAllow(field='description'),)

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        return course.is_user_subscribed(user=user)

    @staticmethod
    def get_lessons_quantity(course):
        return course.lessons.all().count()


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('user', 'course')
