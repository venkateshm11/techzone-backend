# backend/apps/products/serializers.py

from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Used for:
    - Category navigation in React navbar
    - Category filter sidebar on products page
    - Dropdown when admin creates a product
    """

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Used for the products grid page — only fields needed for a card.
    Keeping this lean means faster API responses when listing 20+ products.

    discount_percent and is_in_stock come from @property methods
    on the Product model — SerializerMethodField reads them.
    """

    category_name    = serializers.CharField(source='category.name', read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock      = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'slug', 'price', 'compare_price',
            'discount_percent', 'image', 'brand', 'stock',
            'is_in_stock', 'is_featured', 'category_name',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Used for the single product page — all fields plus nested category object.

    Notice category is a nested CategorySerializer, not just an ID.
    This means the response includes the full category object:
    "category": {"id": 1, "name": "Mobile Phones", "slug": "mobile-phones"}
    instead of just: "category": 1
    """

    category         = CategorySerializer(read_only=True)
    category_id      = serializers.PrimaryKeyRelatedField(
                           queryset=Category.objects.all(),
                           source='category',
                           write_only=True
                       )
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock      = serializers.BooleanField(read_only=True)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_price',
            'discount_percent', 'stock', 'is_in_stock', 'sku', 'brand',
            'image', 'is_active', 'is_featured', 'category', 'category_id',
            'created_at', 'updated_at',
        ]