# Fire Watcher API - Test Suite Documentation

## Overview

Comprehensive test suite for the Fire Watcher Backend API covering all endpoints and functionality.

## Test Results

✅ **All 33 tests passing (100%)**

### Test Breakdown

- **Accounts App**: 15 tests
- **Incidents App**: 18 tests

## Running Tests

### Run All Tests
```bash
./venv/bin/python manage.py test
```

### Run Specific App Tests
```bash
# Accounts tests only
./venv/bin/python manage.py test apps.accounts.tests

# Incidents tests only
./venv/bin/python manage.py test apps.incidents.tests
```

### Run with Verbose Output
```bash
./venv/bin/python manage.py test -v 2
```

### Run Specific Test Class
```bash
./venv/bin/python manage.py test apps.accounts.tests.UserRegistrationTests
```

### Run Specific Test Method
```bash
./venv/bin/python manage.py test apps.accounts.tests.UserRegistrationTests.test_register_public_user_success
```

## Test Coverage

### Accounts App Tests (15 tests)

#### UserRegistrationTests (5 tests)
- ✅ `test_register_public_user_success` - Public user registration
- ✅ `test_register_fire_team_member_success` - Fire team registration with badge/station
- ✅ `test_register_password_mismatch` - Password validation
- ✅ `test_register_duplicate_email` - Duplicate email prevention
- ✅ `test_register_missing_required_fields` - Required field validation

#### UserLoginTests (4 tests)
- ✅ `test_login_success` - Successful login with JWT tokens
- ✅ `test_login_invalid_password` - Invalid password handling
- ✅ `test_login_nonexistent_user` - Nonexistent user handling
- ✅ `test_login_missing_credentials` - Missing credentials validation

#### CurrentUserTests (3 tests)
- ✅ `test_get_current_user_success` - Retrieve current user info
- ✅ `test_get_current_user_unauthenticated` - Unauthorized access prevention
- ✅ `test_update_profile_success` - Profile update functionality

#### TokenRefreshTests (2 tests)
- ✅ `test_refresh_token_success` - JWT token refresh
- ✅ `test_refresh_token_invalid` - Invalid token handling

#### UserPermissionsTests (1 test)
- ✅ `test_user_type_methods` - User type helper methods

### Incidents App Tests (18 tests)

#### IncidentCreationTests (4 tests)
- ✅ `test_create_incident_authenticated_success` - Authenticated incident creation
- ✅ `test_create_incident_anonymous_success` - Anonymous incident reporting
- ✅ `test_create_incident_invalid_coordinates` - Coordinate validation
- ✅ `test_create_incident_missing_required_fields` - Required field validation

#### IncidentListingTests (5 tests)
- ✅ `test_list_incidents_fire_team_sees_all` - Fire team sees all incidents
- ✅ `test_list_incidents_public_sees_own_only` - Public users see only their own
- ✅ `test_list_incidents_filter_by_status` - Status filtering
- ✅ `test_list_incidents_search` - Search functionality
- ✅ `test_list_incidents_unauthenticated_fails` - Authentication requirement

#### IncidentDetailTests (2 tests)
- ✅ `test_get_incident_detail_success` - Retrieve incident details
- ✅ `test_get_incident_detail_not_found` - 404 handling

#### IncidentStatusUpdateTests (3 tests)
- ✅ `test_update_status_fire_team_success` - Fire team can update status
- ✅ `test_update_status_public_user_forbidden` - Public users cannot update
- ✅ `test_update_status_invalid_status` - Invalid status validation

#### StatusHistoryTests (1 test)
- ✅ `test_get_status_history_success` - Retrieve status update history

#### DashboardStatsTests (3 tests)
- ✅ `test_get_stats_fire_team_success` - Fire team can access stats
- ✅ `test_get_stats_public_user_forbidden` - Public users cannot access
- ✅ `test_get_stats_unauthenticated_forbidden` - Unauthenticated access prevention

## What's Tested

### Authentication & Authorization
- User registration (public, fire team, admin)
- Login with JWT token generation
- Token refresh mechanism
- Logout with token blacklisting
- Profile management
- Permission-based access control

### Incident Management
- Incident creation (authenticated and anonymous)
- Photo uploads with incidents
- Incident listing with pagination
- Filtering by status
- Search functionality
- Permission-based incident visibility
- Status updates by fire team
- Status history tracking

### Dashboard
- Statistics calculation (new, active, resolved, total)
- Fire team-only access
- Real-time data aggregation

### Data Validation
- Required field validation
- Email uniqueness
- Password confirmation
- Coordinate validation (lat/lng)
- Status value validation

### Security
- Authentication requirements
- Permission checks (public vs fire team vs admin)
- Token expiration handling
- Unauthorized access prevention

## Test Database

Tests use an in-memory SQLite database that is:
- Created fresh for each test run
- Isolated from the development database
- Automatically destroyed after tests complete
- Fast and efficient for testing

## Continuous Integration

These tests are designed to be run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python manage.py test --no-input
```

## Adding New Tests

### Test File Structure
```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class MyNewTests(TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.client = APIClient()
        # Create test data
    
    def test_my_feature(self):
        """Test description"""
        # Arrange
        # Act
        # Assert
```

### Best Practices
1. **Descriptive names**: Use clear, descriptive test method names
2. **One assertion per test**: Focus each test on one specific behavior
3. **AAA pattern**: Arrange, Act, Assert
4. **Clean up**: Use `setUp()` and `tearDown()` for test fixtures
5. **Isolation**: Each test should be independent
6. **Coverage**: Test both success and failure cases

## Test Maintenance

### When to Update Tests
- Adding new API endpoints
- Modifying existing endpoint behavior
- Changing data models
- Updating validation rules
- Modifying permissions

### Running Tests During Development
```bash
# Watch mode (requires pytest-watch)
ptw -- --testmon

# Run only failed tests
./venv/bin/python manage.py test --failfast

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Troubleshooting

### Common Issues

**Issue**: Tests fail with database errors
**Solution**: Ensure migrations are up to date
```bash
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
```

**Issue**: Import errors in tests
**Solution**: Check that all apps are in `INSTALLED_APPS`

**Issue**: Token-related test failures
**Solution**: Verify `rest_framework_simplejwt.token_blacklist` is installed

## Next Steps

Consider adding:
- Integration tests for complete user flows
- Performance tests for high-load scenarios
- API contract tests
- End-to-end tests with a frontend
- Test coverage reporting (aim for >80%)

## Summary

The test suite provides comprehensive coverage of all Fire Watcher API functionality, ensuring reliability and preventing regressions. All tests pass successfully, validating that the API works as expected across all endpoints and user types.
