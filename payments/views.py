import logging
import stripe
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import permissions
from orders.models import Order
from payments.models import Payment
from payments.serializers import CheckoutSessionSerializer
from .tasks import send_payment_success_email

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=CheckoutSessionSerializer,
        responses={200: dict, 400: dict, 404: dict},
        summary="Создать платёжную сессию",
    )
    def post(self, request, *args, **kwargs):
        DOMAIN = "https://c23ba772ff67.ngrok-free.app"

        serializer = CheckoutSessionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        provider = serializer.validated_data['provider']

        order = Order.objects.get(id=order_id, user=request.user)

        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=order.total_price,
            provider=provider,
            status=Payment.PaymentStatus.PENDING,
        )

        if provider == Payment.PaymentProvider.STRIPE:
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'rub',
                            'unit_amount': int(order.total_price * 100),
                            'product_data': {'name': f"Order #{order.id}"},
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    metadata={
                        'user_id': str(request.user.id),
                        'order_id': str(order.id)
                    },
                    success_url=DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=DOMAIN + '/cancel/',
                )

                return Response({'checkout_url': checkout_session.url})
            except Exception as e:
                return Response({'error': str(e)}, status=400)

        return Response({
            'message': f'Пожалуйста, оплатите через {provider}. Мы подтвердим вручную.',
            'payment_id': payment.id
        }, status=200)



@csrf_exempt
@api_view(['POST'])
@extend_schema(
    request=None,
    responses={200: dict},
)
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        logger.warning(f"Неверный формат данных от Stripe: {e}")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    event_type = event.get('type')

    if event_type == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        user_id = metadata.get('user_id')
        order_id = metadata.get('order_id')

        if not user_id or not order_id:
            logger.error("Отсутствует metadata (user_id или order_id)")
            return JsonResponse({'error': 'Отсутствуют данные о пользователе или заказе'}, status=400)

        try:
            payment = Payment.objects.get(order_id=int(order_id), user_id=int(user_id))
            payment.status = Payment.PaymentStatus.PAID
            payment.provider_payment_id = session.get("payment_intent") or session.get("id")
            payment.save()

            send_payment_success_email.delay(
                payment.user.email,
                payment.order.id,
                payment.order.total_price,
            )

            logger.info(f"Платёж #{payment.id} успешно подтверждён и обновлён")

        except Payment.DoesNotExist:
            logger.error(f"Платёж не найден (order_id={order_id}, user_id={user_id})")
            return JsonResponse({'error': 'Payment not found'}, status=404)

    return JsonResponse({'status': 'ok'})
