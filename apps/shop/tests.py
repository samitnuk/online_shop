# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from django_webtest import WebTest

from apps.shop.models import Category, Product


def get_admin():
    admin, _ = User.objects.get_or_create(username='admin12345',
                                          password="drowssap")
    admin.is_staff = True
    admin.save()
    return admin


class FormTests(WebTest):

    fixtures = ['../load_data.json']

    user, _ = User.objects.get_or_create(username='username',
                                         password="drowssap")

    def test_product_creation_by_user(self):
        # user cannot create products
        resp = self.app.get(reverse('shop:product_create'), user=self.user)
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(resp.location,
                         '/admin/login/?next=/staff_area/product_create/')

    def test_product_creation_by_admin(self):
        form = self.app.get(
            reverse('shop:product_create'), user=get_admin()).form
        category = Category.objects.all().first()
        form['category'] = category.id
        form['name'] = "Тестовий продукт"
        form['model_name'] = 'Some test MDL-name'
        form['description'] = 'Some test description, not very long'
        # form['price'] = 12.34
        # form['stock'] = 42
        form['available'] = True
        form.submit()

        product = Product.objects.filter(
            model_name='Some test MDL-name').first()
        self.assertEqual(product.category, category)
        self.assertEqual(product.name, "Тестовий продукт")
        self.assertEqual(product.slug, slugify("Тестовий продукт",
                                               allow_unicode=True))
        self.assertEqual(product.description,
                         'Some test description, not very long')
        self.assertEqual(product.price, 12.34)
        self.assertEqual(product.stock, 42)
        self.assertTrue(product.available)
