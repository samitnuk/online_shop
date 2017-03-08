from django_webtest import WebTest

from django.urls import reverse

from apps.shop.models import Category, Manufacturer, Product
from .. import utils


class ManufacturerWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_manufacturer_creating_by_regular_user(self):
        # user cannot create manufacturers
        resp = self.app.get(
            reverse('shop:manufacturer_create'),
            user=utils.get_regular_user()
        )
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(
            resp.location,
            '/admin/login/?next=/staff_area/manufacturer_create/')

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
        pass

    def test_manufacturer_updating_by_staff_member(self):
        pass

    def test_manufacturer_products_property(self):
        pass

    def test_manufacturer_products_qty_property(self):
        pass
