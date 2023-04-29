from django.contrib import admin
from django.utils.safestring import mark_safe

from store.models import Category, Product, Gallery


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_image', 'name', 'price', 'available', 'popular', 'bestseller', 'created', 'uploaded']
    list_editable = ['available', 'popular', 'bestseller']
    list_filter = ['name', 'price', 'available', 'popular', 'bestseller', 'created', 'uploaded']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [GalleryInline]
    fields = ['category', 'name', 'slug', 'description', 'image', 'preview', 'price', 'available', 'popular', 'bestseller', ]

    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}"  width="150">')

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}"  width="50">')

    get_image.short_description = "image"
