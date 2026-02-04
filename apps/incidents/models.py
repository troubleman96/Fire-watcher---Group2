"""
Models for Incidents App

This module defines the data models for fire incident reporting and management.
Includes models for:
- Incident: Core fire incident data
- StatusUpdate: Audit trail for incident status changes
- IncidentPhoto: Photos associated with incidents
"""

import uuid
from django.db import models
from django.conf import settings


class Incident(models.Model):
    """
    Incident Model
    
    Represents a fire incident report.
    Stores location, description, status, and reporter information.
    """
    
    # Status Choices
    STATUS_CHOICES = [
        ('new', 'New'),
        ('enroute', 'En Route'),
        ('arrived', 'Arrived'),
        ('fighting', 'Fighting Fire'),
        ('extinguished', 'Extinguished'),
        ('closed', 'Closed'),
    ]
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the incident"
    )
    
    # Reporter Information
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_incidents',
        help_text="User who reported the incident (null if anonymous)"
    )
    
    # Cached reporter info for quick access (in case reporter is anonymous or deleted)
    reporter_name = models.CharField(
        max_length=255,
        help_text="Name of the person who reported the incident"
    )
    
    reporter_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number of the reporter"
    )
    
    # Location Information
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude coordinate of the incident"
    )
    
    lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude coordinate of the incident"
    )
    
    address = models.TextField(
        help_text="Human-readable address of the incident"
    )
    
    # Incident Details
    description = models.TextField(
        help_text="Detailed description of the fire incident"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Current status of the incident"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the incident was reported"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the incident was last updated"
    )
    
    class Meta:
        verbose_name = 'Incident'
        verbose_name_plural = 'Incidents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        """String representation of the incident."""
        return f"Incident {self.id} - {self.status} - {self.address}"
    
    def is_active(self):
        """Check if incident is still active (not closed or extinguished)."""
        return self.status not in ['extinguished', 'closed']


class StatusUpdate(models.Model):
    """
    Status Update Model
    
    Represents a status change in an incident.
    Provides an audit trail of all status changes.
    """
    
    # Status Choices (same as Incident)
    STATUS_CHOICES = Incident.STATUS_CHOICES
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the status update"
    )
    
    # Related Incident
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name='status_updates',
        help_text="The incident this update belongs to"
    )
    
    # Status Information
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text="New status of the incident"
    )
    
    # Who made the update
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_updates',
        help_text="User who made this status update"
    )
    
    # Additional Notes
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes about the status change (e.g., 'Team Alpha dispatched')"
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When this status update was created"
    )
    
    class Meta:
        verbose_name = 'Status Update'
        verbose_name_plural = 'Status Updates'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        """String representation of the status update."""
        return f"{self.incident.id} - {self.status} at {self.timestamp}"


class IncidentPhoto(models.Model):
    """
    Incident Photo Model
    
    Represents a photo uploaded for an incident.
    Multiple photos can be associated with a single incident.
    """
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the photo"
    )
    
    # Related Incident
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="The incident this photo belongs to"
    )
    
    # Image File
    image = models.ImageField(
        upload_to='incident_photos/%Y/%m/%d/',
        help_text="Uploaded incident photo"
    )
    
    # Timestamp
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the photo was uploaded"
    )
    
    class Meta:
        verbose_name = 'Incident Photo'
        verbose_name_plural = 'Incident Photos'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        """String representation of the photo."""
        return f"Photo for {self.incident.id} - {self.uploaded_at}"
