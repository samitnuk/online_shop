from django.core.urlresolvers import reverse
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)
    parent_category = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            kwargs={'category_slug': self.slug})

    @property
    def products(self):
        return self.category_products.all()

    def subcategories(self):
        return Category.objects.filter(parent_category__id=self.id)

    def has_parent_category(self):
        return True if self.parent_category else False

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
        max_length=200, db_index=True, verbose_name="Виробник")
    slug = models.SlugField(
        max_length=200, db_index=True, allow_unicode=True)

    class Meta:
        verbose_name = "Виробник"
        verbose_name_plural = "Виробники"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            kwargs={'id': self.id, 'slug': self.slug})

    @property
    def products(self):
        return self.manufacturer_products.all()


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='category_products', verbose_name="Категорія")
    manufacturer = models.ForeignKey(
        Manufacturer, related_name='manufacturer_products',
        verbose_name="Виробник", blank=True, null=True)
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Назва")
    slug = models.SlugField(
        max_length=200, db_index=True, allow_unicode=True)
    model_name = models.CharField(
        max_length=200, blank=True, verbose_name="Модель")
    main_image = models.ImageField(
        upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Зображення")
    description = models.TextField(
        blank=True, verbose_name="Опис")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ціна")
    stock = models.PositiveIntegerField(
        verbose_name="На складі")
    available = models.BooleanField(
        default=True, verbose_name="Доступний")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        index_together = ['id', 'slug']
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            kwargs={'id': self.id, 'slug': self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/', blank=True, verbose_name="Зображення")
