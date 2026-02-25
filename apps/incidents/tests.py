"""
Tests for Incidents App

This module contains comprehensive tests for incident management.
Tests cover:
- Incident creation (with and without photos)
- Incident listing and filtering
- Status updates
- Permission checks
- Dashboard statistics
"""

from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.incidents.models import Incident, StatusUpdate, IncidentPhoto
from decimal import Decimal


class IncidentCreationTests(TestCase):
    """Test suite for incident creation."""
    
    def setUp(self):
        """Set up test client and users."""
        self.client = APIClient()
        self.incidents_url = reverse('incident-list-create')
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            name='Test User',
            password='testpass123',
            phone='+1234567890',
            user_type='public'
        )
    
    def test_create_incident_authenticated_success(self):
        """Test creating incident as authenticated user."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'lat': '40.712800',
            'lng': '-74.006000',
            'address': '123 Main St, New York, NY',
            'description': 'Fire in building',
            'reporter_name': 'Test User',
            'reporter_phone': '+1234567890'
        }
        
        response = self.client.post(self.incidents_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['address'], '123 Main St, New York, NY')
        self.assertEqual(response.data['status'], 'new')
        self.assertIsNotNone(response.data['reporter'])
        
        # Verify incident was created
        self.assertEqual(Incident.objects.count(), 1)
        incident = Incident.objects.first()
        self.assertEqual(incident.reporter, self.user)
        self.assertEqual(incident.status, 'new')
        
        # Verify initial status update was created
        self.assertEqual(StatusUpdate.objects.count(), 1)
        status_update = StatusUpdate.objects.first()
        self.assertEqual(status_update.status, 'new')
        self.assertEqual(status_update.notes, 'Incident reported')
    
    def test_create_incident_anonymous_success(self):
        """Test creating incident without authentication (anonymous)."""
        data = {
            'lat': '40.712800',
            'lng': '-74.006000',
            'address': '456 Oak Ave, New York, NY',
            'description': 'Large fire with smoke',
            'reporter_name': 'Anonymous Reporter',
            'reporter_phone': '+9876543210'
        }
        
        response = self.client.post(self.incidents_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['reporter'])
        
        # Verify incident was created
        incident = Incident.objects.first()
        self.assertIsNone(incident.reporter)
        self.assertEqual(incident.reporter_name, 'Anonymous Reporter')
    
    def test_create_incident_invalid_coordinates(self):
        """Test incident creation fails with invalid coordinates."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'lat': '999.999999',  # Invalid latitude
            'lng': '-74.006000',
            'address': '123 Main St',
            'description': 'Fire',
            'reporter_name': 'Test User'
        }
        
        response = self.client.post(self.incidents_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_incident_missing_required_fields(self):
        """Test incident creation fails when required fields are missing."""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'lat': '40.712800',
            # Missing lng, address, description
        }
        
        response = self.client.post(self.incidents_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IncidentListingTests(TestCase):
    """Test suite for incident listing and filtering."""
    
    def setUp(self):
        """Set up test client, users, and incidents."""
        self.client = APIClient()
        self.incidents_url = reverse('incident-list-create')
        
        # Create public user
        self.public_user = User.objects.create_user(
            username='public',
            email='public@example.com',
            name='Public User',
            password='testpass123',
            user_type='public'
        )
        
        # Create fire team user
        self.fire_team_user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team'
        )
        
        # Create incidents
        self.incident1 = Incident.objects.create(
            reporter=self.public_user,
            reporter_name='Public User',
            reporter_phone='+1234567890',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='123 Main St',
            description='Fire 1',
            status='new'
        )
        
        self.incident2 = Incident.objects.create(
            reporter=self.public_user,
            reporter_name='Public User',
            reporter_phone='+1234567890',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='456 Oak Ave',
            description='Fire 2',
            status='fighting'
        )
        
        self.incident3 = Incident.objects.create(
            reporter=None,
            reporter_name='Anonymous',
            reporter_phone='+9876543210',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='789 Pine St',
            description='Fire 3',
            status='extinguished'
        )
    
    def test_list_incidents_fire_team_sees_all(self):
        """Test fire team members can see all incidents."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        response = self.client.get(self.incidents_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
    
    def test_list_incidents_public_sees_own_only(self):
        """Test public users only see their own incidents."""
        self.client.force_authenticate(user=self.public_user)
        
        response = self.client.get(self.incidents_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Only their 2 incidents
    
    def test_list_incidents_filter_by_status(self):
        """Test filtering incidents by status."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        response = self.client.get(f'{self.incidents_url}?status=new')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['status'], 'new')
    
    def test_list_incidents_search(self):
        """Test searching incidents."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        response = self.client.get(f'{self.incidents_url}?search=Main')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIn('Main', response.data['results'][0]['address'])
    
    def test_list_incidents_unauthenticated_fails(self):
        """Test listing incidents requires authentication."""
        response = self.client.get(self.incidents_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class IncidentDetailTests(TestCase):
    """Test suite for incident detail retrieval."""
    
    def setUp(self):
        """Set up test client, users, and incident."""
        self.client = APIClient()
        
        # Create users
        self.public_user = User.objects.create_user(
            username='public',
            email='public@example.com',
            name='Public User',
            password='testpass123',
            user_type='public'
        )
        
        self.fire_team_user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team'
        )
        
        # Create incident
        self.incident = Incident.objects.create(
            reporter=self.public_user,
            reporter_name='Public User',
            reporter_phone='+1234567890',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='123 Main St',
            description='Test Fire',
            status='new'
        )
        
        self.detail_url = reverse('incident-detail', kwargs={'id': self.incident.id})
    
    def test_get_incident_detail_success(self):
        """Test retrieving incident details."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], '123 Main St')
        self.assertIn('photos', response.data)
        self.assertIn('status_updates', response.data)
    
    def test_get_incident_detail_not_found(self):
        """Test retrieving nonexistent incident returns 404."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        import uuid
        fake_id = uuid.uuid4()
        url = reverse('incident-detail', kwargs={'id': fake_id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class IncidentStatusUpdateTests(TestCase):
    """Test suite for incident status updates."""
    
    def setUp(self):
        """Set up test client, users, and incident."""
        self.client = APIClient()
        
        # Create users
        self.public_user = User.objects.create_user(
            username='public',
            email='public@example.com',
            name='Public User',
            password='testpass123',
            user_type='public'
        )
        
        self.fire_team_user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team'
        )
        
        # Create incident
        self.incident = Incident.objects.create(
            reporter=self.public_user,
            reporter_name='Public User',
            reporter_phone='+1234567890',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='123 Main St',
            description='Test Fire',
            status='new'
        )
        
        self.status_url = reverse('incident-status-update', kwargs={'id': self.incident.id})
    
    def test_update_status_fire_team_success(self):
        """Test fire team can update incident status."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        data = {
            'status': 'fighting',
            'notes': 'Team on scene'
        }
        
        response = self.client.patch(self.status_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'fighting')
        
        # Verify database was updated
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'fighting')
        
        # Verify status update was created
        status_update = StatusUpdate.objects.filter(
            incident=self.incident,
            status='fighting'
        ).first()
        self.assertIsNotNone(status_update)
        self.assertEqual(status_update.notes, 'Team on scene')
    
    def test_update_status_public_user_forbidden(self):
        """Test public users cannot update incident status."""
        self.client.force_authenticate(user=self.public_user)
        
        data = {
            'status': 'fighting',
            'notes': 'Trying to update'
        }
        
        response = self.client.patch(self.status_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_status_invalid_status(self):
        """Test updating with invalid status fails."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        data = {
            'status': 'invalid_status',
            'notes': 'Test'
        }
        
        response = self.client.patch(self.status_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StatusHistoryTests(TestCase):
    """Test suite for incident status history."""
    
    def setUp(self):
        """Set up test client, users, and incident with history."""
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team'
        )
        
        # Create incident
        self.incident = Incident.objects.create(
            reporter=self.user,
            reporter_name='Fire Team',
            reporter_phone='+1234567890',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='123 Main St',
            description='Test Fire',
            status='fighting'
        )
        
        # Create status updates
        StatusUpdate.objects.create(
            incident=self.incident,
            status='new',
            updated_by=self.user,
            notes='Reported'
        )
        StatusUpdate.objects.create(
            incident=self.incident,
            status='enroute',
            updated_by=self.user,
            notes='Team dispatched'
        )
        StatusUpdate.objects.create(
            incident=self.incident,
            status='fighting',
            updated_by=self.user,
            notes='On scene'
        )
        
        self.history_url = reverse('incident-status-history', kwargs={'id': self.incident.id})
    
    def test_get_status_history_success(self):
        """Test retrieving incident status history."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.history_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should have 3 manual updates
        self.assertGreaterEqual(len(response.data), 3)


class DashboardStatsTests(TestCase):
    """Test suite for dashboard statistics."""
    
    def setUp(self):
        """Set up test client, users, and incidents."""
        self.client = APIClient()
        self.stats_url = reverse('dashboard-stats')
        
        # Create users
        self.public_user = User.objects.create_user(
            username='public',
            email='public@example.com',
            name='Public User',
            password='testpass123',
            user_type='public'
        )
        
        self.fire_team_user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team'
        )
        
        # Create incidents with different statuses
        Incident.objects.create(
            reporter=self.public_user,
            reporter_name='User',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='Address 1',
            description='Fire 1',
            status='new'
        )
        Incident.objects.create(
            reporter=self.public_user,
            reporter_name='User',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='Address 2',
            description='Fire 2',
            status='new'
        )
        Incident.objects.create(
            reporter=self.public_user,
            reporter_name='User',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='Address 3',
            description='Fire 3',
            status='fighting'
        )
        Incident.objects.create(
            reporter=self.public_user,
            reporter_name='User',
            lat=Decimal('40.712800'),
            lng=Decimal('-74.006000'),
            address='Address 4',
            description='Fire 4',
            status='extinguished'
        )
    
    def test_get_stats_fire_team_success(self):
        """Test fire team can access dashboard stats."""
        self.client.force_authenticate(user=self.fire_team_user)
        
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['new'], 2)
        self.assertEqual(response.data['active'], 1)  # fighting
        self.assertEqual(response.data['resolved'], 1)  # extinguished
        self.assertEqual(response.data['total'], 4)
    
    def test_get_stats_public_user_forbidden(self):
        """Test public users cannot access dashboard stats."""
        self.client.force_authenticate(user=self.public_user)
        
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_stats_unauthenticated_forbidden(self):
        """Test unauthenticated users cannot access dashboard stats."""
        response = self.client.get(self.stats_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
