# Fire Watcher API - Detailed Endpoint Documentation

This document provides detailed information about all API endpoints, including request/response formats and examples.

## Base URL

```
http://localhost:8000/api
```

---

## Authentication Endpoints

### 1. Register User

**Endpoint**: `POST /auth/register/`

**Description**: Create a new user account

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "user_type": "public",
  "badge_number": "",  // Optional, for fire_team
  "fire_station": ""   // Optional, for fire_team
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "user_type": "public",
    "badge_number": null,
    "fire_station": null,
    "created_at": "2026-02-04T21:00:00Z"
  },
  "tokens": {
    "refresh": "refresh_token_here",
    "access": "access_token_here"
  }
}
```

---

### 2. Login

**Endpoint**: `POST /auth/login/`

**Description**: Authenticate and get JWT tokens

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "user_type": "public",
    "badge_number": null,
    "fire_station": null,
    "created_at": "2026-02-04T21:00:00Z"
  },
  "tokens": {
    "refresh": "refresh_token_here",
    "access": "access_token_here"
  }
}
```

---

### 3. Get Current User

**Endpoint**: `GET /auth/me/`

**Description**: Get current authenticated user's information

**Authentication**: Required (Bearer token)

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "user_type": "public",
  "badge_number": null,
  "fire_station": null,
  "created_at": "2026-02-04T21:00:00Z"
}
```

---

### 4. Update Profile

**Endpoint**: `PATCH /auth/me/`

**Description**: Update current user's profile

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "name": "Updated Name",
  "phone": "+9876543210"
}
```

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "email": "user@example.com",
  "name": "Updated Name",
  "phone": "+9876543210",
  "user_type": "public",
  "badge_number": null,
  "fire_station": null,
  "created_at": "2026-02-04T21:00:00Z"
}
```

---

### 5. Refresh Token

**Endpoint**: `POST /auth/token/refresh/`

**Description**: Refresh access token using refresh token

**Authentication**: Not required

**Request Body**:
```json
{
  "refresh": "refresh_token_here"
}
```

**Response** (200 OK):
```json
{
  "access": "new_access_token_here"
}
```

---

### 6. Logout

**Endpoint**: `POST /auth/logout/`

**Description**: Logout by blacklisting refresh token

**Authentication**: Required (Bearer token)

**Request Body**:
```json
{
  "refresh": "refresh_token_here"
}
```

**Response** (205 Reset Content):
```json
{
  "message": "Logout successful"
}
```

---

## Incident Endpoints

### 1. List Incidents

**Endpoint**: `GET /incidents/`

**Description**: List all incidents (filtered by user permissions)

**Authentication**: Required (Bearer token)

**Query Parameters**:
- `status` (optional): Filter by status (new, enroute, arrived, fighting, extinguished, closed)
- `search` (optional): Search in address, description, reporter_name
- `ordering` (optional): Order by field (created_at, updated_at, status)
- `page` (optional): Page number for pagination

**Response** (200 OK):
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/incidents/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid-here",
      "reporter_name": "John Doe",
      "reporter_phone": "+1234567890",
      "lat": "40.712800",
      "lng": "-74.006000",
      "address": "123 Main St, New York, NY",
      "description": "Fire in building",
      "status": "new",
      "created_at": "2026-02-04T21:00:00Z",
      "updated_at": "2026-02-04T21:00:00Z"
    }
  ]
}
```

---

### 2. Create Incident

**Endpoint**: `POST /incidents/`

**Description**: Report a new fire incident

**Authentication**: Optional (can be anonymous)

**Content-Type**: `multipart/form-data` (for photo uploads) or `application/json`

**Request Body** (multipart/form-data):
```
lat: 40.7128
lng: -74.0060
address: 123 Main St, New York, NY
description: Fire in building
reporter_name: John Doe
reporter_phone: +1234567890
photos: [file1.jpg, file2.jpg]  // Optional
```

**Response** (201 Created):
```json
{
  "id": "uuid-here",
  "reporter": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "user_type": "public",
    "badge_number": null,
    "fire_station": null,
    "created_at": "2026-02-04T21:00:00Z"
  },
  "reporter_name": "John Doe",
  "reporter_phone": "+1234567890",
  "lat": "40.712800",
  "lng": "-74.006000",
  "address": "123 Main St, New York, NY",
  "description": "Fire in building",
  "status": "new",
  "photos": [
    {
      "id": "uuid-here",
      "image": "http://localhost:8000/media/incident_photos/2026/02/04/photo1.jpg",
      "uploaded_at": "2026-02-04T21:00:00Z"
    }
  ],
  "status_updates": [
    {
      "id": "uuid-here",
      "status": "new",
      "updated_by": {
        "id": "uuid-here",
        "email": "user@example.com",
        "name": "John Doe",
        "phone": "+1234567890",
        "user_type": "public",
        "badge_number": null,
        "fire_station": null,
        "created_at": "2026-02-04T21:00:00Z"
      },
      "notes": "Incident reported",
      "timestamp": "2026-02-04T21:00:00Z"
    }
  ],
  "created_at": "2026-02-04T21:00:00Z",
  "updated_at": "2026-02-04T21:00:00Z"
}
```

---

### 3. Get Incident Detail

**Endpoint**: `GET /incidents/{id}/`

**Description**: Get detailed information about a specific incident

**Authentication**: Required (Bearer token)

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "reporter": {
    "id": "uuid-here",
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "user_type": "public",
    "badge_number": null,
    "fire_station": null,
    "created_at": "2026-02-04T21:00:00Z"
  },
  "reporter_name": "John Doe",
  "reporter_phone": "+1234567890",
  "lat": "40.712800",
  "lng": "-74.006000",
  "address": "123 Main St, New York, NY",
  "description": "Fire in building",
  "status": "fighting",
  "photos": [
    {
      "id": "uuid-here",
      "image": "http://localhost:8000/media/incident_photos/2026/02/04/photo1.jpg",
      "uploaded_at": "2026-02-04T21:00:00Z"
    }
  ],
  "status_updates": [
    {
      "id": "uuid-here",
      "status": "fighting",
      "updated_by": {
        "id": "uuid-here",
        "email": "fireteam@example.com",
        "name": "Fire Team Alpha",
        "phone": "+1234567890",
        "user_type": "fire_team",
        "badge_number": "FT001",
        "fire_station": "Station 1",
        "created_at": "2026-02-04T21:00:00Z"
      },
      "notes": "Team on scene, engaging fire",
      "timestamp": "2026-02-04T21:15:00Z"
    },
    {
      "id": "uuid-here",
      "status": "new",
      "updated_by": {
        "id": "uuid-here",
        "email": "user@example.com",
        "name": "John Doe",
        "phone": "+1234567890",
        "user_type": "public",
        "badge_number": null,
        "fire_station": null,
        "created_at": "2026-02-04T21:00:00Z"
      },
      "notes": "Incident reported",
      "timestamp": "2026-02-04T21:00:00Z"
    }
  ],
  "created_at": "2026-02-04T21:00:00Z",
  "updated_at": "2026-02-04T21:15:00Z"
}
```

---

### 4. Update Incident Status

**Endpoint**: `PATCH /incidents/{id}/status/`

**Description**: Update the status of an incident (Fire Team only)

**Authentication**: Required (Fire Team or Admin only)

**Request Body**:
```json
{
  "status": "fighting",
  "notes": "Team Alpha on scene, engaging fire"
}
```

**Response** (200 OK):
```json
{
  "id": "uuid-here",
  "reporter": {...},
  "reporter_name": "John Doe",
  "reporter_phone": "+1234567890",
  "lat": "40.712800",
  "lng": "-74.006000",
  "address": "123 Main St, New York, NY",
  "description": "Fire in building",
  "status": "fighting",
  "photos": [...],
  "status_updates": [...],
  "created_at": "2026-02-04T21:00:00Z",
  "updated_at": "2026-02-04T21:15:00Z"
}
```

---

### 5. Get Status History

**Endpoint**: `GET /incidents/{id}/updates/`

**Description**: Get complete status update history for an incident

**Authentication**: Required (Bearer token)

**Response** (200 OK):
```json
[
  {
    "id": "uuid-here",
    "status": "fighting",
    "updated_by": {
      "id": "uuid-here",
      "email": "fireteam@example.com",
      "name": "Fire Team Alpha",
      "phone": "+1234567890",
      "user_type": "fire_team",
      "badge_number": "FT001",
      "fire_station": "Station 1",
      "created_at": "2026-02-04T21:00:00Z"
    },
    "notes": "Team on scene, engaging fire",
    "timestamp": "2026-02-04T21:15:00Z"
  },
  {
    "id": "uuid-here",
    "status": "new",
    "updated_by": {
      "id": "uuid-here",
      "email": "user@example.com",
      "name": "John Doe",
      "phone": "+1234567890",
      "user_type": "public",
      "badge_number": null,
      "fire_station": null,
      "created_at": "2026-02-04T21:00:00Z"
    },
    "notes": "Incident reported",
    "timestamp": "2026-02-04T21:00:00Z"
  }
]
```

---

## Dashboard Endpoints

### 1. Get Dashboard Statistics

**Endpoint**: `GET /dashboard/stats/`

**Description**: Get summary statistics for fire team dashboard

**Authentication**: Required (Fire Team or Admin only)

**Response** (200 OK):
```json
{
  "new": 5,
  "active": 7,
  "resolved": 10,
  "total": 22
}
```

**Statistics Breakdown**:
- `new`: Incidents with status "new"
- `active`: Incidents with status "enroute", "arrived", or "fighting"
- `resolved`: Incidents with status "extinguished" or "closed"
- `total`: Total number of incidents

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Authentication Header Format

For all authenticated endpoints, include the JWT access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Example:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```
