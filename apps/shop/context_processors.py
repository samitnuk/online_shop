from django.core.cache import cache

from .models import Category


def menu_categories(request):
    key = 'menu_categories'
    cached_menu_categories = cache.get(key)
    if cached_menu_categories is not None:
        return {'menu_categories': cached_menu_categories}
    menu_categories_ = Category.objects.all()
    cache.set(key, menu_categories_)
    return {'menu_categories': menu_categories_}
