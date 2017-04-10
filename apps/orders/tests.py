from django.shortcuts import reverse
from django_webtest import WebTest

from apps.orders.models import Order
from apps.shop import utils
from apps.shop.models import Product


class OrdersWebTests(WebTest):

    fixtures = ['../load_data.json']

    def test_order_creation(self):
        # Login user
        user = utils.get_regular_user()
        form = self.app.get(reverse('accounts:login')).forms['main-form']
        form['username'] = user.username
        form['password'] = "asdkjfoih1222pkljkh"
        form.submit().follow()

        # Get products for tests
        products = Product.objects.all()
        product1 = products.order_by('?').first()
        product2 = products.order_by('?').first()
        while product1 == product2:
            product2 = products.order_by('?').first()

        # Add 1st product to cart
        form = self.app.get(
            reverse(
                'shop:product_detail',
                kwargs={'slug': product1.slug},
            ),
        ).forms['main-form']
        qty = product1.stock - 1 if product1.stock != 1 else 1
        form['quantity'] = qty
        form.submit()

        # Add 2nd product to cart
        form = self.app.get(
            reverse(
                'shop:product_detail',
                kwargs={'slug': product2.slug},
            ),
        ).forms['main-form']
        qty = product2.stock - 1 if product2.stock != 1 else 1
        form['quantity'] = qty
        form.submit()

        # Create order
        form = self.app.get(reverse('order:create')).forms['main-form']
        form['first_name'] = "Test_first_name"
        form['last_name'] = "Test_last_name"
        form['carrier'] = "Test carrier"
        form['city'] = "Testtown"
        form['warehouse_num'] = "2"
        form['phone_num'] = "(000) 11-22-333"
        response = form.submit()

        user = response.context['user']

        order = Order.objects.filter(user=user).first()

        self.assertEqual(str(order), "Замовлення №: {}".format(order.id))
        self.assertEqual(order.first_name, "Test_first_name")
        self.assertEqual(order.last_name, "Test_last_name")
        self.assertEqual(order.carrier, "Test carrier")
        self.assertEqual(order.city, "Testtown")
        self.assertEqual(order.warehouse_num, 2)
        self.assertEqual(order.phone_num, "(000) 11-22-333")
        self.assertFalse(order.paid)

        items = order.get_items()
        for item in items:
            self.assertIn(item.product, [product1, product2])

        self.assertEqual(
            order.get_total_cost(),
            sum([item.get_cost() for item in items])
        )
