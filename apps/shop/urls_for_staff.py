from django.conf.urls import url

from . import views_for_staff

urlpatterns = [
    url(r'^$',
        views_for_staff.main,
        name='staff_area'),

    # Categories
    url(r'^categories/$',
        views_for_staff.categories,
        name='categories'),
    url(r'^categories/(?P<category_slug>[-\w]+)/$',
        views_for_staff.categories,
        name='category'),
    url(r'^category_create/$',
        views_for_staff.category_create,
        name='category_create'),
    url(r'^category_update/(?P<slug>[-\w]+)/$',
        views_for_staff.category_update,
        name='category_update'),

    # Manufacturers
    url(r'^manufacturers/$',
        views_for_staff.manufacturers,
        name='manufacturers'),
    url(r'^manufacturer_create/$',
        views_for_staff.manufacturer_create,
        name='manufacturer_create'),
    url(r'^manufacturer_update/(?P<slug>[-\w]+)/$',
        views_for_staff.manufacturer_update,
        name='manufacturer_update'),

    # Products
    url(r'^product_create/$',
        views_for_staff.product_create,
        name='product_create'),
    url(r'^product_update/(?P<slug>[-\w]+)/$',
        views_for_staff.product_update,
        name='product_update'),
]
