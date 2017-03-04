from decimal import Decimal

# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from django_webtest import WebTest

from apps.shop.models import Category, Product


def get_staff_member():
    admin, _ = User.objects.get_or_create(username='admin12345',
                                          password="drowssap")
    admin.is_staff = True
    admin.save()
    return admin


def get_regular_user():
    user, _ = User.objects.get_or_create(username='username',
                                         password="drowssap")
    return user


class FormTests(WebTest):

    fixtures = ['../load_data.json']

    def test_product_creation_by_reqular_user(self):
        # user cannot create products
        resp = self.app.get(reverse('shop:product_create'),
                            user=get_regular_user())
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(resp.location,
                         '/admin/login/?next=/staff_area/product_create/')

    def test_product_creation_by_staff_member(self):
        form = self.app.get(
            reverse('shop:product_create'), user=get_staff_member()).form
        category = Category.objects.all().first()
        name = "Тестовий продукт"
        model_name = 'Some test MDL-name'
        form['category'] = category.id
        form['name'] = name
        form['model_name'] = model_name
        form['description'] = 'Some test description, not very long'
        form['available'] = True
        form['price'] = '12.34'
        form['stock'] = '42'
        form.submit()

        product = Product.objects.filter(
            model_name='Some test MDL-name').first()
        self.assertEqual(product.category, category)
        self.assertEqual(product.name, "Тестовий продукт")
        self.assertEqual(product.slug, slugify(
            '{}-{}'.format(name, model_name), allow_unicode=True))
        self.assertEqual(product.description,
                         'Some test description, not very long')
        self.assertEqual(product.price, Decimal('12.34'))
        self.assertEqual(product.stock, 42)
        self.assertTrue(product.available)

    def test_category_creation_by_reqular_user(self):
        # user cannot create categories
        resp = self.app.get(reverse('shop:category_create'),
                            user=get_regular_user())
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(resp.location,
                         '/admin/login/?next=/staff_area/category_create/')

    def test_category_creation_by_staff_member(self):
        form = self.app.get(
            reverse('shop:category_create'), user=get_staff_member()).form
        slug = slugify("Тестова категорія", allow_unicode=True)
        form['name'] = "Тестова категорія"
        form['parent_category'] = 1
        form.submit()

        category = Category.objects.filter(name="Тестова категорія").first()
        self.assertEqual(category.name, "Тестова категорія")
        self.assertEqual(category.slug, slug)
