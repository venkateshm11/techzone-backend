# backend/apps/orders/serializers.py
# Replace the entire file with this updated version

from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductListSerializer


# Define the status order — used for the progress timeline in React
STATUS_STEPS = ['PENDING', 'CONFIRMED', 'PACKED', 'SHIPPED', 'DELIVERED']


class OrderItemSerializer(serializers.ModelSerializer):
    product    = ProductListSerializer(read_only=True)
    item_total = serializers.DecimalField(
                     max_digits=10,
                     decimal_places=2,
                     read_only=True
                 )

    class Meta:
        model  = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase', 'item_total']


class OrderSerializer(serializers.ModelSerializer):
    """
    Returns full order details including items and status progress.
    status_index tells React how far along the order is in the pipeline
    so it can highlight the correct step in the timeline.
    """

    items        = OrderItemSerializer(many=True, read_only=True)
    user_name    = serializers.CharField(source='user.name',  read_only=True)
    user_email   = serializers.CharField(source='user.email', read_only=True)
    status_index = serializers.SerializerMethodField()

    class Meta:
        model  = Order
        fields = [
            'id', 'user_name', 'user_email',
            'status', 'status_index', 'payment_status',
            'total_amount', 'shipping_address', 'notes',
            'razorpay_order_id', 'razorpay_payment_id',
            'items', 'created_at',
        ]
        read_only_fields = [
            'status', 'payment_status', 'total_amount',
            'razorpay_order_id', 'razorpay_payment_id', 'created_at',
        ]

    def get_status_index(self, obj):
        """
        Returns the position of the current status in STATUS_STEPS.
        PENDING=0, CONFIRMED=1, PACKED=2, SHIPPED=3, DELIVERED=4
        CANCELLED returns -1 — React uses this to show the cancelled state.
        """
        if obj.status == 'CANCELLED':
            return -1
        try:
            return STATUS_STEPS.index(obj.status)
        except ValueError:
            return 0


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.DictField()
    notes            = serializers.CharField(required=False, allow_blank=True)

    def validate_shipping_address(self, value):
        required = ['name', 'phone', 'street', 'city', 'state', 'pincode']
        missing  = [f for f in required if not value.get(f)]
        if missing:
            raise serializers.ValidationError(
                f"Missing address fields: {', '.join(missing)}"
            )
        return value