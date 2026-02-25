"""
Tests for Accounts App

This module contains comprehensive tests for user authentication and management.
Tests cover:
- User registration
- Login/logout
- Token refresh
- Profile management
- Permission checks
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User


class UserRegistrationTests(TestCase):
    """Test suite for user registration."""
    
    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.register_url = reverse('register')
    
    def test_register_public_user_success(self):
        """Test successful registration of a public user."""
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'phone': '+1234567890',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'user_type': 'public'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')
        self.assertEqual(response.data['user']['user_type'], 'public')
        
        # Verify user was created in database
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
    
    def test_register_fire_team_member_success(self):
        """Test successful registration of a fire team member."""
        data = {
            'email': 'fireteam@example.com',
            'name': 'Fire Team Alpha',
            'phone': '+1234567890',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'user_type': 'fire_team',
            'badge_number': 'FT001',
            'fire_station': 'Station 1'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['user_type'], 'fire_team')
        self.assertEqual(response.data['user']['badge_number'], 'FT001')
        self.assertEqual(response.data['user']['fire_station'], 'Station 1')
    
    def test_register_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'user_type': 'public'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email."""
        # Create first user
        User.objects.create_user(
            username='test1',
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        # Try to register with same email
        data = {
            'email': 'test@example.com',
            'name': 'Another User',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'user_type': 'public'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_missing_required_fields(self):
        """Test registration fails when required fields are missing."""
        data = {
            'email': 'test@example.com',
            # Missing name, password, etc.
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    """Test suite for user login."""
    
    def setUp(self):
        """Set up test client and create test user."""
        self.client = APIClient()
        self.login_url = reverse('login')
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            name='Test User',
            password='testpass123',
            user_type='public'
        )
    
    def test_login_success(self):
        """Test successful login with valid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_login_invalid_password(self):
        """Test login fails with invalid password."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login fails with nonexistent email."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_missing_credentials(self):
        """Test login fails when credentials are missing."""
        data = {}
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CurrentUserTests(TestCase):
    """Test suite for current user endpoint."""
    
    def setUp(self):
        """Set up test client and create authenticated user."""
        self.client = APIClient()
        self.me_url = reverse('current-user')
        
        # Create and authenticate user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            name='Test User',
            password='testpass123',
            phone='+1234567890',
            user_type='public'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_current_user_success(self):
        """Test retrieving current user information."""
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['name'], 'Test User')
        self.assertEqual(response.data['user_type'], 'public')
    
    def test_get_current_user_unauthenticated(self):
        """Test retrieving current user fails when not authenticated."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile_success(self):
        """Test updating user profile."""
        data = {
            'name': 'Updated Name',
            'phone': '+9876543210'
        }
        
        response = self.client.patch(self.me_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')
        self.assertEqual(response.data['phone'], '+9876543210')
        
        # Verify database was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.phone, '+9876543210')


class TokenRefreshTests(TestCase):
    """Test suite for JWT token refresh."""
    
    def setUp(self):
        """Set up test client and create user with tokens."""
        self.client = APIClient()
        self.refresh_url = reverse('token-refresh')
        self.login_url = reverse('login')
        
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        
        # Login to get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.refresh_token = login_response.data['tokens']['refresh']
    
    def test_refresh_token_success(self):
        """Test successfully refreshing access token."""
        data = {
            'refresh': self.refresh_token
        }
        
        response = self.client.post(self.refresh_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_refresh_token_invalid(self):
        """Test refresh fails with invalid token."""
        data = {
            'refresh': 'invalid_token_here'
        }
        
        response = self.client.post(self.refresh_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPermissionsTests(TestCase):
    """Test suite for user type permissions."""
    
    def setUp(self):
        """Set up test users with different types."""
        self.client = APIClient()
        
        # Create public user
        self.public_user = User.objects.create_user(
            username='public',
            email='public@example.com',
            name='Public User',
            password='testpass123',
            user_type='public'
        )
        
        # Create fire team member
        self.fire_team_user = User.objects.create_user(
            username='fireteam',
            email='fireteam@example.com',
            name='Fire Team',
            password='testpass123',
            user_type='fire_team',
            badge_number='FT001',
            fire_station='Station 1'
        )
        
        # Create admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            name='Admin User',
            password='testpass123',
            user_type='admin',
            is_staff=True,
            is_superuser=True
        )
    
    def test_user_type_methods(self):
        """Test user type helper methods."""
        # Public user
        self.assertFalse(self.public_user.is_fire_team())
        self.assertFalse(self.public_user.is_admin_user())
        
        # Fire team user
        self.assertTrue(self.fire_team_user.is_fire_team())
        self.assertFalse(self.fire_team_user.is_admin_user())
        
        # Admin user
        self.assertFalse(self.admin_user.is_fire_team())
        self.assertTrue(self.admin_user.is_admin_user())
