"""
URL Configuration for Dashboard Endpoints

Defines dashboard-specific endpoints.
"""

from django.urls import path
from .views import DashboardStatsView

urlpatterns = [
    # Dashboard stats endpoint
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
