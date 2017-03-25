from django.conf.urls import url

from . import views


urlpatterns = [
    url('^apply', views.coupon_apply, name='apply'),
]
