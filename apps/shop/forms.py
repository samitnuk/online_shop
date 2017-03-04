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
            CATEGORIES_CHOICES.append([subcat.id, "*  {}".format(subcat.name)])
            if subcat.subcategories() is None:
                continue
            for subcat_ in subcat.subcategories():
                choice = [subcat_.id, "*** {}".format(subcat_.name)]
                CATEGORIES_CHOICES.append(choice)

    return CATEGORIES_CHOICES


class CategoryForm(forms.ModelForm):
    parent_category = forms.ChoiceField(
        label='Батьківська категорія', choices=categories_choices())

    class Meta:
        model = Category
        fields = ('name', 'parent_category', 'slug')
        widgets = {'slug': forms.HiddenInput()}

    def clean_parent_category(self):
        if self.cleaned_data['parent_category']:
            return Category.objects.filter(
                pk=int(self.cleaned_data['parent_category'])).first()
        return None

    def clean(self):
        cd = self.cleaned_data
        cd['slug'] = slugify(cd['name'], allow_unicode=True)
        return cd


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категорія',
                                 choices=categories_choices(),)

    class Meta:
        model = Product
        fields = (
            'name', 'model_name', 'category', 'main_image', 'description',
            'price', 'stock', 'available', 'slug',
        )
        widgets = {'slug': forms.HiddenInput(attrs={'value': 'temp_slug'})}

    def clean_category(self):
        category = Category.objects.filter(
            pk=int(self.cleaned_data['category'])).first()
        return category

    def clean(self):
        cd = self.cleaned_data
        cd['slug'] = slugify(self.cleaned_data['name'], allow_unicode=True)
        return cd


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Зображення')

    class Meta:
        Model = ProductImage
        fields = ('image', )


ImageFormSet = forms.modelformset_factory(
    ProductImage, form=ImageForm, extra=10
)
