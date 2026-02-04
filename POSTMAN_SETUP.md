# Postman Collection Setup Guide

This guide explains how to use the Fire Watcher API Postman collection with automatic JWT token management.

## Files Included

1. **fire-api.postman_collection.json** - The main API collection
2. **fire-api.postman_environment.json** - Environment variables for local development

## Import into Postman

### Step 1: Import Collection

1. Open Postman
2. Click **Import** button (top left)
3. Select **fire-api.postman_collection.json**
4. Click **Import**

### Step 2: Import Environment

1. Click **Import** button again
2. Select **fire-api.postman_environment.json**
3. Click **Import**

### Step 3: Activate Environment

1. In the top-right corner, click the environment dropdown
2. Select **Fire API - Local**
3. The environment is now active

## How Automatic JWT Management Works

The collection uses Postman's **Test Scripts** to automatically manage JWT tokens:

### 1. Login/Register Flow

When you call **Login** or **Register User**:
- The response contains JWT tokens
- A test script automatically extracts the tokens
- Tokens are saved to environment variables:
  - `access_token` - Used for authentication
  - `refresh_token` - Used to get new access tokens
  - `user_id`, `user_email`, `user_type` - User info

### 2. Authenticated Requests

All endpoints (except auth endpoints) automatically use the saved `access_token`:
- Collection-level auth is set to Bearer Token
- Uses `{{access_token}}` variable
- No need to manually copy/paste tokens!

### 3. Token Refresh

When your access token expires:
- Call **Refresh Token** endpoint
- It uses the saved `refresh_token`
- Automatically updates `access_token` with the new one

### 4. Logout

When you call **Logout**:
- Tokens are blacklisted on the server
- Test script automatically clears all tokens from environment

## Quick Start Guide

### 1. Start Your Django Server

```bash
cd "/home/troubleman/Documents/software work/Group2-fireAPI"
source venv/bin/activate
python manage.py runserver
```

### 2. Register a User

1. Open the collection
2. Go to **Authentication** → **Register User**
3. Click **Send**
4. ✅ Tokens are automatically saved!

### 3. Test Authenticated Endpoints

1. Go to **Incidents** → **List Incidents**
2. Click **Send**
3. ✅ Request automatically uses your saved token!

### 4. Create an Incident

1. Go to **Incidents** → **Create Incident (JSON)**
2. Click **Send**
3. ✅ Incident ID is automatically saved to `{{incident_id}}`

### 5. View Incident Details

1. Go to **Incidents** → **Get Incident Detail**
2. Notice the URL uses `{{incident_id}}`
3. Click **Send**
4. ✅ Automatically uses the last created incident!

## Testing Fire Team Features

### Register a Fire Team Member

1. Go to **Authentication** → **Register Fire Team Member**
2. Click **Send**
3. ✅ Now you're logged in as a fire team member!

### Update Incident Status

1. Go to **Incidents** → **Update Incident Status**
2. Modify the status (e.g., "fighting")
3. Click **Send**
4. ✅ Only works with fire team or admin accounts!

### View Dashboard Stats

1. Go to **Dashboard** → **Get Dashboard Stats**
2. Click **Send**
3. ✅ See statistics for all incidents!

## Environment Variables

The environment includes these variables:

| Variable | Description | Auto-Updated |
|----------|-------------|--------------|
| `base_url` | API base URL | No |
| `access_token` | JWT access token | Yes (on login/register/refresh) |
| `refresh_token` | JWT refresh token | Yes (on login/register) |
| `user_id` | Current user ID | Yes (on login/register) |
| `user_email` | Current user email | Yes (on login) |
| `user_type` | Current user type | Yes (on login) |
| `incident_id` | Last created incident ID | Yes (on create incident) |

## Tips & Tricks

### 1. View Saved Tokens

1. Click the **eye icon** next to environment dropdown
2. See all saved variables and their values
3. Tokens are marked as "secret" for security

### 2. Check Console Logs

1. Open Postman Console (View → Show Postman Console)
2. See helpful messages like:
   - ✅ Login successful! User: john@example.com
   - ✅ Tokens saved! Access token: eyJ0eXAiOiJKV1QiLCJ...
   - ✅ Incident created! ID: abc-123-def

### 3. Switch Between Users

To test with different user types:
1. Call **Logout** to clear current tokens
2. Call **Login** with different credentials
3. Or call **Register Fire Team Member** for fire team access

### 4. Test Different Scenarios

The collection includes examples for:
- Public user registration and incident reporting
- Fire team member registration with badge/station
- Filtering incidents by status
- Searching incidents by keyword
- Updating incident status with notes
- Viewing status history

### 5. Photo Uploads

For **Create Incident (with Photos)**:
1. Open the request
2. Go to **Body** tab
3. Enable the "photos" field
4. Click **Select Files** to choose images
5. Click **Send**

## Troubleshooting

### "Unauthorized" Error

**Problem**: Getting 401 Unauthorized errors

**Solutions**:
1. Check if `access_token` is set in environment
2. Token might be expired - call **Refresh Token**
3. Or login again with **Login** endpoint

### "Forbidden" Error

**Problem**: Getting 403 Forbidden errors

**Solutions**:
1. Check your `user_type` in environment
2. Some endpoints require `fire_team` or `admin` type
3. Register/login as fire team member for those endpoints

### Token Not Saving

**Problem**: Tokens not automatically saving after login

**Solutions**:
1. Make sure **Fire API - Local** environment is selected
2. Check Postman Console for any script errors
3. Verify the response status is 200/201

### Base URL Issues

**Problem**: Requests failing with connection errors

**Solutions**:
1. Verify Django server is running: `python manage.py runserver`
2. Check `base_url` in environment is `http://localhost:8000`
3. Make sure no other service is using port 8000

## Collection Structure

```
Fire Watcher API/
├── Authentication/
│   ├── Register User (saves tokens)
│   ├── Login (saves tokens)
│   ├── Get Current User
│   ├── Update Profile
│   ├── Refresh Token (updates access token)
│   ├── Logout (clears tokens)
│   └── Register Fire Team Member (saves tokens)
├── Incidents/
│   ├── List Incidents
│   ├── List Incidents - Filter by Status
│   ├── List Incidents - Search
│   ├── Create Incident (JSON)
│   ├── Create Incident (with Photos) (saves incident_id)
│   ├── Get Incident Detail (uses incident_id)
│   ├── Update Incident Status
│   └── Get Status History
└── Dashboard/
    └── Get Dashboard Stats
```

## Next Steps

1. **Customize**: Modify request bodies to test different scenarios
2. **Add Tests**: Add more test scripts to validate responses
3. **Create Workflows**: Use Postman's Collection Runner for automated testing
4. **Share**: Export and share the collection with your team

## Support

For API documentation, see:
- [README.md](file:///home/troubleman/Documents/software%20work/Group2-fireAPI/README.md)
- [API_DOCUMENTATION.md](file:///home/troubleman/Documents/software%20work/Group2-fireAPI/API_DOCUMENTATION.md)

Happy Testing! 🔥
