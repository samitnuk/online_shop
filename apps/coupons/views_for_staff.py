from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Coupon
from .forms import CouponForm


@staff_member_required
def coupons(request):
    context = {'coupons': Coupon.objects.all()}
    return render(request, 'coupons/staff_area/coupons.html', context)


def coupon_create(request):
    form = CouponForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('coupon:list')
    context = {'form': form}
    return render(request, 'coupons/staff_area/coupon_form.html', context)
