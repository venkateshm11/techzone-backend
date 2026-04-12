# backend/apps/orders/urls.py

from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, OrderListView, OrderDetailView

urlpatterns = [
    path('',               CreateOrderView.as_view(),  name='order-create'),
    path('list/',          OrderListView.as_view(),    name='order-list'),
    path('<int:pk>/',      OrderDetailView.as_view(),  name='order-detail'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
]