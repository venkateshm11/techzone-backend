# backend/apps/users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .views import RegisterView, ProfileView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Use our custom serializer that accepts email instead of username."""
    serializer_class = CustomTokenObtainPairSerializer


urlpatterns = [
    path('token/',         CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(),          name='token_refresh'),
    path('register/',      RegisterView.as_view(),              name='register'),
    path('profile/',       ProfileView.as_view(),               name='profile'),
]