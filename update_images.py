import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

# Update product images with Unsplash URLs
updates = {
    'iphone-15-pro-max': 'https://images.unsplash.com/photo-1592286927505-1fed6c3d8117?w=400&h=400&fit=crop',
    'samsung-galaxy-s24-ultra': 'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=400&h=400&fit=crop',
    'oneplus-12': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
    'google-pixel-8-pro': 'https://images.unsplash.com/photo-1511336307830-e87b3b44e9e1?w=400&h=400&fit=crop',
    'xiaomi-14-ultra': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop',
    'macbook-pro-16-m3-max': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop',
    'dell-xps-15': 'https://images.unsplash.com/photo-1588872657840-790ff3bde4c5?w=400&h=400&fit=crop',
    'asus-vivobook-15': 'https://images.unsplash.com/photo-1602524206684-88c01e63a4a2?w=400&h=400&fit=crop',
    'hp-pavilion-15': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=400&fit=crop',
    'lenovo-thinkpad-x1': 'https://images.unsplash.com/photo-1529373377773-747fdf83b5b2?w=400&h=400&fit=crop',
    'ipad-pro-129-m2': 'https://images.unsplash.com/photo-1544716278-ca5e3af4abd8?w=400&h=400&fit=crop',
    'samsung-galaxy-tab-s9-ultra': 'https://images.unsplash.com/photo-1526045612212-70caf1dba33f?w=400&h=400&fit=crop',
    'ipad-air-11': 'https://images.unsplash.com/photo-1526045612212-70caf1dba33f?w=400&h=400&fit=crop',
    'apple-magsafe-charger': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop',
    'usb-c-fast-charger-65w': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop',
    'phone-screen-protector-pack-of-2': 'https://images.unsplash.com/photo-1609042231345-d0886f84c87e?w=400&h=400&fit=crop',
    'laptop-stand-aluminum': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f7?w=400&h=400&fit=crop',
    'sony-wh-1000xm5': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
    'apple-airpods-pro-2': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
    'bose-quietcomfort-45': 'https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=400&h=400&fit=crop',
    'jbl-tune-770nc': 'https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=400&h=400&fit=crop',
    'samsung-galaxy-buds2-pro': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
}

count = 0
for slug, image_url in updates.items():
    try:
        product = Product.objects.get(slug=slug)
        product.image = image_url
        product.save()
        print(f'✓ Updated: {product.name}')
        count += 1
    except Product.DoesNotExist:
        print(f'✗ Not found: {slug}')

print(f'\n✓ Updated {count} products with new images')
