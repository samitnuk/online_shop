from django import forms

from ..shop.models import Product


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label="Кількість", choices=[], coerce=int)
    update = forms.BooleanField(required=False, initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        product = Product.objects.filter(id=product_id).first()
        choices = [(i, str(i)) for i in range(1, product.stock + 1)]
        self.fields['quantity'].choices = choices
