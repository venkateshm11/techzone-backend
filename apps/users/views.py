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


class BootstrapSuperuserView(APIView):
    """
    POST /api/auth/bootstrap-superuser/
    
    Creates the first admin/superuser via frontend.
    Only works if NO admin user exists (safety check).
    
    This is useful for initial setup after deployment.
    Once an admin exists, this endpoint returns 403 Forbidden.
    
    Payload:
    {
        "email": "admin@example.com",
        "password": "strong-password",
        "first_name": "Admin",
        "last_name": "User"
    }
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Safety check: only allow if NO admins exist
        if CustomUser.objects.filter(role='ADMIN').exists():
            return Response(
                {'error': 'An admin account already exists. Cannot create another.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get data from request
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        
        # Validate required fields
        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already in use.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate password length
        if len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create superuser
            user = CustomUser.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='ADMIN'
            )
            
            # Generate JWT tokens so admin is logged in immediately
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Admin account created successfully!',
                'user': UserProfileSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error creating superuser: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )