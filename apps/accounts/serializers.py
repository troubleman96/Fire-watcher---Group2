"""
Serializers for Accounts App

This module contains DRF serializers for user-related data.
Serializers handle the conversion between complex data types (like Django models)
and Python datatypes that can be easily rendered into JSON.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    
    Serializes user data for API responses.
    Excludes sensitive information like password.
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'phone',
            'user_type',
            'badge_number',
            'fire_station',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User Registration Serializer
    
    Handles user registration with password validation.
    Creates a new user account with hashed password.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="User password (will be hashed)"
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Password confirmation"
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'phone',
            'password',
            'password_confirm',
            'user_type',
            'badge_number',
            'fire_station',
        ]
    
    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def validate_user_type(self, value):
        """
        Validate user type.
        Only allow 'public' type during self-registration.
        Fire team and admin accounts should be created by admins.
        """
        if value not in ['public', 'fire_team', 'admin']:
            raise serializers.ValidationError("Invalid user type.")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new user with hashed password.
        """
        # Remove password_confirm as it's not needed for user creation
        validated_data.pop('password_confirm')
        
        # Extract password
        password = validated_data.pop('password')
        
        # Set username to email if not provided
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        
        # Create user instance
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    User Update Serializer
    
    Allows users to update their profile information.
    Excludes sensitive fields like user_type which should only be changed by admins.
    """
    
    class Meta:
        model = User
        fields = [
            'name',
            'phone',
        ]
