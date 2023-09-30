from rest_framework.filters import OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.payments.models import Payment
from apps.payments.serializers import PaymentCreateSerializer, PaymentListSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['course_payment', 'lesson_payment']
    ordering_fields = ['datetime_payment']


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [AllowAny]


class PaymentSuccessAPIView(APIView):
    @staticmethod
    def get(request):
        verify_payment_number = request.query_params.get('verify_payment_number')
        payment = get_object_or_404(Payment, verify_payment_number=verify_payment_number)

        payment.status = Payment.Status.SUCCESS
        payment.save()

        response_data = {'message': 'Payment successful'}
        return Response(response_data, status=status.HTTP_200_OK)


class PaymentCancelAPIView(APIView):
    @staticmethod
    def get(request):
        verify_payment_number = request.query_params.get('verify_payment_number')
        payment = get_object_or_404(Payment, verify_payment_number=verify_payment_number)

        payment.status = Payment.Status.CANCEL
        payment.save()

        response_data = {'message': 'Payment canceled'}

        return Response(response_data, status=status.HTTP_200_OK)
