from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST, product_id=product_id)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update'])
    return redirect('cart:detail')


def cart_remove_product(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        product = item['product']
        item['update_quantity_form'] = CartAddProductForm(
                                        product_id=product.id,
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')
