from django.shortcuts import get_object_or_404

from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from ..orders.models import Order


def payment_notification(sender, **_):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

valid_ipn_received.connect(payment_notification)
