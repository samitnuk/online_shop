from django_webtest import WebTest

from django.conf import settings
from django.shortcuts import reverse

from apps.shop.models import Product


class CartWebTests(WebTest):

    fixtures = ['../load_data.json']

    # Helpers ----------------------------------------------------------------
    def add_product_to_cart(self, product):
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

    def add_two_products_to_cart(self):
        products = Product.objects.all()
        product1 = products.order_by('?').first()
        product2 = products.order_by('?').first()
        while product1 == product2:
            product2 = products.order_by('?').first()

        self.add_product_to_cart(product1)
        self.add_product_to_cart(product2)

        return product1, product2

    # Tests ------------------------------------------------------------------
    def test_cart_add_product_GET(self):
        product1 = Product.objects.order_by('?').first()
        # GET is not allowed
        self.app.get(
            reverse(
                'cart:add_product',
                kwargs={'product_id': product1.id}
            ),
            status=405,  # webtest.app.AppError in other case
        )

    def test_cart_add_product_POST(self):
        self.add_two_products_to_cart()

    def test_cart_remove_product(self):
        product1, product2 = self.add_two_products_to_cart()

        self.app.get(
            reverse(
                'cart:remove_product',
                kwargs={'product_id': product2.id}
            ),
        )

        cart = self.app.session[settings.CART_SESSION_ID]
        product_data = cart.get(str(product2.id))
        self.assertIsNone(product_data)

    def test_cart_detail(self):
        product1, product2 = self.add_two_products_to_cart()
        response = self.app.get(reverse('cart:detail'))

        self.assertIn(product1.slug, response)
        self.assertIn(product2.slug, response)

    def test_cart_clean(self):
        self.add_two_products_to_cart()
        self.app.get(reverse('cart:clear'))
        cart = self.app.session.get(settings.CART_SESSION_ID)
        self.assertIsNone(cart)
