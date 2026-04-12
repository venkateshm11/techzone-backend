# backend/apps/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display  = ('email', 'name', 'role', 'is_active', 'date_joined')
    list_filter   = ('role', 'is_active')
    search_fields = ('email', 'name')
    ordering      = ('-date_joined',)

    # These define what fields appear on the edit page in Django admin
    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal Info',{'fields': ('name', 'phone')}),
        ('Permissions',  {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
    )

    # Fields shown when creating a new user via Django admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email', 'name', 'password1', 'password2', 'role'),
        }),
    )