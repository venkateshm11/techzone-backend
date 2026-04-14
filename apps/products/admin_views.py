# backend/apps/products/admin_views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone

from apps.users.permissions import IsAdminUser
from apps.orders.models import Order
from apps.cart.models import CartItem
from .models import Product, Category
from .serializers import ProductDetailSerializer, ProductListSerializer, CategorySerializer


class AdminStatsView(APIView):
    """
    GET /api/admin/stats/
    Returns dashboard statistics for the admin panel.
    All numbers are computed fresh on each request.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()

        # Orders placed today
        today_orders = Order.objects.filter(
            created_at__date=today
        )

        # Revenue today (only from paid orders)
        today_revenue = today_orders.filter(
            payment_status='PAID'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Total revenue all time
        total_revenue = Order.objects.filter(
            payment_status='PAID'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Order counts by status
        pending_orders   = Order.objects.filter(status='PENDING').count()
        confirmed_orders = Order.objects.filter(status='CONFIRMED').count()
        total_orders     = Order.objects.count()

        # Low stock products (5 or fewer units)
        low_stock = Product.objects.filter(
            is_active=True,
            stock__lte=5
        ).count()

        # Out of stock
        out_of_stock = Product.objects.filter(
            is_active=True,
            stock=0
        ).count()

        # Total active products
        total_products = Product.objects.filter(is_active=True).count()

        return Response({
            'today_orders'   : today_orders.count(),
            'today_revenue'  : today_revenue,
            'total_orders'   : total_orders,
            'total_revenue'  : total_revenue,
            'pending_orders' : pending_orders,
            'confirmed_orders': confirmed_orders,
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock,
            'total_products' : total_products,
        })


class AdminProductListView(APIView):
    """
    GET  /api/admin/products/ — all products including inactive
    POST /api/admin/products/ — create new product
    
    The key difference from the public product API:
    This returns ALL products regardless of is_active status.
    Admins need to see hidden products to manage them.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.all().select_related(
            'category'
        ).order_by('-created_at')

        # Filter by search query if provided
        search = request.query_params.get('search')
        if search:
            products = products.filter(name__icontains=search)

        # Filter by stock status
        stock_filter = request.query_params.get('stock')
        if stock_filter == 'low':
            products = products.filter(stock__lte=5, stock__gt=0)
        elif stock_filter == 'out':
            products = products.filter(stock=0)

        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminProductDetailView(APIView):
    """
    GET    /api/admin/products/{id}/ — get one product
    PUT    /api/admin/products/{id}/ — update product
    DELETE /api/admin/products/{id}/ — soft delete (sets is_active=False)
    """

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(ProductDetailSerializer(product).data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(
            product, data=request.data, partial=True
            # partial=True means not all fields are required
            # Admin can update just the price without sending
            # all other fields again
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Product not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        # Soft delete — never actually delete products
        # Deleting breaks order history (OrderItem references product)
        product.is_active = False
        product.save()
        return Response(
            {'message': f'"{product.name}" has been hidden.'},
            status=status.HTTP_200_OK
        )


class AdminOrderListView(APIView):
    """
    GET /api/admin/orders/
    Returns ALL orders across all customers.
    Filterable by status.
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        from apps.orders.models import Order
        from apps.orders.serializers import OrderSerializer

        orders = Order.objects.all().prefetch_related(
            'items', 'items__product'
        ).select_related('user').order_by('-created_at')

        # Filter by status
        status_filter = request.query_params.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderUpdateView(APIView):
    """
    PUT /api/admin/orders/{id}/status/
    Admin updates the status of an order.
    Only status field can be changed here — not payment.
    """

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        from apps.orders.models import Order
        from apps.orders.serializers import OrderSerializer

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')
        valid_statuses = ['PENDING', 'CONFIRMED', 'PACKED', 'SHIPPED', 'DELIVERED', 'CANCELLED']

        if not new_status or new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)


class AdminCategoryListView(APIView):
    """
    GET  /api/admin/categories/ — list all categories
    POST /api/admin/categories/ — create new category
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        """Get all categories including inactive ones"""
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new category"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCategoryDetailView(APIView):
    """
    GET    /api/admin/categories/{slug}/ — get one category
    PUT    /api/admin/categories/{slug}/ — update category
    DELETE /api/admin/categories/{slug}/ — delete category
    """

    permission_classes = [IsAdminUser]

    def get_object(self, slug):
        try:
            return Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, slug):
        category = self.get_object(slug)
        if not category:
            return Response(
                {'error': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(CategorySerializer(category).data)

    def put(self, request, slug):
        category = self.get_object(slug)
        if not category:
            return Response(
                {'error': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        category = self.get_object(slug)
        if not category:
            return Response(
                {'error': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response({'message': f'Category "{category.name}" deleted.'})
