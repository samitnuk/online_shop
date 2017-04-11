from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

from ..orders.models import Order


@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.ADMIN_MAIL,
        'amount': '{}'.format(
            order.get_total_cost().quantize(Decimal('.01'))),
        'item_name': _('Order {}').format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal_ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(
            host, reverse('payment:canceled')),
    }

    context = {
        'order': order,
        'form': PayPalPaymentsForm(initial=paypal_dict)
    }
    return render(request, 'payment/process.html', context)


@csrf_exempt
@login_required
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
