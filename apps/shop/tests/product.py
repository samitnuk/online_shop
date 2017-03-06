from decimal import Decimal

from django_webtest import WebTest

# from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from apps.shop.models import Category, Manufacturer, Product
from .. import utils


class ProductWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_product_creating_by_reqular_user(self):
        # user cannot create products
        resp = self.app.get(reverse('shop:product_create'),
                            user=utils.get_regular_user())
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(resp.location,
                         '/admin/login/?next=/staff_area/product_create/')

    def test_product_creating_by_staff_member(self):
        form = self.app.get(
            reverse('shop:product_create'),
            user=utils.get_staff_member()
        ).form
        category = Category.objects.first()
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

        product = Product.objects.filter(model_name=model_name).first()
        self.assertEqual(product.category, category)
        self.assertEqual(product.name, "Тестовий продукт")
        self.assertEqual(product.slug, slugify(
            '{}-{}'.format(name, model_name), allow_unicode=True))
        self.assertEqual(product.description,
                         'Some test description, not very long')
        self.assertEqual(product.price, Decimal('12.34'))
        self.assertEqual(product.stock, 42)
        self.assertTrue(product.available)

    def test_product_creating_by_staff_member_no_category_selected(self):
        form = self.app.get(
            reverse('shop:product_create'),
            user=utils.get_staff_member()
        ).form
        name = "Тестовий продукт test"
        model_name = 'Some test MDL-name'
        # category is not selected
        form['name'] = name
        form['model_name'] = model_name
        form['description'] = 'Some test description, not very long'
        form['available'] = True
        form['price'] = '12.34'
        form['stock'] = '42'
        form.submit()

        product = Product.objects.filter(
            model_name='Some test MDL-name').first()
        self.assertIsNone(product)

    def test_product_creating_by_staff_member_no_manufacturer_selected(self):
        # In future Manufacturer will be required field
        pass

    def test_product_updating_by_reqular_user(self):
        pass

    def test_product_updating_by_staff_member(self):
        pass
