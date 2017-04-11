from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from celery.task import task

from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = _('Order number {}').format(order_id)
    message = _("Hello! \
              You successfully made order. \
              Your order number {}").format(order_id)
    mail_send = send_mail(
        subject, message, settings.ADMIN_MAIL, [order.user.email]
    )
    return mail_send
