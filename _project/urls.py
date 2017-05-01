"""_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.apps import apps as django_apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^staff_area/', include('apps.shop.urls_for_staff',
                                 namespace='staff_area')),

    url(r'^paypal/', include('paypal.standard.ipn.urls')),

    url(r'^search/', include('haystack.urls')),

    url(r'^cart/', include('apps.cart.urls', namespace='cart')),
    url(r'^order/', include('apps.orders.urls', namespace='order')),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^coupons/', include('apps.coupons.urls', namespace='coupon')),
    url(r'^payment/', include('apps.payment.urls', namespace='payment')),
    url(r'^', include('apps.shop.urls', namespace='shop'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

rosetta_is_installed = django_apps.is_installed('rosetta')
if rosetta_is_installed:
    urlpatterns = [
        url(r'^rosetta/', include('rosetta.urls')),
    ] + urlpatterns

# ___________________________________________________________________________
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
