from django import forms

from .models import Category, Manufacturer, Product, ProductImage
from . import utils


class CategoryForm(forms.ModelForm):
    parent_category = forms.ChoiceField(
        label='Батьківська категорія', choices=[])

    class Meta:
        model = Category
        fields = ('name', 'parent_category', 'image')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['parent_category'].choices = utils.cat_choices(categories)

    def clean_parent_category(self):
        if self.cleaned_data['parent_category']:
            return Category.objects.filter(
                pk=int(self.cleaned_data['parent_category'])).first()
        return None


class ManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ('name', 'image')


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категорія', choices=[])

    class Meta:
        model = Product
        fields = (
            'name', 'model_name', 'category', 'manufacturer', 'main_image',
            'description', 'price', 'stock', 'available',
        )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields['category'].choices = utils.cat_choices(categories)

    def clean_category(self):
        category = Category.objects.filter(
            pk=int(self.cleaned_data['category'])).first()
        return category


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Зображення')

    class Meta:
        Model = ProductImage
        fields = ('image', )


ImageFormSet = forms.modelformset_factory(
    ProductImage, form=ImageForm, extra=10
)
