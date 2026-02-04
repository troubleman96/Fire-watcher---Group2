"""
Business Logic Services for Incidents App

This module contains the business logic for incident-related operations.
Following clean architecture principles, services encapsulate business rules.
"""

from django.db import transaction
from django.db.models import Count, Q
from .models import Incident, StatusUpdate, IncidentPhoto
from .serializers import (
    IncidentCreateSerializer,
    IncidentDetailSerializer,
    IncidentListSerializer
)


class IncidentService:
    """
    Incident Service
    
    Handles business logic for incident operations including:
    - Creating incidents
    - Updating incident status
    - Retrieving incidents with filtering
    - Calculating statistics
    """
    
    @staticmethod
    def create_incident(data, user=None, photos=None):
        """
        Create a new fire incident.
        
        Args:
            data (dict): Incident data (location, description, etc.)
            user (User, optional): User reporting the incident
            photos (list, optional): List of photo files to attach
        
        Returns:
            tuple: (incident instance, errors dict or None)
        
        Example:
            incident, errors = IncidentService.create_incident({
                'lat': 40.7128,
                'lng': -74.0060,
                'address': '123 Main St',
                'description': 'Fire in building',
                'reporter_name': 'John Doe',
                'reporter_phone': '+1234567890'
            }, user=request.user, photos=request.FILES.getlist('photos'))
        """
        serializer = IncidentCreateSerializer(data=data)
        
        if serializer.is_valid():
            with transaction.atomic():
                # Create the incident
                incident = Incident.objects.create(
                    reporter=user,
                    reporter_name=data.get('reporter_name', user.name if user else 'Anonymous'),
                    reporter_phone=data.get('reporter_phone', user.phone if user else ''),
                    lat=serializer.validated_data['lat'],
                    lng=serializer.validated_data['lng'],
                    address=serializer.validated_data['address'],
                    description=serializer.validated_data['description'],
                    status='new'
                )
                
                # Create initial status update
                StatusUpdate.objects.create(
                    incident=incident,
                    status='new',
                    updated_by=user,
                    notes='Incident reported'
                )
                
                # Handle photo uploads
                if photos:
                    for photo in photos:
                        IncidentPhoto.objects.create(
                            incident=incident,
                            image=photo
                        )
            
            return incident, None
        else:
            return None, serializer.errors
    
    @staticmethod
    def update_incident_status(incident, status, user, notes=''):
        """
        Update the status of an incident.
        
        Args:
            incident (Incident): Incident to update
            status (str): New status
            user (User): User making the update
            notes (str, optional): Notes about the status change
        
        Returns:
            tuple: (updated incident, errors dict or None)
        """
        # Validate status
        valid_statuses = [choice[0] for choice in Incident.STATUS_CHOICES]
        if status not in valid_statuses:
            return None, {'status': f'Invalid status. Must be one of: {valid_statuses}'}
        
        with transaction.atomic():
            # Update incident status
            incident.status = status
            incident.save()
            
            # Create status update record
            StatusUpdate.objects.create(
                incident=incident,
                status=status,
                updated_by=user,
                notes=notes
            )
        
        return incident, None
    
    @staticmethod
    def get_incidents(filters=None, user=None):
        """
        Get incidents with optional filtering.
        
        Args:
            filters (dict, optional): Filter parameters (status, reporter_id)
            user (User, optional): Current user (for permission filtering)
        
        Returns:
            QuerySet: Filtered incidents
        
        Example:
            incidents = IncidentService.get_incidents(
                filters={'status': 'new'},
                user=request.user
            )
        """
        queryset = Incident.objects.all()
        
        if filters:
            # Filter by status
            if 'status' in filters:
                queryset = queryset.filter(status=filters['status'])
            
            # Filter by reporter (for public users to see their own reports)
            if 'reporter_id' in filters:
                queryset = queryset.filter(reporter_id=filters['reporter_id'])
        
        # If user is public, only show their own incidents
        if user and not user.is_fire_team() and not user.is_admin_user():
            queryset = queryset.filter(reporter=user)
        
        return queryset.select_related('reporter').prefetch_related('photos', 'status_updates')
    
    @staticmethod
    def get_incident_by_id(incident_id):
        """
        Get a single incident by ID.
        
        Args:
            incident_id (str/UUID): Incident ID
        
        Returns:
            Incident or None: Incident instance if found
        """
        try:
            return Incident.objects.select_related('reporter').prefetch_related(
                'photos',
                'status_updates__updated_by'
            ).get(id=incident_id)
        except Incident.DoesNotExist:
            return None
    
    @staticmethod
    def get_dashboard_stats():
        """
        Get dashboard statistics for fire team.
        
        Returns:
            dict: Statistics including counts by status
        
        Example:
            {
                'new': 5,
                'active': 7,  # enroute + arrived + fighting
                'resolved': 10,  # extinguished + closed
                'total': 22
            }
        """
        # Count incidents by status
        status_counts = Incident.objects.values('status').annotate(count=Count('id'))
        
        # Initialize counters
        stats = {
            'new': 0,
            'active': 0,
            'resolved': 0,
            'total': 0
        }
        
        # Aggregate counts
        for item in status_counts:
            status = item['status']
            count = item['count']
            
            if status == 'new':
                stats['new'] = count
            elif status in ['enroute', 'arrived', 'fighting']:
                stats['active'] += count
            elif status in ['extinguished', 'closed']:
                stats['resolved'] += count
            
            stats['total'] += count
        
        return stats
