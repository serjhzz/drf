from rest_framework import serializers
from apps.payments.models import Payment
from apps.payments.services import create_url_payment, generate_random_number


class PaymentListSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'creator', 'creator_name', 'course_payment', 'lesson_payment', 'amount', 'datetime', 'status'
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    verify_payment_number = serializers.HiddenField(default=generate_random_number)
    status = serializers.CharField(read_only=True)
    datetime = serializers.DateTimeField(read_only=True)
    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'amount', 'course_payment', 'lesson_payment', 'status', 'datetime', 'creator', 'payment_url',
            'verify_payment_number',
        ]

    def validate(self, data):
        course_payment = data.get("course_payment")
        lesson_payment = data.get("lesson_payment")

        if course_payment is None and lesson_payment is None:
            raise serializers.ValidationError(
                "Either 'course_payment' or 'lesson_payment' must be provided.")

        if course_payment is not None and lesson_payment is not None:
            raise serializers.ValidationError(
                "Provide either 'course_payment' or 'lesson_payment', not both.")

        return data

    @staticmethod
    def get_payment_url(obj):
        """
        Creating a payment data dict, so we can generate a payment url
        """
        payment_data = {
            "amount": obj.amount,
            "verify_payment_number": obj.verify_payment_number
        }

        course_payment = obj.course_payment
        if course_payment:
            payment_data['name'] = course_payment.name
            payment_data['description'] = course_payment.description

        lesson_payment = obj.lesson_payment
        if lesson_payment:
            payment_data['name'] = lesson_payment.name
            payment_data['description'] = lesson_payment.description

        payment_url = create_url_payment(payment_data)

        return payment_url
