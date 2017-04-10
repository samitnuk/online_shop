from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Category, Product


@receiver(post_save, sender=Category)
def clean_category_related_cache(instance, **_):
    category = instance
    key = 'category_{}_has_parent_category'.format(category.id)
    cache.delete(key)


@receiver(post_save, sender=Product)
@receiver(pre_delete, sender=Product)
def clean_product_related_cache(instance, **_):
    product = instance
    category = product.category
    key = 'category_{}_products'.format(category.id)
    cache.delete(key)
