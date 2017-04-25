from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main, name='main_page'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^product_detail/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
    url(r'^(?P<manufacturer_slug>[-\w]+)/$',
        views.product_list_by_manufacturer,
        name='product_list_by_manufacturer'),
]
