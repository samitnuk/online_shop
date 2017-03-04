from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),

    url(r'^staff_area/category_create/$',
        views.category_create,
        name='category_create'),
    url(r'^staff_area/product_create/$',
        views.product_create,
        name='product_create'),
    url(r'^staff_area/product_update/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        views.product_update,
        name='product_update'),
]
