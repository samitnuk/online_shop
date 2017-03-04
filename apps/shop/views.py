from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext

from .models import Category, Product, ProductImage
from .forms import CategoryForm, ProductForm, ImageFormSet
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


@staff_member_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product,
        'cart_product_form': CartAddProductForm(product_id=product.id),
        'images': [img.image for img in product.images.all()]
    }
    return render(request, 'shop/detail.html', context)


def category_create(request):

    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('shop:product_list')

    context = {'form': form}
    return render(request, 'shop/staff_area/category_form.html', context)


@staff_member_required
def product_create(request):

    product_form = ProductForm(request.POST or None, request.FILES or None)
    formset = ImageFormSet(request.POST or None, request.FILES or None,
                           queryset=ProductImage.objects.none())

    if product_form.is_valid() and formset.is_valid():
        product = product_form.save()
        for form in formset.cleaned_data:
            if form.get('image', None) is not None:
                ProductImage.objects.create(product=product,
                                            image=form['image'])
        return redirect('shop:product_list')

    context = {
        'product_form': product_form,
        'formset': formset,
        'context_instance': RequestContext(request),
    }
    return render(request, 'shop/staff_area/product_form.html', context)


@staff_member_required
def product_update(request, pk, slug):

    product = get_object_or_404(Product, pk=pk, slug=slug)

    product_form = ProductForm(
        request.POST or None, request.FILES or None,
        instance=product,
    )
    formset = ImageFormSet(
        request.POST or None, request.FILES or None,
        queryset=ProductImage.objects.filter(product=product))

    if product_form.is_valid() and formset.is_valid():
        product_form.save()
        for form in formset.cleaned_data:
            if form.get('image', None) is not None:
                ProductImage.objects.get_or_create(product=product,
                                                   image=form['image'])
        return redirect('shop:product_list')

    context = {
        'product_form': product_form,
        'formset': formset,
        'context_instance': RequestContext(request),
    }
    return render(request, 'shop/staff_area/product_form.html', context)
