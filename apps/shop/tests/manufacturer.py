from django_webtest import WebTest

from django.urls import reverse

from apps.shop.models import Category, Manufacturer, Product
from .. import utils


class ManufacturerWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_manufacturer_creating_by_regular_user(self):
        # user cannot create manufacturers
        response = self.app.get(
            reverse('shop:manufacturer_create'),
            user=utils.get_regular_user()
        )
        planned_resp = '/admin/login/?next=/staff_area/manufacturer_create/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp,
        )

    def test_manufacturer_creating_by_staff_member(self):
        form = self.app.get(
            reverse('shop:manufacturer_create'),
            user=utils.get_staff_member()
        ).form
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
            reverse('shop:manufacturer_update',
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
            reverse('shop:manufacturer_update',
                    kwargs={'slug': manufacturer.slug}),
            user=utils.get_staff_member(),
        ).form
        name = "Новий виробник"
        form['name'] = name
        form.submit()

        manufacturer_upd = Manufacturer.objects.filter(name=name).first()
        self.assertEqual(manufacturer_upd.name, name)
        self.assertEqual(manufacturer_upd.slug, utils.slugify_(name))

    def test_manufacturer_products_property(self):
        manufacturer = Manufacturer.objects.first()
        m_slug = manufacturer.slug
        m_products = manufacturer.products
        initial_count = m_products.count()

        product1 = Product.objects.first()
        if product1 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product1.slug}),
            user=utils.get_staff_member(),
        ).form
        form['manufacturer'] = manufacturer.id
        form.submit()

        product2 = Product.objects.all()[2]
        if product2 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product2.slug}),
            user=utils.get_staff_member(),
        ).form
        form['manufacturer'] = manufacturer.id
        form.submit()

        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        m_products = manufacturer.products
        self.assertEqual(m_products.count(), initial_count+2)
        self.assertIn(product1, m_products)
        self.assertIn(product2, m_products)

    def test_manufacturer_products_qty_property(self):
        manufacturer = Manufacturer.objects.first()
        m_slug = manufacturer.slug
        m_products = manufacturer.products
        initial_count = m_products.count()

        product1 = Product.objects.first()
        if product1 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product1.slug}),
            user=utils.get_staff_member(),
        ).form
        form['manufacturer'] = manufacturer.id
        form.submit()

        product2 = Product.objects.all()[2]
        if product2 in m_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product2.slug}),
            user=utils.get_staff_member(),
        ).form
        form['manufacturer'] = manufacturer.id
        form.submit()

        manufacturer = Manufacturer.objects.filter(slug=m_slug).first()
        self.assertEqual(manufacturer.products_qty, initial_count+2)
