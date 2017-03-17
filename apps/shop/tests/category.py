from django_webtest import WebTest

from django.shortcuts import reverse

from apps.shop.models import Category, Product
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
        category = Category.objects.first()
        cat_slug = category.slug
        category_products = category.products()
        initial_count = category_products.count()

        product1 = Product.objects.first()
        if product1 in category_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product1.slug}),
            user=utils.get_staff_member(),
        ).form
        form['category'] = category.id
        form.submit()

        product2 = Product.objects.all()[2]
        if product2 in category_products:
            initial_count -= 1
        form = self.app.get(
            reverse('shop:product_update', kwargs={'slug': product2.slug}),
            user=utils.get_staff_member(),
        ).form
        form['category'] = category.id
        form.submit()

        category = Category.objects.filter(slug=cat_slug).first()
        cat_products = category.products()
        self.assertEqual(cat_products.count(), initial_count+2)
        self.assertIn(product1, cat_products)
        self.assertIn(product2, cat_products)

    def test_category_subcategories_method(self):
        category = Category.objects.first()
        cat_slug = category.slug

        sub_cat1 = Category.objects.all()[2]
        form = self.app.get(
            reverse('shop:category_update', kwargs={'slug': sub_cat1.slug}),
            user=utils.get_staff_member(),
        ).form
        form['parent_category'] = category.id
        form.submit()

        sub_cat2 = Category.objects.all()[3]
        form = self.app.get(
            reverse('shop:category_update', kwargs={'slug': sub_cat2.slug}),
            user=utils.get_staff_member(),
        ).form
        form['parent_category'] = category.id
        form.submit()

        category = Category.objects.filter(slug=cat_slug).first()
        subcategories = category.subcategories()
        self.assertEqual(subcategories.count(), 2)
        self.assertIn(sub_cat1, subcategories)
        self.assertIn(sub_cat2, subcategories)

    def test_category_has_parent_category_method(self):
        categories = Category.objects.all()
        parent_category = categories.first()

        sub_cat1 = categories[2]
        sub_cat1_name = sub_cat1.name
        form = self.app.get(
            reverse('shop:category_update', kwargs={'slug': sub_cat1.slug}),
            user=utils.get_staff_member(),
        ).form
        form['parent_category'] = parent_category.id
        form.submit()

        sub_cat1 = Category.objects.filter(name=sub_cat1_name).first()
        self.assertTrue(sub_cat1.has_parent_category())
        self.assertEqual(sub_cat1.parent_category, parent_category)

        sub_cat2 = categories[3]
        sub_cat2_name = sub_cat2.name
        form = self.app.get(
            reverse('shop:category_update', kwargs={'slug': sub_cat2.slug}),
            user=utils.get_staff_member(),
        ).form
        form['parent_category'] = parent_category.id
        form.submit()

        sub_cat2 = Category.objects.filter(name=sub_cat2_name).first()
        self.assertTrue(sub_cat2.has_parent_category())
        self.assertEqual(sub_cat2.parent_category, parent_category)

    def test_category_full_name_property(self):
        pass
