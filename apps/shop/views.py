from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from ..cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': Category.objects.all(),
        'products': products
    }

    return render(request, 'shop/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product,
        'cart_product_form': CartAddProductForm(product_id=product.id),
        'images': product.images.all()
    }
    return render(request, 'shop/detail.html', context)
