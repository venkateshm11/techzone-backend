# backend/apps/users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Creates a new customer account.
    
    generics.CreateAPIView handles the boilerplate:
    - reads request.data
    - passes to serializer
    - calls serializer.save() if valid
    - returns 201 Created with the new object
    - returns 400 Bad Request with errors if invalid
    
    AllowAny because an unauthenticated user must be able to register.
    """

    queryset           = CustomUser.objects.all()
    serializer_class   = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens immediately after registration
        # so the user is logged in right after signing up
        refresh = RefreshToken.for_user(user)

        return Response({
            'user'   : UserProfileSerializer(user).data,
            'access' : str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Account created successfully.',
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/profile/ — returns current user's data
    PUT  /api/auth/profile/ — updates name and phone
    
    IsAuthenticated means the JWT token is required.
    Django reads the token from the Authorization header,
    decodes it, finds the user, and sets request.user automatically.
    """

    serializer_class   = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always return the currently logged-in user
        # Users can only see and edit their own profile
        return self.request.user