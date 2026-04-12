# backend/apps/products/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - GET, HEAD, OPTIONS requests → allowed for everyone (even anonymous users)
    - POST, PUT, PATCH, DELETE requests → only allowed for admin users

    SAFE_METHODS is a tuple defined by DRF: ('GET', 'HEAD', 'OPTIONS')
    These are 'safe' because they don't change any data.
    """

    def has_permission(self, request, view):
        # Allow all read requests
        if request.method in SAFE_METHODS:
            return True

        # For write operations, user must be logged in AND be an admin
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )