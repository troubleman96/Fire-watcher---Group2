"""
Business Logic Services for Accounts App

This module contains the business logic for user-related operations.
Following clean architecture principles, services encapsulate business rules
and keep views thin and focused on HTTP concerns.
"""

from django.contrib.auth import authenticate
from django.db import transaction
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer


class UserService:
    """
    User Service
    
    Handles business logic for user operations including:
    - User registration
    - User authentication
    - Profile management
    """
    
    @staticmethod
    def register_user(data):
        """
        Register a new user.
        
        Args:
            data (dict): User registration data including email, password, name, etc.
        
        Returns:
            tuple: (user instance, errors dict or None)
        
        Example:
            user, errors = UserService.register_user({
                'email': 'john@example.com',
                'name': 'John Doe',
                'password': 'securepass123',
                'password_confirm': 'securepass123'
            })
        """
        serializer = UserRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            # Use transaction to ensure data integrity
            with transaction.atomic():
                user = serializer.save()
            return user, None
        else:
            return None, serializer.errors
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user with email and password.
        
        Args:
            email (str): User's email address
            password (str): User's password
        
        Returns:
            User or None: User instance if authentication successful, None otherwise
        
        Example:
            user = UserService.authenticate_user('john@example.com', 'password123')
        """
        user = authenticate(username=email, password=password)
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        
        Args:
            user_id (str/UUID): User's unique identifier
        
        Returns:
            User or None: User instance if found, None otherwise
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by their email address.
        
        Args:
            email (str): User's email address
        
        Returns:
            User or None: User instance if found, None otherwise
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def update_user_profile(user, data):
        """
        Update a user's profile information.
        
        Args:
            user (User): User instance to update
            data (dict): Updated profile data
        
        Returns:
            tuple: (updated user instance, errors dict or None)
        """
        from .serializers import UserUpdateSerializer
        
        serializer = UserUpdateSerializer(user, data=data, partial=True)
        
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
            return user, None
        else:
            return None, serializer.errors
    
    @staticmethod
    def get_fire_team_members():
        """
        Get all fire team members.
        
        Returns:
            QuerySet: All users with user_type='fire_team'
        """
        return User.objects.filter(user_type='fire_team')
    
    @staticmethod
    def is_fire_team_member(user):
        """
        Check if a user is a fire team member.
        
        Args:
            user (User): User instance to check
        
        Returns:
            bool: True if user is fire team member, False otherwise
        """
        return user.user_type == 'fire_team' if user else False
