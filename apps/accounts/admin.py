"""
Django Admin Configuration for Accounts App

This module configures how the User model appears in the Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin
    
    Extends Django's UserAdmin to include custom fields in the admin interface.
    """
    
    # Fields to display in the list view
    list_display = [
        'email',
        'name',
        'user_type',
        'phone',
        'is_active',
        'created_at'
    ]
    
    # Fields to filter by
    list_filter = [
        'user_type',
        'is_active',
        'is_staff',
        'created_at'
    ]
    
    # Fields to search
    search_fields = [
        'email',
        'name',
        'phone',
        'badge_number'
    ]
    
    # Ordering
    ordering = ['-created_at']
    
    # Fieldsets for the detail view
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('name', 'phone', 'username')
        }),
        ('User Type & Role', {
            'fields': ('user_type', 'badge_number', 'fire_station')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at')
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'user_type'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'last_login', 'date_joined']
