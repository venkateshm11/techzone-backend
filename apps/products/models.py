# backend/apps/products/models.py

from django.db import models


class Category(models.Model):
    """
    Represents a product category like 'Mobile Phones' or 'Laptop Accessories'.
    Products belong to a category. Categories appear in navigation and filters.
    """

    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image       = models.URLField(blank=True)   # Cloudinary URL — added later
    is_active   = models.BooleanField(default=True)

    class Meta:
        db_table        = 'categories'
        verbose_name_plural = 'Categories'
        ordering        = ['name']

    def __str__(self):
        return self.name
    

    # backend/apps/products/models.py  (continued — same file, paste below Category)

class Product(models.Model):
    """
    A product sold in the shop.

    Key decisions explained:
    - price is DecimalField NOT FloatField — floats have rounding errors with money
    - slug is used in URLs instead of id — better for SEO
    - is_active=False means hidden, not deleted — preserves order history
    - compare_price is the original MRP, price is the selling price
    """

    category     = models.ForeignKey(
                       Category,
                       on_delete=models.PROTECT,   # prevent deleting category that has products
                       related_name='products'
                   )
    name         = models.CharField(max_length=255)
    slug         = models.SlugField(unique=True, max_length=255)
    description  = models.TextField(blank=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price= models.DecimalField(max_digits=10, decimal_places=2,
                       null=True, blank=True)  # MRP — shown crossed out
    stock        = models.PositiveIntegerField(default=0)
    sku          = models.CharField(max_length=50, unique=True)
    brand        = models.CharField(max_length=100, blank=True)
    image        = models.URLField(blank=True)    # main Cloudinary image URL
    is_active    = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False)  # shown on homepage
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        """Returns discount % if compare_price exists and is higher than price."""
        if self.compare_price and self.compare_price > self.price:
            discount = ((self.compare_price - self.price) / self.compare_price) * 100
            return round(discount)
        return 0