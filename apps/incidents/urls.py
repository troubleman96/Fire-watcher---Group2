"""
URL Configuration for Incidents App

Defines incident management and dashboard endpoints.
"""

from django.urls import path
from .views import (
    IncidentListCreateView,
    IncidentDetailView,
    IncidentStatusUpdateView,
    IncidentStatusHistoryView,
    DashboardStatsView,
)

urlpatterns = [
    # Incident endpoints
    path('', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('<uuid:id>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('<uuid:id>/status/', IncidentStatusUpdateView.as_view(), name='incident-status-update'),
    path('<uuid:id>/updates/', IncidentStatusHistoryView.as_view(), name='incident-status-history'),
]
