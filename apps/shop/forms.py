from django import forms
from django.utils.text import slugify

from .models import Category, Product, ProductImage


def categories_choices():
    CATEGORIES_CHOICES = []
    all_cats = Category.objects.all()
    main_cats = [cat for cat in all_cats if not cat.has_parent_category()]

    for cat in main_cats:
        CATEGORIES_CHOICES.append([int(cat.id), cat.name])
        if cat.subcategories() is None:
            continue
        for subcat in cat.subcategories():
            CATEGORIES_CHOICES.append([subcat.id, "-   {}".format(subcat.name)])
            if subcat.subcategories() is None:
                continue
            for subcat_ in subcat.subcategories():
                choice = [subcat_.id, " -- {}".format(subcat_.name)]
                CATEGORIES_CHOICES.append(choice)

    return CATEGORIES_CHOICES


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категорія',
                                 choices=categories_choices(),)

    class Meta:
        model = Product
        fields = (
            'name', 'model_name', 'category', 'main_image', 'description',
            'price', 'stock', 'available'
        )

    def clean_category(self):
        category = Category.objects.filter(
            pk=int(self.cleaned_data['category'])
        ).first()
        return category

    def clean_slug(self):
        return slugify(self.name, allow_unicode=True)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Зображення')

    class Meta:
        Model = ProductImage
        fields = ('image', )


ImageFormSet = forms.modelformset_factory(
        ProductImage, form=ImageForm, extra=10
    )
