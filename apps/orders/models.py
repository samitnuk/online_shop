from django.db import models

from ..shop.models import Product


class Order(models.Model):
    first_name = models.CharField(verbose_name="Ім,я", max_length=50)
    last_name = models.CharField(verbose_name="Прізвище", max_length=50)
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(verbose_name="Адреса", max_length=250)
    postal_code = models.CharField(verbose_name="Поштовий код", max_length=20)
    city = models.CharField(verbose_name="Місто", max_length=100)
    created = models.DateTimeField(verbose_name="Створене", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Оновлене", auto_now=True)
    paid = models.BooleanField(verbose_name="Оплачене", default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return "Замовлення: {}".format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items")
    product = models.ForeignKey(Product, related_name="order_items")
    price = models.DecimalField(verbose_name="Ціна", max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name="К-сть", default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity