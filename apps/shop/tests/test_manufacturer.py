from django.urls import reverse
from django.core.cache import cache
from django_webtest import WebTest

from apps.shop.models import Manufacturer, Product

from .. import utils


class ManufacturerWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_manufacturer_creating_by_regular_user(self):
        # user cannot create manufacturers
        response = self.app.get(
            reverse('staff_area:manufacturer_create'),
            user=utils.get_regular_user()
        )
        planned_resp = '/admin/login/?next=/staff_area/manufacturer_create/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp,
        )

    def test_manufacturer_creating_by_staff_member(self):
        form = self.app.get(
            reverse('staff_area:manufacturer_create'),
            user=utils.get_staff_member()
        ).forms['main-form']
        name = "Тестовий виробник"
        form['name'] = name
        form.submit()

        manufacturer = Manufacturer.objects.filter(name=name).first()
        self.assertEqual(manufacturer.name, name)
        self.assertEqual(manufacturer.slug, utils.slugify_(name))

    def test_manufacturer_updating_by_regular_user(self):
        # user cannot update manufacturers
        manufacturer = Manufacturer.objects.first()
        response = self.app.get(
            reverse('staff_area:manufacturer_update',
                    kwargs={'slug': manufacturer.slug}),
            user=utils.get_regular_user()
        )
        planned_resp = '/admin/login/?next=/staff_area/manufacturer_update/{}/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp.format(manufacturer.slug),
        )

    def test_manufacturer_updating_by_staff_member(self):
        manufacturer = Manufacturer.objects.first()
        form = self.app.get(
            reverse('staff_area:manufacturer_update',
                    kwargs={'slug': manufacturer.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        name = "Новий виробник"
        form['name'] = name
        form.submit()

        manufacturer_upd = Manufacturer.objects.filter(name=name).first()
        self.assertEqual(manufacturer_upd.name, name)
        self.assertEqual(manufacturer_upd.slug, utils.slugify_(name))

    def test_manufacturer_products_property(self):

        cache.clear()

        manufacturer = Manufacturer.objects.first()
        m_slug = manufacturer.slug
        m_products = manufacturer.products
        initial_count = m_products.count()

        # Test cache _________________________________________________________
        key = 'manufacturer_{}_products'.format(manufacturer.id)
        manufacturer_products = manufacturer.products
        cached_products = cache.get(key)
        self.assertEqual(manufacturer_products.count(),
                         cached_products.count())
        # End test cache _____________________________________________________

        product1 = Product.objects.first()
        if product1 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product1.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        form['manufacturer'] = manufacturer.id
        form.submit()

        # Test cache _________________________________________________________
        self.assertIsNone(cache.get(key))
        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        products = manufacturer.products
        cached_products = cache.get(key)
        self.assertIn(product1, products)
        self.assertIn(product1, cached_products)
        # End test cache _____________________________________________________

        product2 = Product.objects.all()[2]
        if product2 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product2.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        form['manufacturer'] = manufacturer.id
        form.submit()

        # Test cache _________________________________________________________
        self.assertIsNone(cache.get(key))
        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        products = manufacturer.products
        cached_products = cache.get(key)
        self.assertIn(product2, products)
        self.assertIn(product2, cached_products)
        # End test cache _____________________________________________________

        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        m_products = manufacturer.products
        self.assertEqual(m_products.count(), initial_count + 2)
        self.assertIn(product1, m_products)
        self.assertIn(product2, m_products)

    def test_manufacturer_products_qty_property(self):
        manufacturer = Manufacturer.objects.first()
        m_slug = manufacturer.slug
        m_products = manufacturer.products
        initial_count = m_products.count()

        # Test cache _________________________________________________________
        key = 'manufacturer_{}_products_qty'.format(manufacturer.id)
        products_qty = manufacturer.products_qty
        cached_products_qty = cache.get(key)
        self.assertEqual(products_qty, cached_products_qty)
        # End test cache _____________________________________________________

        product1 = Product.objects.first()
        if product1 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product1.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        form['manufacturer'] = manufacturer.id
        form.submit()

        # Test cache _________________________________________________________
        self.assertIsNone(cache.get(key))
        # End test cache _____________________________________________________

        product2 = Product.objects.all()[2]
        if product2 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('staff_area:product_update',
                    kwargs={'slug': product2.slug}),
            user=utils.get_staff_member(),
        ).forms['main-form']
        form['manufacturer'] = manufacturer.id
        form.submit()

        # Test cache _________________________________________________________
        self.assertIsNone(cache.get(key))
        # End test cache _____________________________________________________

        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        self.assertEqual(manufacturer.products_qty, initial_count + 2)

    def test_get_absolute_url_method(self):

        cache.clear()

        manufacturer = Manufacturer.objects.order_by('?').first()
        absolute_url = reverse(
            'shop:product_list_by_manufacturer',
            kwargs={'manufacturer_slug': manufacturer.slug})

        self.assertEqual(manufacturer.get_absolute_url(), absolute_url)

        # Test cache _________________________________________________________
        key = 'manufacturer_{}_abs_url'.format(manufacturer.id)
        cached_abs_url = cache.get(key)
        self.assertEqual(cached_abs_url, absolute_url)
        # End test cache _____________________________________________________
