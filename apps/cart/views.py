# backend/apps/cart/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer
from apps.products.models import Product


class CartView(APIView):
    """
    GET  /api/cart/ — returns all cart items for logged-in user
    POST /api/cart/ — adds a product to cart

    Why APIView instead of ModelViewSet?
    The cart has custom logic that doesn't fit standard CRUD:
    - Adding an existing product increases quantity instead of
      creating a duplicate row (unique_together on the model)
    - The cart is always scoped to request.user — you never
      pass a user ID in the URL
    APIView gives us full control over this logic.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all cart items for the current user."""
        items = CartItem.objects.filter(
            user=request.user
        ).select_related('product', 'product__category')
        # select_related here fetches product AND product's category
        # in one query — prevents N+1 queries for each cart item

        serializer = CartItemSerializer(items, many=True)

        # Calculate cart summary totals
        cart_total = sum(item.item_total for item in items)
        item_count = sum(item.quantity for item in items)

        return Response({
            'items'     : serializer.data,
            'cart_total': cart_total,
            'item_count': item_count,
        })

    def post(self, request):
        """
        Add a product to cart.
        If product already in cart → increase quantity.
        If product not in cart → create new CartItem.
        """

        serializer = CartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product  = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        # Check stock before adding
        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} units available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get_or_create either fetches the existing CartItem
        # or creates a new one — prevents duplicate rows
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # Product already in cart — increase quantity
            new_quantity = cart_item.quantity + quantity

            # Check stock for the new combined quantity
            if product.stock < new_quantity:
                return Response(
                    {'error': f'Only {product.stock} units available.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED
        )


class CartItemView(APIView):
    """
    PUT    /api/cart/{id}/ — update quantity of one cart item
    DELETE /api/cart/{id}/ — remove one item from cart
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """
        Helper to fetch a CartItem that belongs to this user.
        Scoping by user means a customer can never modify
        another customer's cart items by guessing an ID.
        """
        try:
            return CartItem.objects.get(pk=pk, user=user)
        except CartItem.DoesNotExist:
            return None

    def put(self, request, pk):
        """Update quantity of a specific cart item."""
        cart_item = self.get_object(pk, request.user)
        if not cart_item:
            return Response(
                {'error': 'Cart item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get('quantity')
        if not quantity or int(quantity) < 1:
            return Response(
                {'error': 'Quantity must be at least 1.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = int(quantity)

        # Validate against current stock
        if cart_item.product.stock < quantity:
            return Response(
                {'error': f'Only {cart_item.product.stock} units available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

    def delete(self, request, pk):
        """Remove a specific item from the cart."""
        cart_item = self.get_object(pk, request.user)
        if not cart_item:
            return Response(
                {'error': 'Cart item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    """
    DELETE /api/cart/clear/ — removes ALL items from cart.
    Called automatically after a successful order is placed.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)