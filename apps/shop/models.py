from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from . import utils


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True,
                            verbose_name=_('Name'))
    slug = AutoSlugField(
        always_update=True, populate_from='name', unique=True,
        slugify=utils.slugify_, db_index=True)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    image = models.ImageField(upload_to=utils.category_img_path,
                              blank=True, verbose_name=_('Image'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        key = 'category_{}_abs_url'.format(self.id)
        abs_url = cache.get(key)
        if abs_url:
            return abs_url
        abs_url = reverse('shop:product_list_by_category',
                          kwargs={'category_slug': self.slug})
        cache.set(key, abs_url)
        return abs_url

    def products(self):
        key = 'category_{}_products'.format(self.id)
        cached_products = cache.get(key)
        if cached_products:
            return cached_products
        products = self.category_products.all()
        cache.set(key, products)
        return products

    def subcategories(self):
        key = 'category_{}_subcategories'.format(self.id)
        cached_subcategories = cache.get(key)
        if cached_subcategories:
            return cached_subcategories
        subcategories = Category.objects.filter(parent_category__id=self.id)
        cache.set(key, subcategories)
        return subcategories

    def has_parent_category(self):
        key = 'category_{}_has_parent_category'.format(self.id)
        cached_value = cache.get(key)
        if cached_value:
            return True if cached_value == 'True' else False
        value = True if self.parent_category else False
        if value:
            cache.set(key, 'True')
        else:
            cache.set(key, 'False')
        return value

    @property
    def full_name(self):  # to show in admin panel
        if not self.has_parent_category():
            return self.name
        cat = self
        full_name = self.name
        while cat.has_parent_category():
            full_name = "{} / {}".format(cat.parent_category.name, full_name)
            cat = cat.parent_category
        return full_name


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name=_('Manufacturer'))
    slug = AutoSlugField(
        always_update=True, populate_from='name', unique=True,
        slugify=utils.slugify_, db_index=True)
    image = models.ImageField(upload_to=utils.manufacturer_img_path,
                              blank=True, verbose_name=_('Image'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        key = 'manufacturer_{}_abs_url'.format(self.id)
        abs_url = cache.get(key)
        if abs_url:
            return abs_url
        abs_url = reverse(
            'shop:manufacturer_detail', kwargs={'slug': self.slug})
        cache.set(key, abs_url)
        return abs_url

    @property
    def products(self):
        key = 'manufacturer_{}_products'.format(self.id)
        cached_products = cache.get(key)
        if cached_products:
            return cached_products
        products = self.manufacturer_products.all()
        cache.set(key, products)
        return products

    @property
    def products_qty(self):
        key = 'manufacturer_{}_products_qty'.format(self.id)
        cached_products_qty = cache.get(key)
        if cached_products_qty:
            return cached_products_qty
        products_qty = self.manufacturer_products.count()
        cache.set(key, products_qty)
        return products_qty


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='category_products', verbose_name=_('Category'))
    manufacturer = models.ForeignKey(
        Manufacturer, related_name='manufacturer_products',
        verbose_name=_('Manufacturer'))
    name = models.CharField(
        max_length=200, db_index=True, verbose_name=_('Name'))
    model_name = models.CharField(
        max_length=200, blank=True, verbose_name=_('Model'))
    slug = AutoSlugField(
        always_update=True, populate_from=utils.base_for_product_slug,
        unique=True, slugify=utils.slugify_, db_index=True)
    main_image = models.ImageField(upload_to=utils.product_main_img_path,
                                   blank=True, verbose_name=_('Image'))
    description = models.TextField(
        blank=True, verbose_name=_('Description'))
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('Price'))
    stock = models.PositiveIntegerField(
        verbose_name=_('Stock Qty'))
    available = models.BooleanField(
        default=True, verbose_name=_('Available'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to=utils.product_img_path,
                              blank=True, verbose_name=_('Image'))
