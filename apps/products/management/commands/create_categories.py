# backend/apps/products/management/commands/create_categories.py

from django.core.management.base import BaseCommand
from apps.products.models import Category


class Command(BaseCommand):
    help = 'Create default product categories'

    def handle(self, *args, **options):
        categories_data = [
            {'name': 'Mobiles', 'slug': 'mobiles', 'description': 'Latest smartphones and mobile phones'},
            {'name': 'Laptops', 'slug': 'laptops', 'description': 'Computers and laptops for work and gaming'},
            {'name': 'Accessories', 'slug': 'accessories', 'description': 'Phone and tech accessories'},
            {'name': 'Headphones', 'slug': 'headphones', 'description': 'Wireless and wired headphones and earbuds'},
            {'name': 'Tablets', 'slug': 'tablets', 'description': 'Tablet computers and iPad devices'},
            {'name': 'Monitors', 'slug': 'monitors', 'description': 'Display monitors and LED screens'},
            {'name': 'Speakers', 'slug': 'speakers', 'description': 'Bluetooth and wired speakers'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        self.stdout.write(self.style.SUCCESS('Category creation completed!'))
