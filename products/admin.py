from django.contrib import admin
from .models import Product, Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category_to_str', 'slug', 'j_publish', 'status', 'parts')
    list_filter = ('publish', 'author', 'status', 'category','color','technique')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
