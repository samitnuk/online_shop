from django import forms
from django.utils.text import slugify

from .models import Category, Manufacturer, Product, ProductImage
from . import utils


class CategoryForm(forms.ModelForm):
    parent_category = forms.ChoiceField(
        label='Батьківська категорія', choices=[])

    class Meta:
        model = Category
        fields = ('name', 'parent_category', 'image', 'slug')
        widgets = {'slug': forms.HiddenInput(attrs={'value': 'temp_slug'})}

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['parent_category'].choices = utils.cat_choices(categories)

    def clean_parent_category(self):
        if self.cleaned_data['parent_category']:
            return Category.objects.filter(
                pk=int(self.cleaned_data['parent_category'])).first()
        return None

    def clean(self):
        cd = self.cleaned_data
        cd['slug'] = slugify(cd['name'], allow_unicode=True)
        return cd


class ManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ('name', 'image', 'slug')
        widgets = {'slug': forms.HiddenInput(attrs={'value': 'temp_slug'})}

    def clean(self):
        cd = self.cleaned_data
        cd['slug'] = slugify(cd['name'], allow_unicode=True)
        return cd


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категорія', choices=[])

    class Meta:
        model = Product
        fields = (
            'name', 'model_name', 'category', 'manufacturer', 'main_image',
            'description', 'price', 'stock', 'available', 'slug',
        )
        widgets = {'slug': forms.HiddenInput(attrs={'value': 'temp_slug'})}

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = utils.cat_choices(categories)

    def clean_category(self):
        category = Category.objects.filter(
            pk=int(self.cleaned_data['category'])).first()
        return category

    def clean(self):
        cd = self.cleaned_data
        str_for_slug = '{}-{}'.format(cd['name'], cd['model_name'])
        cd['slug'] = slugify(str_for_slug, allow_unicode=True)
        return cd


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Зображення')

    class Meta:
        Model = ProductImage
        fields = ('image', )


ImageFormSet = forms.modelformset_factory(
    ProductImage, form=ImageForm, extra=10
)
