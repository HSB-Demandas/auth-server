# 📚 Django App Implementation Guidelines

This document outlines the design principles and implementation guidelines for reusable Django apps. These apps should be self-contained, pluggable, and maintainable across different Django projects.

---

## ✅ Design Criteria

### 1. **Good Practices**
- Follow SOLID principles.
- Prefer composition over inheritance.
- Use dependency inversion for external services.
- Keep business logic separate from Django views.
- Follow DRY (Don't Repeat Yourself) principle.

### 2. **3rd Party Integration**
- All external service integrations must be encapsulated in dedicated wrapper classes.
- Example structure:
  ```
  your_app/
  ├── integrations/
  │   ├── base.py
  │   ├── service1_wrapper.py
  │   └── service2_wrapper.py
  └── ...
  ```
- Wrappers should implement clear interfaces and handle all service-specific logic.
- Mocking should be done at the wrapper level, not at the service level.

### 3. **Configuration & Environment**
- Never access `os.environ` directly in the app code.
- Always use Django's settings system for configuration.
- Example:
  ```python
  # bad
  import os
  API_KEY = os.environ.get('API_KEY')

  # good
  from django.conf import settings
  API_KEY = settings.API_KEY
  ```
- Document all required settings in the app's documentation.
- Provide sensible defaults where possible.

### 4. **Architecture & Organization**
- Follow Django's recommended app structure:
  - `models.py` for data models
  - `views.py` for view logic
  - `serializers.py` for API serialization
  - `services.py` for business logic
  - `tasks.py` for background jobs
  - `templates/` for templates
  - `static/` for static assets
  - `migrations/` for database migrations
- Keep related functionality grouped together.
- Use abstract base classes for common model functionality.
- Document model relationships and usage patterns.

### 5. **Data Layer**
- Use Django's ORM exclusively for database operations.
- Implement proper model relationships and constraints.
- Use proper indexes for query optimization.
- Document model relationships and usage patterns.
- Implement proper error handling for database operations.

### 6. **Business Logic**
- Keep business logic in services, not in views or models.
- Use dependency injection for external services.
- Implement proper error handling and validation.
- Follow Django's transaction management patterns.
- Use Django's caching framework effectively.

### 7. **API Layer**
- Use Django REST Framework (DRF) for API endpoints.
- Implement proper authentication/authorization.
- Use serializers for data validation and transformation.
- Follow RESTful principles.
- Document API endpoints with Swagger/OpenAPI.

### 8. **Testing Strategy**
- Clear separation of test types:
  - Unit tests: Test business logic and models
  - Internal integration tests: Test Django ORM and internal systems
  - External integration tests: Test external service integrations
- External integration tests should be:
  - Disabled by default (require explicit flag)
  - Clearly marked as external tests
  - Use real credentials only in test environments
  - Include setup and teardown procedures
- Example test structure:
  ```
  your_app/
  ├── tests/
  │   ├── unit/
  │   │   ├── test_models.py
  │   │   └── test_services.py
  │   ├── internal_integration/
  │   │   ├── test_views.py
  │   │   └── test_queries.py
  │   └── external_integration/
  │       ├── test_service1.py
  │       └── test_service2.py
  ```

### 9. **Documentation**
- Document all public interfaces.
- Include installation instructions.
- Document configuration options.
- Provide usage examples.
- Document API endpoints.
- Include migration instructions.
- Document external service requirements.

---

## 🤖 LLM Implementation Instructions

When generating or editing Django app code:

### 1. Model Implementation
```python
# models.py
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class YourModel(BaseModel):
    # Fields
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive')
        ],
        default='active'
    )
    
    # Methods
    def get_full_representation(self):
        return f"{self.name} ({self.status})"
```

### 2. Service Layer
```python
# services.py
from .models import YourModel
from django.core.exceptions import ValidationError

class YourService:
    def __init__(self, model_class=YourModel):
        self.model_class = model_class

    def create_instance(self, data):
        try:
            instance = self.model_class.objects.create(**data)
            return instance
        except ValidationError as e:
            raise ValueError(f"Validation failed: {str(e)}")
```

### 3. API Implementation
```python
# serializers.py
from rest_framework import serializers
from .models import YourModel

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

# views.py
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = [IsAuthenticated]
```

### 4. Testing Pattern
```python
# tests/test_models.py
from django.test import TestCase
from .models import YourModel

class YourModelTests(TestCase):
    def setUp(self):
        self.instance = YourModel.objects.create(name="Test")

    def test_creation(self):
        self.assertIsNotNone(self.instance.id)
        self.assertEqual(self.instance.name, "Test")

# tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class YourModelViewTests(TestCase):
    def test_list_endpoint(self):
        response = self.client.get(reverse('yourmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### 5. Configuration Pattern
```python
# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'
    verbose_name = 'Your App Name'

    def ready(self):
        import your_app.signals  # Import signals if needed
```

### 6. Best Practices
- Use Django's built-in features over third-party packages when possible
- Follow Django's security best practices
- Use proper error handling and logging
- Implement proper caching strategies
- Use Django's signals for event handling
- Follow Django's template inheritance patterns
- Use Django's form system for validation
- Implement proper database migrations
- Use Django's admin interface for maintenance
- Follow Django's testing patterns

---

## 📋 Documentation Requirements

Every Django app documentation must include:

1. **Overview**
   - Purpose and main use cases
   - Key features
   - Dependencies

2. **Installation**
   - Required packages
   - Configuration steps
   - Database setup
   - Caching setup

3. **Usage**
   - Basic setup
   - Common operations
   - Integration points

4. **API Documentation**
   - Endpoints
   - Request/response formats
   - Authentication
   - Rate limiting

5. **Configuration**
   - Required settings
   - Optional settings
   - Environment variables

6. **Testing**
   - Running tests
   - Test coverage
   - Mocking strategies

7. **Security**
   - Authentication
   - Authorization
   - Input validation
   - Error handling

8. **Performance**
   - Caching strategies
   - Database optimization
   - Query optimization

9. **Troubleshooting**
   - Common issues
   - Debugging tips
   - Error messages
