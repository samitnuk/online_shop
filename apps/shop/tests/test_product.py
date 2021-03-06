from decimal import Decimal

from django.core.cache import cache
from django.urls import reverse
from django_webtest import WebTest

from apps.shop.models import Category, Manufacturer, Product

from .. import utils


class ProductWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_product_detail_page(self):
        product = Product.objects.first()
        response = self.app.get(reverse('shop:product_detail',
                                        kwargs={'slug': product.slug}))
        self.assertContains(
            response, product.model_name, count=1, status_code=200)

    def test_product_creating_by_regular_user(self):
        # user cannot create products
        response = self.app.get(reverse('staff_area:product_create'),
                                user=utils.get_regular_user())
        planned_resp = '/admin/login/?next=/staff_area/product_create/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp,
        )

    def test_product_creating_by_staff_member(self):
        form = self.app.get(
            reverse('staff_area:product_create'),
            user=utils.get_staff_member()
        ).forms['main-form']
        category = Category.objects.first()
        manufacturer = Manufacturer.objects.first()
        name = "Тестовий продукт"
        model_name = 'Some test MDL-name'
        form['category'] = category.id
        form['manufacturer'] = manufacturer.id
        form['name'] = name
        form['model_name'] = model_name
        form['description'] = 'Some test description, not very long'
        form['available'] = True
        form['price'] = '12.34'
        form['stock'] = '42'
        form.submit(upload_files=[
            ('main_image', '.././test_images/test_img.jpg'),
            ('form-0-image', '.././test_images/test_img_2.jpg'),
            ('form-1-image', '.././test_images/test_img_3.jpg'),
        ])

        product = Product.objects.filter(model_name=model_name).first()
        self.assertEqual(product.category, category)
        self.assertEqual(product.name, "Тестовий продукт")
        self.assertEqual(product.slug, utils.slugify_(
            '{}-{}'.format(name, model_name)))
        self.assertEqual(product.description,
                         'Some test description, not very long')
        self.assertEqual(product.price, Decimal('12.34'))
        self.assertEqual(product.stock, 42)
        self.assertTrue(product.available)
        self.assertIsNotNone(product.main_image)
        self.assertEqual(product.images.count(), 2)

    def test_product_creating_by_staff_member_no_category_selected(self):
        manufacturer = Manufacturer.objects.first()
        form = self.app.get(
            reverse('staff_area:product_create'),
            user=utils.get_staff_member()
        ).forms['main-form']
        name = "Тестовий продукт test"
        model_name = 'Some test MDL-name'
        # category is not selected
        form['name'] = name
        form['model_name'] = model_name
        form['manufacturer'] = manufacturer.id
        form['description'] = 'Some test description, not very long'
        form['available'] = True
        form['price'] = '12.34'
        form['stock'] = '42'
        form.submit()

        product = Product.objects.filter(
            model_name='Some test MDL-name').first()
        self.assertIsNone(product)

    def test_product_creating_by_staff_member_no_manufacturer_selected(self):
        category = Category.objects.first()
        form = self.app.get(
            reverse('staff_area:product_create'),
            user=utils.get_staff_member()
        ).forms['main-form']
        name = "Тестовий продукт test test"
        model_name = 'Some test MDL-name 123'
        # category is not selected
        form['name'] = name
        form['model_name'] = model_name
        form['category'] = category.id
        form['description'] = 'Some test description, not very long'
        form['available'] = True
        form['price'] = '12.34'
        form['stock'] = '42'
        form.submit()

        product = Product.objects.filter(model_name=model_name).first()
        self.assertIsNone(product)

    def test_product_updating_by_regular_user(self):
        # user cannot update categories
        product = Product.objects.first()
        response = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product.slug}),
            user=utils.get_regular_user(),
        )
        planned_resp = '/admin/login/?next=/staff_area/product_update/{}/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp.format(product.slug),
        )

    def test_product_updating_by_staff_member(self):
        product = Product.objects.first()
        category = Category.objects.first()
        manufacturer = Manufacturer.objects.first()
        form = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        name = "Нова тестова назва"
        model_name = "Модель 234UI"
        form['name'] = name
        form['model_name'] = model_name
        form['category'] = category.id
        form['manufacturer'] = manufacturer.id
        form.submit()

        product_upd = Product.objects.filter(name=name).first()
        self.assertEqual(product_upd.name, name)
        self.assertEqual(product_upd.slug,
                         utils.slugify_('{}-{}'.format(name, model_name)))
        self.assertEqual(product_upd.category, category)
        self.assertEqual(product_upd.manufacturer, manufacturer)

    def test_get_absolute_url_method(self):

        cache.clear()

        product = Product.objects.order_by('?').first()
        absolute_url = reverse(
            'shop:product_detail', kwargs={'slug': product.slug})

        self.assertEqual(product.get_absolute_url(), absolute_url)

        # Test cache _________________________________________________________
        key = 'product_{}_abs_url'.format(product.id)
        cached_abs_url = cache.get(key)
        self.assertEqual(cached_abs_url, absolute_url)
        # End test cache _____________________________________________________
