from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Category, Product


@receiver(post_save, sender=Category)
@receiver(pre_delete, sender=Category)
def clean_category_related_cache(instance, **_):
    category = instance
    cache.delete('category_{}_abs_url'.format(category.id))
    cache.delete('category_{}_has_parent_category'.format(category.id))
    cache.delete('menu_categories')
    if category.parent_category is not None:
        parent_category = category.parent_category
        cache.delete('category_{}_subcategories'.format(parent_category.id))


@receiver(post_save, sender=Product)
@receiver(pre_delete, sender=Product)
def clean_product_related_cache(instance, **_):
    product = instance
    category = product.category
    cache.delete('category_{}_products'.format(category.id))
