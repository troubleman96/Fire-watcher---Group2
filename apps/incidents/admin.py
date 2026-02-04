"""
Django Admin Configuration for Incidents App

This module configures how incident models appear in the Django admin interface.
"""

from django.contrib import admin
from .models import Incident, StatusUpdate, IncidentPhoto


class StatusUpdateInline(admin.TabularInline):
    """
    Inline admin for status updates.
    Allows viewing and editing status updates directly from the incident page.
    """
    model = StatusUpdate
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['status', 'updated_by', 'notes', 'timestamp']


class IncidentPhotoInline(admin.TabularInline):
    """
    Inline admin for incident photos.
    Allows viewing and uploading photos directly from the incident page.
    """
    model = IncidentPhoto
    extra = 0
    readonly_fields = ['uploaded_at']
    fields = ['image', 'uploaded_at']


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Incident model.
    """
    
    # Inline models
    inlines = [StatusUpdateInline, IncidentPhotoInline]
    
    # List view configuration
    list_display = [
        'id',
        'reporter_name',
        'address',
        'status',
        'created_at',
        'updated_at'
    ]
    
    list_filter = [
        'status',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'reporter_name',
        'reporter_phone',
        'address',
        'description'
    ]
    
    ordering = ['-created_at']
    
    # Detail view configuration
    fieldsets = (
        ('Reporter Information', {
            'fields': ('reporter', 'reporter_name', 'reporter_phone')
        }),
        ('Location', {
            'fields': ('lat', 'lng', 'address')
        }),
        ('Incident Details', {
            'fields': ('description', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    """
    Admin configuration for StatusUpdate model.
    """
    
    list_display = [
        'incident',
        'status',
        'updated_by',
        'timestamp'
    ]
    
    list_filter = [
        'status',
        'timestamp'
    ]
    
    search_fields = [
        'incident__id',
        'notes'
    ]
    
    ordering = ['-timestamp']
    
    readonly_fields = ['timestamp']


@admin.register(IncidentPhoto)
class IncidentPhotoAdmin(admin.ModelAdmin):
    """
    Admin configuration for IncidentPhoto model.
    """
    
    list_display = [
        'id',
        'incident',
        'uploaded_at'
    ]
    
    list_filter = [
        'uploaded_at'
    ]
    
    search_fields = [
        'incident__id'
    ]
    
    ordering = ['-uploaded_at']
    
    readonly_fields = ['uploaded_at']
