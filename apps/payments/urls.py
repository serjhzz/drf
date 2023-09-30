from django.urls import path

from apps.payments.apps import PaymentsConfig
from apps.payments.views import (
    PaymentListAPIView,
    PaymentCreateAPIView,
    PaymentSuccessAPIView,
    PaymentCancelAPIView,
)

app_name = PaymentsConfig.name

urlpatterns = [
    path('api/payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('api/payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('api/payment/success/', PaymentSuccessAPIView.as_view(), name='success'),
    path('api/payment/cancel/', PaymentCancelAPIView.as_view(), name='cancel'),
]
