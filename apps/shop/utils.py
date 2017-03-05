def product_main_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.slug, filename)


def product_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.product.slug, filename)


def category_img_path(instance, filename):
    return 'categories/{}/{}'.format(instance.slug, filename)
