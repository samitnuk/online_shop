from django_webtest import WebTest

from django.conf import settings
from django.shortcuts import reverse

from apps.shop.models import Product
from apps.shop import utils


class OrdersWebTests(WebTest):

    fixtures = ['../load_data.json']

    def test_order_creation(self):
        products = Product.objects.all()
        product1 = products.order_by('?').first()
        product2 = products.order_by('?').first()
        while product1 == product2:
            product2 = products.order_by('?').first()
        print(product1, product2)
        form = self.app.get(
            reverse(
                'shop:product_detail',
                kwargs={'slug': product1.slug},
            ),
        ).form
        qty = product1.stock - 1 if product1.stock != 1 else 1
        form['quantity'] = qty
        form.submit()

        form = self.app.get(
            reverse(
                'shop:product_detail',
                kwargs={'slug': product2.slug},
            ),
        ).form
        qty = product2.stock - 1 if product2.stock != 1 else 1
        form['quantity'] = qty
        form.submit()
        cart = self.app.session[settings.CART_SESSION_ID]
        print(cart)
        user = utils.get_staff_member()
        print(user)
        form = self.app.get(reverse('orders:create'), user=user)
        # form['first_name'] = "Test_first_name"
        # form['last_name'] = "Test_last_name"
        # form['carrier'] = "Test carrier"
        # form['city'] = "Testtown"
        # form['warehouse_num'] = "2"
        # form['phone_num'] = "(000) 11-22-333"
        # response = form.submit().follow()
        #
        # user = response.context['user']
        #
        # order = user.products.first()
        #
        # self.assertEqual(order.first_name, "Test_first_name")
