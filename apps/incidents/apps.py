"""
Incidents App Configuration

This app handles fire incident reporting and management for the Fire Watcher system.
"""

from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    """Configuration class for the incidents app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.incidents'
    verbose_name = 'Fire Incidents'
