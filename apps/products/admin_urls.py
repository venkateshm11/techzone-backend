# backend/apps/products/admin_urls.py

from django.urls import path
from .admin_views import (
    AdminStatsView,
    AdminProductListView,
    AdminProductDetailView,
    AdminOrderListView,
    AdminOrderUpdateView,
    AdminCategoryListView,
    AdminCategoryDetailView,
)

urlpatterns = [
    path('stats/',                          AdminStatsView.as_view(),           name='admin-stats'),
    path('products/',                       AdminProductListView.as_view(),     name='admin-products'),
    path('products/<int:pk>/',              AdminProductDetailView.as_view(),   name='admin-product-detail'),
    path('orders/',                         AdminOrderListView.as_view(),       name='admin-orders'),
    path('orders/<int:pk>/status/',         AdminOrderUpdateView.as_view(),     name='admin-order-status'),
    path('categories/',                     AdminCategoryListView.as_view(),    name='admin-categories'),
    path('categories/<slug:slug>/',         AdminCategoryDetailView.as_view(),  name='admin-category-detail'),
]