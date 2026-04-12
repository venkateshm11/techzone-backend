# backend/apps/users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
    This manager tells Django how to create users for our CustomUser model.
    Django's default manager expects a 'username' field — ours uses 'email'.
    Without this manager, commands like createsuperuser would break.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)  # lowercases the domain part
        user = self.model(email=email, **extra_fields)
        user.set_password(password)          # hashes the password — never store plain text
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Superuser must have these fields set to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Our custom user model. Replaces Django's built-in User entirely.
    
    AbstractBaseUser gives us: password hashing, last_login tracking.
    PermissionsMixin gives us: is_superuser, groups, user_permissions
                               (needed for Django admin to work correctly).
    """

    ROLE_CHOICES = [
        ('USER', 'Customer'),
        ('ADMIN', 'Administrator'),
    ]

    email       = models.EmailField(unique=True)               # login field
    name        = models.CharField(max_length=150)
    phone       = models.CharField(max_length=15, blank=True)  # optional
    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    is_active   = models.BooleanField(default=True)            # False = account disabled
    is_staff    = models.BooleanField(default=False)           # True = can access Django admin
    date_joined = models.DateTimeField(auto_now_add=True)      # set once, never changed

    objects = CustomUserManager()  # connect our custom manager

    USERNAME_FIELD  = 'email'      # use email to log in instead of username
    REQUIRED_FIELDS = ['name']     # asked when running createsuperuser

    class Meta:
        db_table  = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.name} ({self.email})'

    @property
    def is_admin(self):
        """Convenience property — check this anywhere in the codebase."""
        return self.role == 'ADMIN'