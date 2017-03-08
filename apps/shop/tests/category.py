from django_webtest import WebTest

from django.shortcuts import reverse

from apps.shop.models import Category, Manufacturer, Product
from .. import utils


class CategoryWebTests(WebTest):

    fixtures = ['.././load_data.json']

    def test_category_creation_by_regular_user(self):
        # user cannot create categories
        response = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_regular_user()
        )
        planned_resp = '/admin/login/?next=/staff_area/category_create/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp,
        )

    def test_category_creating_by_staff_member(self):
        # test for case with parent_category
        form = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_staff_member()
        ).form
        category = Category.objects.first()
        name = "Тестова категорія"
        form['name'] = name
        form['parent_category'] = category.id
        form.submit()

        category = Category.objects.filter(name=name).first()
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, utils.slugify_(name))
        self.assertTrue(category.has_parent_category())
        self.assertFalse(category.products())  # <QuerySet []>
        self.assertFalse(category.subcategories())  # <QuerySet []>

        # test for case without parent_category
        form = self.app.get(
            reverse('shop:category_create'),
            user=utils.get_staff_member()
        ).form
        name = "Тестова категорія 2"
        form['name'] = name
        form.submit()

        category = Category.objects.filter(name=name).first()
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, utils.slugify_(name))
        self.assertFalse(category.has_parent_category())
        self.assertFalse(category.products())  # <QuerySet []>
        self.assertFalse(category.subcategories())  # <QuerySet []>

    def test_category_updating_by_regular_user(self):
        # user cannot update categories
        category = Category.objects.first()
        response = self.app.get(
            reverse('shop:category_update', kwargs={'slug': category.slug}),
            user=utils.get_regular_user(),
        )
        planned_resp = '/admin/login/?next=/staff_area/category_update/{}/'
        self.assertRedirects(
            response=response,
            expected_url=planned_resp.format(category.slug),
        )

    def test_category_updating_by_staff_member(self):
        category = Category.objects.first()
        parent_category = Category.objects.all()[2]
        form = self.app.get(
            reverse('shop:category_update', kwargs={'slug': category.slug}),
            user=utils.get_staff_member(),
        ).form
        name = "Нова тестова назва"
        form['name'] = name
        form['parent_category'] = parent_category.id
        form.submit()

        category_upd = Category.objects.filter(name=name).first()
        self.assertEqual(category_upd.name, name)
        self.assertEqual(category_upd.slug, utils.slugify_(name))
        self.assertTrue(category_upd.has_parent_category())
        self.assertEqual(category_upd.parent_category, parent_category)

    def test_category_products_method(self):
        pass

    def test_category_subcategories_method(self):
        pass

    def test_category_has_parent_category_method(self):
        pass

    def test_category_full_name_property(self):
        pass
