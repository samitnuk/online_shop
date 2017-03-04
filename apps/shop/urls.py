from django.conf.urls import url

from . import views, views_for_staff


urlpatterns = [

    # ----- URLs for staff members
    url(r'^staff_area/$',
        views_for_staff.staff_area,
        name='staff_area'),
    url(r'^staff_area/category_create/$',
        views_for_staff.category_create,
        name='category_create'),
    url(r'^staff_area/product_create/$',
        views_for_staff.product_create,
        name='product_create'),
    url(r'^staff_area/product_update/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        views_for_staff.product_update,
        name='product_update'),

    # ----- URLs for regular users
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.product_list,
        name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]
