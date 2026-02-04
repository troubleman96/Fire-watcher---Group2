# Quick Setup Script

This script helps you quickly set up the Fire Watcher API after migrations are complete.

## Create Superuser

Run this command to create an admin account:

```bash
./venv/bin/python manage.py createsuperuser
```

You'll be prompted for:
- **Email**: Your admin email (e.g., admin@example.com)
- **Username**: Your admin username (e.g., admin)
- **Name**: Your full name (e.g., Admin User)
- **Password**: Your secure password
- **Password (again)**: Confirm password

## Start Development Server

```bash
./venv/bin/python manage.py runserver
```

The API will be available at: http://localhost:8000/

## Access Points

- **API Root**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Auth Endpoints**: http://localhost:8000/api/auth/
- **Incidents Endpoints**: http://localhost:8000/api/incidents/
- **Dashboard Stats**: http://localhost:8000/api/dashboard/stats/

## Test with Postman

1. Import the Postman collection: `fire-api.postman_collection.json`
2. Import the environment: `fire-api.postman_environment.json`
3. Select "Fire API - Local" environment
4. Start testing!

## Quick Test Commands

### Register a User (curl)
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+1234567890",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "user_type": "public"
  }'
```

### Login (curl)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Save the access token from the response and use it for authenticated requests!

## Database Status

✅ All migrations applied successfully:
- accounts app (User model)
- incidents app (Incident, StatusUpdate, IncidentPhoto models)
- token_blacklist (JWT token management)
- Django core apps (admin, auth, sessions, etc.)

## Next Steps

1. Create a superuser (see above)
2. Start the development server
3. Access Django admin to verify setup
4. Test API endpoints with Postman or curl
5. Start building your frontend!
