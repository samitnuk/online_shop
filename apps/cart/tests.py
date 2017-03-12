from django_webtest import WebTest

from django.conf import settings
from django.shortcuts import reverse

from apps.shop.models import Product


class CartWebTests(WebTest):

    fixtures = ['../load_data.json']

    def test_cart_add_product(self):
        product = Product.objects.order_by('?').first()

        # test GET Method (GET is not allowed)
        self.app.get(
            reverse(
                'cart:add_product',
                kwargs={'product_id': product.id}
            ),
            status=405,  # webtest.app.AppError in other case
        )

        # test POST Method
        form = self.app.get(
            reverse(
                'shop:product_detail',
                kwargs={'slug': product.slug},
            ),
        ).form
        qty = product.stock - 1 if product.stock != 1 else 1
        form['quantity'] = qty
        form.submit()

        cart = self.app.session[settings.CART_SESSION_ID]
        product_data = cart[str(product.id)]
        self.assertEqual(product_data['price'], str(product.price))
        self.assertEqual(product_data['quantity'], qty)
