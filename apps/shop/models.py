from django.core.urlresolvers import reverse
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

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


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', verbose_name="Категорія")
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Назва")
    slug = models.SlugField(
        max_length=200, db_index=True)
    image = models.ImageField(
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
