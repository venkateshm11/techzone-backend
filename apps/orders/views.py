# backend/apps/orders/views.py

import hmac
import hashlib
import razorpay
from django.conf import settings
from django.db import transaction
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from apps.cart.models import CartItem

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreateOrderView(APIView):
    """
    POST /api/orders/
    Creates an order from the customer's current cart.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(
            user=request.user
        ).select_related('product')

        if not cart_items.exists():
            return Response(
                {'error': 'Your cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity:
                return Response({
                    'error': f'Only {cart_item.product.stock} units of '
                             f'"{cart_item.product.name}" are available.'
                }, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user             = request.user,
                    total_amount     = total_amount,
                    shipping_address = serializer.validated_data['shipping_address'],
                    notes            = serializer.validated_data.get('notes', ''),
                    status           = 'PENDING',
                    payment_status   = 'PENDING',
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order             = order,
                        product           = cart_item.product,
                        quantity          = cart_item.quantity,
                        price_at_purchase = cart_item.product.price,
                    )
                    cart_item.product.stock -= cart_item.quantity
                    cart_item.product.save()

                razorpay_order = razorpay_client.order.create({
                    'amount'  : int(total_amount * 100),
                    'currency': 'INR',
                    'receipt' : f'order_{order.id}',
                })

                order.razorpay_order_id = razorpay_order['id']
                order.save()
                cart_items.delete()

            return Response({
                'order_id'         : order.id,
                'razorpay_order_id': order.razorpay_order_id,
                'amount'           : int(total_amount * 100),
                'currency'         : 'INR',
                'razorpay_key_id'  : settings.RAZORPAY_KEY_ID,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': 'Order creation failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPaymentView(APIView):
    """
    POST /api/orders/verify-payment/
    Cryptographically verifies Razorpay payment signature.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        razorpay_order_id   = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature  = request.data.get('razorpay_signature')

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return Response(
                {'error': 'Missing payment verification data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(
                razorpay_order_id=razorpay_order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        message = f'{razorpay_order_id}|{razorpay_payment_id}'
        generated_signature = hmac.new(
            key      = settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            msg      = message.encode('utf-8'),
            digestmod= hashlib.sha256
        ).hexdigest()

        if generated_signature != razorpay_signature:
            order.payment_status = 'FAILED'
            order.save()
            return Response(
                {'error': 'Payment verification failed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.payment_status      = 'PAID'
        order.status              = 'CONFIRMED'
        order.razorpay_payment_id = razorpay_payment_id
        order.save()

        return Response({
            'message' : 'Payment verified successfully.',
            'order_id': order.id,
        })


class OrderListView(generics.ListAPIView):
    """
    GET /api/orders/list/
    Returns all orders for the logged-in customer, newest first.
    """

    serializer_class   = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items', 'items__product')


class OrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/orders/{id}/
    Returns a single order with all items.
    Scoped to request.user — customers only see their own orders.
    """

    serializer_class   = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items', 'items__product')