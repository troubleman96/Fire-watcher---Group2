"""
Serializers for Incidents App

This module contains DRF serializers for incident-related data.
Handles conversion between models and JSON for API responses.
"""

from rest_framework import serializers
from .models import Incident, StatusUpdate, IncidentPhoto
from apps.accounts.serializers import UserSerializer


class IncidentPhotoSerializer(serializers.ModelSerializer):
    """
    Serializer for incident photos.
    """
    
    class Meta:
        model = IncidentPhoto
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class StatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for status updates.
    Includes information about who made the update.
    """
    
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = StatusUpdate
        fields = ['id', 'status', 'updated_by', 'notes', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class IncidentListSerializer(serializers.ModelSerializer):
    """
    Serializer for incident list view.
    Includes basic information without nested relationships for performance.
    """
    
    class Meta:
        model = Incident
        fields = [
            'id',
            'reporter_name',
            'reporter_phone',
            'lat',
            'lng',
            'address',
            'description',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IncidentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for incident detail view.
    Includes nested relationships for photos and status updates.
    """
    
    reporter = UserSerializer(read_only=True)
    photos = IncidentPhotoSerializer(many=True, read_only=True)
    status_updates = StatusUpdateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'id',
            'reporter',
            'reporter_name',
            'reporter_phone',
            'lat',
            'lng',
            'address',
            'description',
            'status',
            'photos',
            'status_updates',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IncidentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new incidents.
    Handles photo uploads via multipart form data.
    """
    
    # Accept multiple photo uploads
    photos = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        help_text="List of photos to upload with the incident"
    )
    
    class Meta:
        model = Incident
        fields = [
            'reporter_name',
            'reporter_phone',
            'lat',
            'lng',
            'address',
            'description',
            'photos'
        ]
    
    def validate_lat(self, value):
        """Validate latitude is within valid range."""
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value
    
    def validate_lng(self, value):
        """Validate longitude is within valid range."""
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value


class IncidentStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating incident status.
    Used by fire team members to update incident progress.
    """
    
    status = serializers.ChoiceField(
        choices=Incident.STATUS_CHOICES,
        help_text="New status for the incident"
    )
    
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional notes about the status change"
    )
