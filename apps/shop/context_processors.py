from django.core.cache import cache

from .models import Category


def menu_categories(request):
    key = 'menu_categories'
    menu_categories_ = cache.get(key)
    if menu_categories_ is None:
        menu_categories_ = Category.objects.all()
        cache.set(key, menu_categories_)
    return {'menu_categories': menu_categories_}
