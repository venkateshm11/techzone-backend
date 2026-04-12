# backend/apps/cart/serializers.py

from rest_framework import serializers
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Returns cart item with full product details nested inside.

    product      → read only, returns full product object for display
    product_id   → write only, accepts product ID when adding to cart
    item_total   → read only, computed from model @property
    """

    product    = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
                     queryset=Product.objects.filter(is_active=True),
                     source='product',
                     write_only=True
                 )
    item_total = serializers.DecimalField(
                     max_digits=10,
                     decimal_places=2,
                     read_only=True
                 )

    class Meta:
        model  = CartItem
        fields = [
            'id', 'product', 'product_id',
            'quantity', 'item_total', 'created_at'
        ]