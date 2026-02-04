"""
URL Configuration for Fire Watcher API

This file defines the main URL routing for the entire project.
It includes routes for:
- Django admin interface
- Authentication endpoints (via accounts app)
- Incident management endpoints (via incidents app)
- API documentation (future enhancement)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin - for backend management
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.accounts.urls')),  # Authentication endpoints
    path('api/incidents/', include('apps.incidents.urls')),  # Incident endpoints
    path('api/dashboard/', include('apps.incidents.urls_dashboard')),  # Dashboard endpoints
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
