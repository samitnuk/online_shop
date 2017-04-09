from django.core.cache import cache

from .models import Category


def menu_categories(request):
    key = 'menu_categories'
    cached_value = cache.get(key)
    if cached_value:
        return cached_value
    menu_categories_ = Category.objects.all()
    return {'menu_categories': menu_categories_}
