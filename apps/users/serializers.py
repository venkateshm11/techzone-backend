# backend/apps/users/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    """
    Used when a customer creates a new account.
    
    password is write_only=True — this means:
    - It is accepted as input when creating a user
    - It is NEVER included in any response
    - You will never accidentally expose a password in an API response
    
    confirm_password only exists for validation — it is not a model field.
    We use it to check both passwords match, then discard it.
    """

    password         = serializers.CharField(
                           write_only=True,
                           validators=[validate_password]
                           # validate_password checks Django's password rules:
                           # min length 8, not too common, not all numeric
                       )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model  = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        """
        Object-level validation — runs after all individual fields are valid.
        We compare passwords here because we need access to both fields at once.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        """
        Remove confirm_password before saving — it's not a model field.
        Use create_user() not create() — create_user() hashes the password.
        If you use create(), the password is stored as plain text. Never do that.
        """
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Used to return user info after login and for the profile page.
    Never includes password — password field is not listed here.
    """

    class Meta:
        model  = CustomUser
        fields = ['id', 'name', 'email', 'phone', 'role', 'date_joined']
        read_only_fields = ['email', 'role', 'date_joined']
        # email and role cannot be changed via profile update


# Override simplejwt's default serializer to:
# 1. Accept 'email' instead of 'username'
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Override simplejwt's default serializer to:
    1. Accept 'email' instead of 'username'
    2. Return user data alongside the tokens
       so React has the user info immediately after login
    """

    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user info to the token response
        data['user'] = UserProfileSerializer(self.user).data
        return data