# backend/apps/cart/urls.py

from django.urls import path
from .views import CartView, CartItemView, CartClearView

urlpatterns = [
    path('',        CartView.as_view(),      name='cart'),
    path('clear/',  CartClearView.as_view(),  name='cart-clear'),
    path('<int:pk>/', CartItemView.as_view(), name='cart-item'),
]