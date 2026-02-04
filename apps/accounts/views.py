"""
API Views for Accounts App

This module contains DRF views for authentication and user management.
Views handle HTTP requests/responses and delegate business logic to services.
"""

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer
)
from .services import UserService


class RegisterView(APIView):
    """
    User Registration Endpoint
    
    POST /api/auth/register/
    
    Allows new users to create an account.
    No authentication required.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Register a new user.
        
        Request Body:
            {
                "email": "user@example.com",
                "name": "John Doe",
                "phone": "+1234567890",
                "password": "securepassword",
                "password_confirm": "securepassword",
                "user_type": "public"
            }
        
        Response:
            201: User created successfully with JWT tokens
            400: Validation errors
        """
        user, errors = UserService.register_user(request.data)
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    User Login Endpoint
    
    POST /api/auth/login/
    
    Authenticates a user and returns JWT tokens.
    No authentication required.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Authenticate a user and return JWT tokens.
        
        Request Body:
            {
                "email": "user@example.com",
                "password": "password123"
            }
        
        Response:
            200: Authentication successful with JWT tokens
            401: Invalid credentials
        """
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user using service
        user = UserService.authenticate_user(email, password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'User account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    """
    Current User Endpoint
    
    GET /api/auth/me/
    
    Returns the currently authenticated user's information.
    Requires authentication.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get current user information.
        
        Response:
            200: User data
            401: Not authenticated
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        """
        Update current user's profile.
        
        Request Body:
            {
                "name": "Updated Name",
                "phone": "+9876543210"
            }
        
        Response:
            200: User updated successfully
            400: Validation errors
        """
        user, errors = UserService.update_user_profile(request.user, request.data)
        
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    User Logout Endpoint
    
    POST /api/auth/logout/
    
    Blacklists the refresh token to log out the user.
    Requires authentication.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Logout user by blacklisting refresh token.
        
        Request Body:
            {
                "refresh": "refresh_token_here"
            }
        
        Response:
            205: Logout successful
            400: Bad request
        """
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
