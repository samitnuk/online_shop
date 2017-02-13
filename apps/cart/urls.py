from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.cart_detail,
        name='cart_detail'),
    url(r'^remove/(?P<product_id>\d+)/$',
        views.cart_remove,
        name='cart_remove'),
    url(r'^add/(?P<product_id>\d+)/$',
        views.cart_add,
        name='cart_add'),
    url(r'^clear/$',
        views.cart_clear,
        name='cart_clear')
]
