from io import BytesIO

import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from ..orders.models import Order


def payment_notification(sender, **_):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipn_obj.invoice)
        order.paid = True
        order.save()

        # Send email
        subject = 'Online Shop - order: {}'.format(order.id)
        message = 'PDF file with your order info attached to this email'
        email = EmailMessage(
            subject, message, settings.ADMIN_MAIL, [order.user.email])

        # Create PDF
        html = render_to_string('orders/pdf.html', {'order': order})
        out = BytesIO()
        weasyprint.HTML(string=html).write_pdf(
            out,
            stylesheets=[weasyprint.CSS(
                settings.STATIC_ROOT + 'css/bootstrap.min.css')])

        # Attach PDF
        email.attach(
            'order_{}.pdf'.format(order.id),
            out.getvalue(),
            'application/pdf',
        )
        email.send()


valid_ipn_received.connect(payment_notification)
