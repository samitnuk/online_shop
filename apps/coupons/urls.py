from django.conf.urls import url

from . import views, views_for_staff

urlpatterns = [
    url(r'^apply/$',
        views.coupon_apply,
        name='apply'),

    url(r'^list/$',
        views_for_staff.coupons,
        name='list'),
    url(r'^create/$',
        views_for_staff.coupon_create,
        name='create'),
]
