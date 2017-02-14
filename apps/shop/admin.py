from django.contrib import admin

from .models import Category, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_name', 'slug', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    liat_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', 'model_name',)}
    inlines = [ProductImageInline,]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
