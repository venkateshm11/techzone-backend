# backend/apps/orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Shows order items directly inside the order page in admin."""
    model  = OrderItem
    extra  = 0
    readonly_fields = ('product', 'quantity', 'price_at_purchase')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter   = ('status', 'payment_status')
    search_fields = ('user__email', 'razorpay_order_id')
    inlines       = [OrderItemInline]
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id')