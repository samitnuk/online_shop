from django_webtest import WebTest

from django.urls import reverse
from django.utils.text import slugify

from apps.shop.models import Category, Manufacturer, Product
from .. import utils


class CategoryWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_category_creation_by_reqular_user(self):
        # user cannot create categories
        resp = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_regular_user()
        )
        self.assertEqual(resp.status, '302 Found')
        self.assertEqual(resp.location,
                         '/admin/login/?next=/staff_area/category_create/')

    def test_category_creating_by_staff_member(self):
        # test for case with parent_category
        form = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_staff_member()
        ).form
        category = Category.objects.first()
        name = "Тестова категорія"
        slug = slugify(name, allow_unicode=True)
        form['name'] = name
        form['parent_category'] = category.id
        form.submit()

        category = Category.objects.filter(name=name).first()
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, slug)
        self.assertTrue(category.has_parent_category())
        self.assertFalse(category.products())  # <QuerySet []>
        self.assertFalse(category.subcategories())  # <QuerySet []>

        # test for case without parent_category
        form = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_staff_member()
        ).form
        name = "Тестова категорія 2"
        slug = slugify(name, allow_unicode=True)
        form['name'] = name
        form.submit()

        category = Category.objects.filter(name=name).first()
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, slug)
        self.assertFalse(category.has_parent_category())
        self.assertFalse(category.products())  # <QuerySet []>
        self.assertFalse(category.subcategories())  # <QuerySet []>

    def test_category_updating_by_reqular_user(self):
        pass

    def test_category_updating_by_staff_member(self):
        pass

    def test_category_products_method(self):
        pass

    def test_category_subcategories_method(self):
        pass

    def test_category_has_parent_category_method(self):
        pass

    def test_category_full_name_property(self):
        pass
