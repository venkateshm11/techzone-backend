# backend/config/urls.py

import os
from pathlib import Path
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import FileResponse
from django.conf import settings

def serve_react_app(request, path=''):
    """
    Serve React app's index.html for all routes except API.
    This allows React Router to handle all frontend routing when page is refreshed.
    """
    # Try to find the React index.html in the frontend dist build
    react_index_path = Path(settings.BASE_DIR).parent / 'frontend' / 'dist' / 'index.html'
    
    if react_index_path.exists():
        with open(react_index_path, 'rb') as f:
            return FileResponse(f, content_type='text/html')
    
    # If no React build exists (development), return a message
    return FileResponse(
        open(os.devnull, 'rb'),
        status=503,
        content_type='text/plain'
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.products.urls')),
    path('api/auth/', include('apps.users.urls')),  
    path('api/cart/', include('apps.cart.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/admin/', include('apps.products.admin_urls')),  # Admin endpoints
]

# Serve React app for all non-API routes (SPA catch-all)
# Regex: (?!api|admin) = "don't match if starts with api or admin"
# MUST be last so API routes take priority
urlpatterns += [
    re_path(r'^(?!api|admin).*', serve_react_app, name='react-app'),
]