# backend/apps/cart/models.py

from django.db import models
from django.conf import settings
from apps.products.models import Product


class CartItem(models.Model):
    """
    One product in a customer's cart.

    Cart is stored in the database, not localStorage — this means:
    - Cart persists across devices and browser sessions
    - Only logged-in users can have a cart
    - We can clear the cart server-side after order is placed
    """

    user       = models.ForeignKey(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.CASCADE,
                     related_name='cart_items'
                 )
    product    = models.ForeignKey(
                     Product,
                     on_delete=models.CASCADE,
                     related_name='cart_items'
                 )
    quantity   = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        # One user cannot have the same product twice — quantity is updated instead
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name} ({self.user.email})'

    @property
    def item_total(self):
        return self.product.price * self.quantity