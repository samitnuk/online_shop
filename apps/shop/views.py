from django.shortcuts import get_object_or_404, render

from ..cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    if category_slug is None:
        category = None
        products = Product.objects.filter(available=True)
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products

    context = {
        'category': category,
        'categories': Category.objects.all(),
        'products': products
    }

    return render(request, 'shop/main.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
        'cart_product_form': CartAddProductForm(product_id=product.id),
        'images': [img.image for img in product.images.all()]
    }
    return render(request, 'shop/product_detail.html', context)


def product_list_by_manufacturer(request):
    pass
