"""
Custom Permissions for Incidents App

This module defines custom permission classes for incident management.
"""

from rest_framework import permissions


class IsFireTeamOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow fire team members to edit incidents.
    Public users can view their own incidents.
    """
    
    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        """
        # Allow unauthenticated users to create incidents (anonymous reporting)
        if request.method == 'POST':
            return True
        
        # Require authentication for other methods
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access a specific incident.
        """
        # Fire team and admins can do anything
        if request.user.is_fire_team() or request.user.is_admin_user():
            return True
        
        # Public users can only view their own incidents
        if request.method in permissions.SAFE_METHODS:
            return obj.reporter == request.user
        
        return False


class IsFireTeamOnly(permissions.BasePermission):
    """
    Permission class that only allows fire team members and admins.
    """
    
    def has_permission(self, request, view):
        """
        Check if user is fire team or admin.
        """
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_fire_team() or request.user.is_admin_user())
        )
