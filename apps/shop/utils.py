from django.contrib.auth.models import User
from slugify import slugify


def product_main_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.slug, filename)


def product_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.product.slug, filename)


def category_img_path(instance, filename):
    return 'categories/{}/{}'.format(instance.slug, filename)


def manufacturer_img_path(instance, filename):
    return 'manufacturers/{}/{}'.format(instance.slug, filename)


def cat_choices(categories):
    CHOICES = [[0, '---------']]
    main_cats = [cat for cat in categories if not cat.has_parent_category()]

    for cat in main_cats:
        CHOICES.append([int(cat.id), cat.name])
        if cat.subcategories() is None:
            continue
        for subcat in cat.subcategories():
            CHOICES.append([subcat.id, "___  {}".format(subcat.name)])
            if subcat.subcategories() is None:
                continue
            for subcat_ in subcat.subcategories():
                choice = [subcat_.id, "______ {}".format(subcat_.name)]
                CHOICES.append(choice)

    return CHOICES


def base_for_product_slug(instance):
    return '{}-{}'.format(instance.name, instance.model_name)


def slugify_(some_string):
    """
    Convert 'some_string' to correct slug.

    Note: slugify() converts some symbols to "'" (apostrophe),
    and SlugField does not accept apostrophes.
    So this fixed by replacement of all apostrophes.
    """
    return slugify(some_string, only_ascii=True).replace("'", "")


# Helpers for tests ----------------------------------------------------------
def get_staff_member():
    """Create staff member """
    admin, _ = User.objects.get_or_create(username='admin12345',
                                          password="password12345")
    admin.is_staff = True
    admin.save()
    return admin


def get_regular_user():
    """Create regular user """
    user = User.objects.create_user(
        username='test_user',
        first_name='First',
        last_name='Last',
        email='sometest@email.ts',
        password="asdkjfoih1222pkljkh",
    )
    user.save()
    return user
