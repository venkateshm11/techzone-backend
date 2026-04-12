from django.core.management.base import BaseCommand
from apps.products.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Populate the database with sample products and categories'

    def handle(self, *args, **options):
        self.stdout.write('Starting product data population...')

        # Create Categories
        categories_data = [
            {
                'name': 'Smartphones',
                'slug': 'smartphones',
                'description': 'Latest smartphones and mobile phones',
                'image': 'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=400&h=400&fit=crop'
            },
            {
                'name': 'Laptops',
                'slug': 'laptops',
                'description': 'Laptops and notebooks for work and gaming',
                'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop'
            },
            {
                'name': 'Tablets',
                'slug': 'tablets',
                'description': 'Tablets and iPad devices',
                'image': 'https://images.unsplash.com/photo-1544716278-ca5e3af4abd8?w=400&h=400&fit=crop'
            },
            {
                'name': 'Accessories',
                'slug': 'accessories',
                'description': 'Phone and laptop accessories',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'
            },
            {
                'name': 'Headphones',
                'slug': 'headphones',
                'description': 'Headphones, earbuds, and audio devices',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'image': cat_data['image'],
                    'is_active': True
                }
            )
            categories[cat_data['slug']] = category
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f"  ✓ {cat_data['name']} - {status}")

        # Create Products
        products_data = [
            # Smartphones
            {
                'category': 'smartphones',
                'name': 'iPhone 15 Pro Max',
                'brand': 'Apple',
                'price': 139999,
                'compare_price': 149999,
                'stock': 25,
                'sku': 'IPHONE15PM-256',
                'description': 'Latest iPhone with A17 Pro chip, Pro camera system, and Dynamic Island.',
                'image': 'https://images.unsplash.com/photo-1592286927505-1fed6c3d8117?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'smartphones',
                'name': 'Samsung Galaxy S24 Ultra',
                'brand': 'Samsung',
                'price': 129999,
                'compare_price': 139999,
                'stock': 18,
                'sku': 'SAMS24U-512',
                'description': 'Flagship Galaxy phone with advanced AI features and 200MP camera.',
                'image': 'https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'smartphones',
                'name': 'OnePlus 12',
                'brand': 'OnePlus',
                'price': 64999,
                'compare_price': 74999,
                'stock': 42,
                'sku': 'ONEPLUS12-256',
                'description': 'Fast, smooth, and powerful Android flagship.',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'smartphones',
                'name': 'Google Pixel 8 Pro',
                'brand': 'Google',
                'price': 89999,
                'compare_price': 99999,
                'stock': 15,
                'sku': 'PIXEL8P-256',
                'description': 'Google\'s flagship with Tensor chip and advanced photography.',
                'image': 'https://images.unsplash.com/photo-1511336307830-e87b3b44e9e1?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'smartphones',
                'name': 'Xiaomi 14 Ultra',
                'brand': 'Xiaomi',
                'price': 79999,
                'compare_price': 89999,
                'stock': 30,
                'sku': 'XIAOMI14U-512',
                'description': 'Premium Xiaomi with Leica camera and stunning display.',
                'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop',
                'is_featured': False
            },

            # Laptops
            {
                'category': 'laptops',
                'name': 'MacBook Pro 16" M3 Max',
                'brand': 'Apple',
                'price': 239999,
                'compare_price': 259999,
                'stock': 12,
                'sku': 'MBP16M3-512',
                'description': 'Powerful laptop for professionals with 16-inch Retina display.',
                'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'laptops',
                'name': 'Dell XPS 15',
                'brand': 'Dell',
                'price': 149999,
                'compare_price': 169999,
                'stock': 8,
                'sku': 'DXPS15-512',
                'description': 'Premium Windows laptop with OLED display and Core i9.',
                'image': 'https://images.unsplash.com/photo-1588872657840-790ff3bde4c5?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'laptops',
                'name': 'ASUS VivoBook 15',
                'brand': 'ASUS',
                'price': 54999,
                'compare_price': 64999,
                'stock': 35,
                'sku': 'ASVB15-256',
                'description': 'Budget-friendly laptop for everyday computing.',
                'image': 'https://images.unsplash.com/photo-1602524206684-88c01e63a4a2?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'laptops',
                'name': 'HP Pavilion 15',
                'brand': 'HP',
                'price': 59999,
                'compare_price': 69999,
                'stock': 22,
                'sku': 'HPPAV15-256',
                'description': 'Reliable laptop with good battery life and performance.',
                'image': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'laptops',
                'name': 'Lenovo ThinkPad X1',
                'brand': 'Lenovo',
                'price': 119999,
                'compare_price': 134999,
                'stock': 10,
                'sku': 'LENX1-512',
                'description': 'Business laptop with excellent keyboard and build quality.',
                'image': 'https://images.unsplash.com/photo-1529373377773-747fdf83b5b2?w=400&h=400&fit=crop',
                'is_featured': False
            },

            # Tablets
            {
                'category': 'tablets',
                'name': 'iPad Pro 12.9" M2',
                'brand': 'Apple',
                'price': 119999,
                'compare_price': 129999,
                'stock': 14,
                'sku': 'IPADPM2-256',
                'description': 'Powerful tablet with M2 chip and ProMotion display.',
                'image': 'https://images.unsplash.com/photo-1544716278-ca5e3af4abd8?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'tablets',
                'name': 'Samsung Galaxy Tab S9 Ultra',
                'brand': 'Samsung',
                'price': 89999,
                'compare_price': 99999,
                'stock': 20,
                'sku': 'SGTABS9U-256',
                'description': 'Premium tablet with AMOLED display and S Pen.',
                'image': 'https://images.unsplash.com/photo-1526045612212-70caf1dba33f?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'tablets',
                'name': 'iPad Air 11"',
                'brand': 'Apple',
                'price': 79999,
                'compare_price': 89999,
                'stock': 18,
                'sku': 'IPADA11-256',
                'description': 'Best-selling tablet with M2 chip and bright display.',
                'image': 'https://images.unsplash.com/photo-1526045612212-70caf1dba33f?w=400&h=400&fit=crop',
                'is_featured': False
            },

            # Accessories
            {
                'category': 'accessories',
                'name': 'Apple MagSafe Charger',
                'brand': 'Apple',
                'price': 3999,
                'compare_price': 4999,
                'stock': 150,
                'sku': 'APPLMAG-001',
                'description': 'Official Apple MagSafe charging cable.',
                'image': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'accessories',
                'name': 'USB-C Fast Charger 65W',
                'brand': 'Anker',
                'price': 2499,
                'compare_price': 3499,
                'stock': 200,
                'sku': 'ANKERUSC65-001',
                'description': 'Fast charging adapter for all USB-C devices.',
                'image': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'accessories',
                'name': 'Phone Screen Protector (Pack of 2)',
                'brand': 'Spigen',
                'price': 799,
                'compare_price': 1299,
                'stock': 300,
                'sku': 'SPIGEN-SP-001',
                'description': 'Tempered glass screen protectors for smartphones.',
                'image': 'https://images.unsplash.com/photo-1609042231345-d0886f84c87e?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'accessories',
                'name': 'Laptop Stand Aluminum',
                'brand': 'Rain Design',
                'price': 4999,
                'compare_price': 5999,
                'stock': 80,
                'sku': 'RAINLS-ALU-001',
                'description': 'Premium aluminum laptop stand for better ergonomics.',
                'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b3f7?w=400&h=400&fit=crop',
                'is_featured': False
            },

            # Headphones
            {
                'category': 'headphones',
                'name': 'Sony WH-1000XM5',
                'brand': 'Sony',
                'price': 29999,
                'compare_price': 34999,
                'stock': 45,
                'sku': 'SONYWH1KXM5-001',
                'description': 'Best noise-cancelling wireless headphones with 30-hour battery.',
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'headphones',
                'name': 'Apple AirPods Pro 2',
                'brand': 'Apple',
                'price': 27999,
                'compare_price': 29999,
                'stock': 60,
                'sku': 'APPLAIRS2-001',
                'description': 'True wireless earbuds with active noise cancellation.',
                'image': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
                'is_featured': True
            },
            {
                'category': 'headphones',
                'name': 'Bose QuietComfort 45',
                'brand': 'Bose',
                'price': 34999,
                'compare_price': 39999,
                'stock': 25,
                'sku': 'BOSEQUC45-001',
                'description': 'Legendary comfort with world-class noise cancellation.',
                'image': 'https://images.unsplash.com/photo-1487215078519-e21cc028cb29?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'headphones',
                'name': 'JBL Tune 770NC',
                'brand': 'JBL',
                'price': 14999,
                'compare_price': 17999,
                'stock': 70,
                'sku': 'JBLTN770-001',
                'description': 'Affordable wireless headphones with noise cancellation.',
                'image': 'https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=400&h=400&fit=crop',
                'is_featured': False
            },
            {
                'category': 'headphones',
                'name': 'Samsung Galaxy Buds2 Pro',
                'brand': 'Samsung',
                'price': 15999,
                'compare_price': 19999,
                'stock': 55,
                'sku': 'SAMGB2P-001',
                'description': 'Premium earbuds with intelligent ANC and Hi-Fi sound.',
                'image': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
                'is_featured': False
            },
        ]

        created_count = 0
        for prod_data in products_data:
            category_slug = prod_data.pop('category')
            category = categories[category_slug]
            
            slug = slugify(prod_data['name'])
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    **prod_data,
                    'category': category
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"  ✓ {product.name}")

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {created_count} products!'))
