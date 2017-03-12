from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.cart_detail,
        name='detail'),
    url(r'^remove/(?P<product_id>\d+)/$',
        views.cart_remove_product,
        name='remove_product'),
    url(r'^add/(?P<product_id>\d+)/$',
        views.cart_add_product,
        name='add_product'),
    url(r'^clear/$',
        views.cart_clear,
        name='clear')
]
