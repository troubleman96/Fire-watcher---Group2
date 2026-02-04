# Fire Watcher Backend API

A Django REST Framework backend for the Fire Watcher application - a fire incident reporting and management system.

## Features

- **Custom User Management**: Support for public users, fire team members, and administrators
- **Fire Incident Reporting**: Citizens can report fires with location, description, and photos
- **Incident Management**: Fire teams can update incident status and track progress
- **Real-time Status Updates**: Complete audit trail of incident status changes
- **Photo Uploads**: Support for multiple photo uploads per incident
- **Dashboard Statistics**: Summary statistics for fire team dashboard
- **JWT Authentication**: Secure token-based authentication
- **Clean Architecture**: Service-oriented design with clear separation of concerns

## Project Structure

```
Group2-fireAPI/
├── core/                      # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── apps/                      # All Django applications
│   ├── accounts/             # User management and authentication
│   │   ├── models.py         # Custom User model
│   │   ├── serializers.py    # User serializers
│   │   ├── services.py       # Business logic for users
│   │   ├── views.py          # API views for auth
│   │   ├── urls.py           # Auth endpoints
│   │   └── admin.py          # Admin configuration
│   └── incidents/            # Fire incident management
│       ├── models.py         # Incident, StatusUpdate, IncidentPhoto models
│       ├── serializers.py    # Incident serializers
│       ├── services.py       # Business logic for incidents
│       ├── views.py          # API views for incidents
│       ├── permissions.py    # Custom permissions
│       ├── urls.py           # Incident endpoints
│       ├── urls_dashboard.py # Dashboard endpoints
│       └── admin.py          # Admin configuration
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Group2-fireAPI
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser** (for admin access):
```bash
python manage.py createsuperuser
```

6. **Run development server**:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `GET /api/auth/me/` - Get current user info
- `PATCH /api/auth/me/` - Update current user profile
- `POST /api/auth/token/refresh/` - Refresh JWT access token

### Incidents

- `GET /api/incidents/` - List incidents (with filtering and pagination)
- `POST /api/incidents/` - Report a new incident
- `GET /api/incidents/{id}/` - Get incident details
- `PATCH /api/incidents/{id}/status/` - Update incident status (Fire Team only)
- `GET /api/incidents/{id}/updates/` - Get incident status history

### Dashboard

- `GET /api/dashboard/stats/` - Get dashboard statistics (Fire Team only)

## User Types

1. **Public Users** (`user_type: public`):
   - Can report fire incidents
   - Can view their own reported incidents
   - Can update their profile

2. **Fire Team Members** (`user_type: fire_team`):
   - All public user permissions
   - Can view all incidents
   - Can update incident status
   - Can access dashboard statistics
   - Have badge_number and fire_station fields

3. **Administrators** (`user_type: admin`):
   - Full access to all features
   - Can manage users via Django admin

## Incident Status Flow

1. **new** - Incident just reported
2. **enroute** - Fire team dispatched and on the way
3. **arrived** - Fire team arrived at scene
4. **fighting** - Actively fighting the fire
5. **extinguished** - Fire has been put out
6. **closed** - Incident closed and resolved

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register or Login** to get access and refresh tokens
2. **Include the access token** in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```
3. **Refresh the token** when it expires using the refresh endpoint

## Example Usage

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "user_type": "public"
  }'
```

### Report an Incident
```bash
curl -X POST http://localhost:8000/api/incidents/ \
  -H "Authorization: Bearer <access_token>" \
  -F "lat=40.7128" \
  -F "lng=-74.0060" \
  -F "address=123 Main St, New York, NY" \
  -F "description=Fire in building" \
  -F "reporter_name=John Doe" \
  -F "reporter_phone=+1234567890" \
  -F "photos=@photo1.jpg" \
  -F "photos=@photo2.jpg"
```

### Update Incident Status (Fire Team)
```bash
curl -X PATCH http://localhost:8000/api/incidents/{incident_id}/status/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "fighting",
    "notes": "Team Alpha on scene, engaging fire"
  }'
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- Manage users
- View and edit incidents
- Monitor status updates
- Manage photos

## Development Notes

### Service Layer Pattern

This project follows a service-oriented architecture:
- **Models**: Define data structure
- **Serializers**: Handle data validation and transformation
- **Services**: Contain business logic
- **Views**: Handle HTTP requests/responses
- **Permissions**: Control access

This separation ensures:
- Testable business logic
- Reusable code
- Clear responsibilities
- Easy maintenance

### Code Documentation

All code is extensively commented to explain:
- What each component does
- How to use it
- Example usage
- Important considerations

## Testing

Run tests with:
```bash
python manage.py test
```

## Production Deployment

Before deploying to production:

1. **Update settings.py**:
   - Set `DEBUG = False`
   - Update `SECRET_KEY` (use environment variable)
   - Configure `ALLOWED_HOSTS`
   - Update `CORS_ALLOW_ALL_ORIGINS` to specific origins

2. **Use PostgreSQL** instead of SQLite:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'firewatch_db',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Configure static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Use a production server** (e.g., Gunicorn with Nginx)

## License

[camelTech]

## Contributors

[Group 2 - IT
"dev-medy, Abas, camel"]
