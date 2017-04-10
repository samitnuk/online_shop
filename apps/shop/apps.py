from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'apps.shop'

    def ready(self):
        import apps.shop.signals
