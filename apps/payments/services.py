import random
import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_API_KEY


def create_url_payment(data: dict) -> str:
    """Generate a payment url using STRIPE PAYMENT SYSTEM and stripe framework"""
    product = stripe.Product.create(
        name=data['name'],
        description=data['description'],
    )

    price = stripe.Price.create(
        unit_amount=data['amount'],
        currency='eur',
        product=product.id
    )

    payment_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=f'http://127.0.0.1:8000/api/payment/success/?verify_payment_number={data["verify_payment_number"]}',
        cancel_url=f'http://127.0.0.1:8000/api/payment/cancel/?verify_payment_number={data["verify_payment_number"]}',
    )

    return payment_session.url


def generate_random_number() -> str:
    return ''.join(str(random.randint(1, 9)) for _ in range(8))
