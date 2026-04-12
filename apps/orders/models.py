# backend/apps/orders/models.py

from django.db import models
from django.conf import settings
from apps.products.models import Product


class Order(models.Model):
    """
    One order placed by a customer.

    Key decisions:
    - shipping_address is JSONField (snapshot) — if a customer changes their
      address later, old orders still show the correct delivery address
    - razorpay fields store IDs from Razorpay for payment reconciliation
    - user is PROTECT not CASCADE — you cannot delete a user with order history
    """

    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PACKED',    'Packed'),
        ('SHIPPED',   'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING',  'Pending'),
        ('PAID',     'Paid'),
        ('FAILED',   'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    user                = models.ForeignKey(
                              settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT,
                              related_name='orders'
                          )
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='PENDING')
    payment_status      = models.CharField(max_length=20,
                              choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    total_amount        = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address    = models.JSONField()         # snapshot of address at order time
    notes               = models.TextField(blank=True)
    razorpay_order_id   = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} by {self.user.name}'


class OrderItem(models.Model):
    """
    One product line inside an order.

    price_at_purchase stores what the customer actually paid.
    Never recalculate from product.price — that price may have changed.
    """

    order            = models.ForeignKey(Order, on_delete=models.CASCADE,
                           related_name='items')
    product          = models.ForeignKey(Product, on_delete=models.PROTECT,
                           related_name='order_items')
    quantity         = models.PositiveIntegerField()
    price_at_purchase= models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def item_total(self):
        return self.price_at_purchase * self.quantity