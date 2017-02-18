from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.template.defaultfilters import slugify

from .models import Category, Product, ProductImage
from .forms import ProductForm, ImageFormSet
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
        'images': [img.image for img in product.images.all()]
    }
    return render(request, 'shop/detail.html', context)


@staff_member_required
def product_create(request):

    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = ImageFormSet(
            request.POST, request.FILES, queryset=ProductImage.objects.none()
        )
        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            product.category = product_form.cleaned_data['category']
            product.slug = slugify(product.name)

            product.save()
            print(product.slug)
            print(product)
            for form in formset.cleaned_data:
                if form.get('image', None) is not None:
                    ProductImage.objects.create(product=product,
                                                image=form['image'])
            return redirect('shop:product_list')

    context = {
        'product_form': ProductForm(),
        'formset': ImageFormSet(queryset=ProductImage.objects.none()),
        'context_instance': RequestContext(request),
    }
    return render(request, 'shop/product_create.html', context)
