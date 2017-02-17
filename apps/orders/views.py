from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import OrderItem, Order
from .forms import OrderCreateForm
from ..cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm(request.POST or None)
    if form.is_valid():
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})

    context = {'cart': cart, 'form': form}
    return render(request, 'orders/create.html', context)


# def order_confirmed(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     for order_item in order.items.all():
#         product = order_item.product
#         product.stock -= order_item.quantity
#         product.save()
#     return redirect()


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/detail.html', {'order': order})
