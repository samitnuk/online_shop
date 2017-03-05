def product_main_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.slug, filename)


def product_img_path(instance, filename):
    return 'products/{}/{}'.format(instance.product.slug, filename)


def category_img_path(instance, filename):
    return 'categories/{}/{}'.format(instance.slug, filename)


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
