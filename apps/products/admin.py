# backend/apps/products/admin.py

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}  # auto-fills slug as you type name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'price', 'stock', 'is_active', 'is_featured')
    list_filter   = ('category', 'is_active', 'is_featured', 'brand')
    search_fields = ('name', 'sku', 'brand')
    prepopulated_fields = {'slug': ('name',)}