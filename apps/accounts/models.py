"""
Custom User Model for Fire Watcher

This module defines a custom user model that extends Django's AbstractUser.
It includes fields specific to the Fire Watcher application such as user type,
badge number for fire team members, and fire station assignment.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User Model
    
    Extends Django's AbstractUser to include additional fields needed
    for the Fire Watcher application. Supports three user types:
    - public: Regular citizens who can report fires
    - fire_team: Fire department personnel who respond to incidents
    - admin: System administrators
    """
    
    # User Type Choices
    USER_TYPE_CHOICES = [
        ('public', 'Public User'),
        ('fire_team', 'Fire Team Member'),
        ('admin', 'Administrator'),
    ]
    
    # Primary Key - using UUID for better security
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the user"
    )
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        help_text="Full name of the user"
    )
    
    email = models.EmailField(
        unique=True,
        help_text="Email address (used for login)"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    
    # User Type
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='public',
        help_text="Type of user account"
    )
    
    # Fire Team Specific Fields
    badge_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Badge number for fire team members"
    )
    
    fire_station = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Assigned fire station for fire team members"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the user account was created"
    )
    
    # Override username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the user."""
        return f"{self.name} ({self.email})"
    
    def is_fire_team(self):
        """Check if user is a fire team member."""
        return self.user_type == 'fire_team'
    
    def is_admin_user(self):
        """Check if user is an administrator."""
        return self.user_type == 'admin'
