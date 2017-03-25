from django import forms

from .models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField()


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code', 'valid_from', 'valid_to', 'discount', 'active')
