from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from orders.models import Order
from shipping.models import Shipping
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_shipping_status_email(email, tracking_number, status_display):
    subject = f"Обновление доставки #{status_display}"
    message = f"Ваша доставка с номером отслеживания {tracking_number} теперь имеет статус: {status_display}."
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Письмо успешно отправлено пользователю {email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")


@shared_task
def update_shipping_statuses():
    now = timezone.now()
    shipments = Shipping.objects.all()

    for shipment in shipments:
        try:
            order = Order.objects.get(shipping=shipment)
            user_email = order.user.email
        except Order.DoesNotExist:
            continue

        time_create = (now - shipment.created_at).total_seconds()

        old_status = shipment.status

        if shipment.status == Shipping.DeliveryStatus.PENDING:
            if time_create > 5 * 60:
                shipment.status = Shipping.DeliveryStatus.IN_TRANSIT
                shipment.save()
                print(f"Доставка #{shipment.id} -> В ПУТИ")

        elif shipment.status == Shipping.DeliveryStatus.IN_TRANSIT:
            if time_create > 10 * 60:
                shipment.status = Shipping.DeliveryStatus.DELIVERED
                shipment.save()
                print(f"Доставка #{shipment.id}  ДОСТАВЛЕНА")

        if shipment.status != old_status:
            status_display = shipment.get_status_display()
            send_shipping_status_email.delay(user_email, shipment.tracking_number, status_display)