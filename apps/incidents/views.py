"""
API Views for Incidents App

This module contains DRF views for incident management.
Views handle HTTP requests/responses and delegate business logic to services.
"""

from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Incident, StatusUpdate
from .serializers import (
    IncidentListSerializer,
    IncidentDetailSerializer,
    IncidentStatusUpdateSerializer,
    StatusUpdateSerializer
)
from .services import IncidentService
from .permissions import IsFireTeamOrReadOnly, IsFireTeamOnly


class IncidentListCreateView(generics.ListCreateAPIView):
    """
    Incident List and Create Endpoint
    
    GET /api/incidents/
    - List all incidents (fire team sees all, public users see only their own)
    - Supports filtering by status
    - Supports pagination
    
    POST /api/incidents/
    - Create a new incident report
    - Supports photo uploads via multipart/form-data
    - Can be done anonymously or by authenticated users
    """
    
    serializer_class = IncidentListSerializer
    permission_classes = [IsFireTeamOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address', 'description', 'reporter_name']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Get incidents based on user permissions and filters.
        """
        # Get filter parameters
        filters = {}
        if self.request.query_params.get('status'):
            filters['status'] = self.request.query_params.get('status')
        
        # Get incidents using service
        return IncidentService.get_incidents(
            filters=filters,
            user=self.request.user if self.request.user.is_authenticated else None
        )
    
    def create(self, request, *args, **kwargs):
        """
        Create a new incident.
        
        Request Body (multipart/form-data or JSON):
            {
                "lat": 40.7128,
                "lng": -74.0060,
                "address": "123 Main St, New York, NY",
                "description": "Fire in building",
                "reporter_name": "John Doe",
                "reporter_phone": "+1234567890",
                "photos": [<file1>, <file2>]  // Optional
            }
        
        Response:
            201: Incident created successfully
            400: Validation errors
        """
        # Get photos from request
        photos = request.FILES.getlist('photos') if 'photos' in request.FILES else None
        
        # Create incident using service
        incident, errors = IncidentService.create_incident(
            data=request.data,
            user=request.user if request.user.is_authenticated else None,
            photos=photos
        )
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Return detailed incident data
        serializer = IncidentDetailSerializer(incident)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncidentDetailView(generics.RetrieveAPIView):
    """
    Incident Detail Endpoint
    
    GET /api/incidents/{id}/
    
    Retrieve detailed information about a specific incident.
    Includes photos and status update history.
    """
    
    serializer_class = IncidentDetailSerializer
    permission_classes = [IsFireTeamOrReadOnly]
    lookup_field = 'id'
    
    def get_queryset(self):
        """Get all incidents (permissions handled by permission class)."""
        return Incident.objects.all()


class IncidentStatusUpdateView(APIView):
    """
    Incident Status Update Endpoint
    
    PATCH /api/incidents/{id}/status/
    
    Update the status of an incident.
    Only fire team members and admins can update status.
    """
    
    permission_classes = [IsFireTeamOnly]
    
    def patch(self, request, id):
        """
        Update incident status.
        
        Request Body:
            {
                "status": "fighting",
                "notes": "Team Alpha dispatched and on scene"
            }
        
        Response:
            200: Status updated successfully
            400: Validation errors
            403: Permission denied
            404: Incident not found
        """
        # Get incident
        incident = IncidentService.get_incident_by_id(id)
        
        if not incident:
            return Response(
                {'error': 'Incident not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Validate request data
        serializer = IncidentStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status using service
        updated_incident, errors = IncidentService.update_incident_status(
            incident=incident,
            status=serializer.validated_data['status'],
            user=request.user,
            notes=serializer.validated_data.get('notes', '')
        )
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Return updated incident
        return Response(
            IncidentDetailSerializer(updated_incident).data,
            status=status.HTTP_200_OK
        )


class IncidentStatusHistoryView(generics.ListAPIView):
    """
    Incident Status History Endpoint
    
    GET /api/incidents/{id}/updates/
    
    Get the complete status update history for an incident.
    """
    
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get status updates for the specified incident."""
        incident_id = self.kwargs.get('id')
        return StatusUpdate.objects.filter(
            incident_id=incident_id
        ).select_related('updated_by').order_by('-timestamp')


class DashboardStatsView(APIView):
    """
    Dashboard Statistics Endpoint
    
    GET /api/dashboard/stats/
    
    Returns summary statistics for the fire team dashboard.
    Only accessible by fire team members and admins.
    """
    
    permission_classes = [IsFireTeamOnly]
    
    def get(self, request):
        """
        Get dashboard statistics.
        
        Response:
            {
                "new": 5,
                "active": 7,
                "resolved": 10,
                "total": 22
            }
        """
        stats = IncidentService.get_dashboard_stats()
        return Response(stats, status=status.HTTP_200_OK)
