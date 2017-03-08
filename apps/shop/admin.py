from django.contrib import admin

from .models import Category, Manufacturer, Product, ProductImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_name', 'slug', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    inlines = [ProductImageInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer)
admin.site.register(Product, ProductAdmin)
