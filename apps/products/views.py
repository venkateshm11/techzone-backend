# backend/apps/products/views.py

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset           = Category.objects.filter(is_active=True)
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field       = 'slug'
    pagination_class   = None  # ← returns a plain array, not paginated object

class ProductViewSet(viewsets.ModelViewSet):
    """
    Handles all product endpoints.

    Key features:
    - Uses slug in URL instead of id (SEO friendly)
    - Returns different serializers for list vs detail view
    - Supports search, filter by category/brand, and price range
    - featured/ custom action for homepage
    """

    permission_classes = [IsAdminOrReadOnly]
    lookup_field       = 'slug'
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'brand', 'description']
    ordering_fields    = ['price', 'created_at', 'name']
    ordering           = ['-created_at']

    def get_queryset(self):
        """
        This method builds the database query based on URL parameters.
        React sends filters as query params: /api/products/?category=mobile-phones&min_price=500
        """

        # Start with all active products
        queryset = Product.objects.filter(is_active=True).select_related('category')
        # select_related('category') fetches category data in the SAME database query
        # Without it, Django would run a separate query for each product's category
        # This is called the N+1 problem — select_related prevents it

        # Apply filters from query parameters
        category = self.request.query_params.get('category')
        brand    = self.request.query_params.get('brand')
        min_price= self.request.query_params.get('min_price')
        max_price= self.request.query_params.get('max_price')

        if category:
            queryset = queryset.filter(category__slug=category)

        if brand:
            queryset = queryset.filter(brand__icontains=brand)
            # icontains = case-insensitive contains — 'samsung' matches 'Samsung'

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_serializer_class(self):
        """
        Return different serializers for list vs detail.
        List page gets lightweight serializer (fewer fields).
        Detail page gets full serializer (all fields + nested category).
        """

        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """
        Custom endpoint: GET /api/products/featured/
        Returns products marked as is_featured=True.
        Used on the homepage hero/featured section.
        """

        featured_products = Product.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category')[:8]  # limit to 8

        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)