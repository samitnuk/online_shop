from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext

from .forms import CategoryForm, ManufacturerForm, ProductForm, ImageFormSet
from .models import Category, Manufacturer, Product, ProductImage
from . import utils


@staff_member_required
def staff_area(request):
    return render(request, 'shop/staff_area/_main.html', {})


@staff_member_required
def categories(request, category_slug=None):
    if category_slug is None:
        active_category = None
        products = Product.objects.filter(available=True)
    else:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = active_category.products
    context = {
        'categories': Category.objects.all(),
        'active_category': active_category,
        'products': products
    }
    return render(request, 'shop/staff_area/categories.html', context)


@staff_member_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('shop:categories')
    context = {'form': form}
    return render(request, 'shop/staff_area/category_form.html', context)


@staff_member_required
def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(
        request.POST or None, request.FILES or None, instance=category)
    if form.is_valid():
        form.save()
        new_slug = utils.slugify_(form.cleaned_data['name'])
        return redirect('shop:category', category_slug=new_slug)
    context = {'form': form}
    return render(request, 'shop/staff_area/category_form.html', context)


@staff_member_required
def manufacturers(request):
    context = {'manufacturers': Manufacturer.objects.all()}
    return render(request, 'shop/staff_area/manufacturers.html', context)


@staff_member_required
def manufacturer_create(request):
    form = ManufacturerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('shop:manufacturers')
    context = {'form': form}
    return render(request, 'shop/staff_area/manufacturer_form.html', context)


@staff_member_required
def manufacturer_update(request, slug):
    manufacturer = get_object_or_404(Manufacturer, slug=slug)
    form = ManufacturerForm(
        request.POST or None, request.FILES or None, instance=manufacturer)
    if form.is_valid():
        form.save()
        return redirect('shop:manufacturers')
    context = {'form': form}
    return render(request, 'shop/staff_area/manufacturer_form.html', context)


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
def product_update(request, slug):

    product = get_object_or_404(Product, slug=slug)

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
