# backend/apps/users/permissions.py

from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Only allows access to users with role='ADMIN'.
    Used on every admin-only endpoint.

    This is different from Django's built-in IsAdminUser which
    checks is_staff. We check our custom role field instead
    because that's what we set on our CustomUser model.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'ADMIN'
        )