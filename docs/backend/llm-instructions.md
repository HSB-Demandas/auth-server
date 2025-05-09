# 🧠 Guiding Principles

## 🧠 Guiding Principles

- **Understand First, Code Later**: Do not implement any logic before reading and comprehending the entire documentation.
- **TDD is Mandatory**: Follow the strict Test-Driven Development cycle—tests must come before any code.
- **KISS (Keep It Simple, Stupid)**: Prioritize simplicity. Avoid unnecessary abstractions or premature optimizations.
- **SOLID Principles**: Respect single responsibility, interface segregation, dependency inversion, etc.
- **Failing Tests First**: Ensure all planned tests fail before starting implementation.
- **Progressive Complexity**: Always implement the simplest test and logic first, then scale up.
- **Integration Tests Must Be Isolated**: Use environment flags to enable real-world integration testing only when explicitly requested.
- **Strict Sequential TDD**: Never implement or write multiple tests or classes in advance—work one test at a time, only progressing once it passes.
- **Pydantic by Default**: All data structures, inputs, outputs, and configs should use Pydantic models. Avoid using raw dictionaries for transferring data across layers.
- **StructLog for Logging**: Always use StructLog as the default logging tool for all modules, components, and services.

## 🏗️ Environment Setup

### 1. Virtual Environment Location
```bash
# Find the virtual environment location
which python
# Should point to something like: /path/to/project/.venv/bin/python
```

### 2. Project Root Path
```bash
# Get the project root path
python -c "import os; print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))"
```

### 3. Verify Environment
```bash
# Check if in correct virtual environment
which python  # Should point to .venv/bin/python
which pip     # Should point to .venv/bin/pip

# Verify Python version
python --version
```

### 4. Package Installation
```bash
# Install dependencies in virtual environment
poetry install

# Verify installed packages
poetry show

# Check package versions
poetry show --tree
```

## 🔄 Implementation Workflow

### 🚫 Phase 0 — Do Not Implement Yet

> ❗️ No classes, functions, or logic should be written at this stage.

- LLM must:
  - Read and understand all documentation
  - Analyze interfaces, config files, dependencies
  - Produce a summary (optionally) of system understanding

### 1. Initial Analysis
- **Read Documentation First**
  - Study the library documentation thoroughly
  - Identify all required components and their relationships
  - Note any special requirements or constraints

- **Define Scope**
  - Break down the implementation into clear, manageable steps
  - Identify dependencies between components
  - Create a prioritized implementation plan

### 2. TDD Implementation Cycle

### 🧪 Phase 1 — Design the Complete Test Plan

- Write unit tests for all desired behavior before any logic
- Order tests from simplest to most complex
- Include error, edge case, and integration stubs
- All tests should initially fail to confirm correctness

### 🔁 TDD Execution Steps (Strict Sequence)

This section outlines the exact sequence to be followed. **No deviations are allowed** from this step-by-step method:

#### ✅ Step 1 — Plan the Tests
- Identify the full set of unit and integration tests based on the documentation and requirements.
- Do **not** write any implementation code.
- Do **not** write the test code itself yet — only plan the tests and document their purpose.

#### ✅ Step 2 — Define the Execution Sequence
- Organize the planned tests in a logical order:
  - From the least complex to the most complex
  - From most isolated (unit) to more integrated
- Prioritize foundational components and simple data validation first

#### ✅ Step 3 — Implement the First Test
- Write the code for the **first test only**
- This test must **fail** initially

#### ✅ Step 4 — Make the First Test Pass
- Write the minimal class, function, or structure required to make the current test pass
- Do not refactor or implement other classes or methods yet

#### ✅ Step 5 — Move to the Next Test
- Only after the current test passes, proceed to the next planned test in the sequence
- Repeat the cycle:
  - Write the test
  - Watch it fail
  - Implement just enough to pass it
  - Refactor only if necessary

#### ⚠️ Important Restrictions
- Do not write multiple tests in advance
- Do not implement future classes preemptively
- Always work on a single test at a time
- Always make tests fail first before fixing them
- Maintain strict test ordering throughout

### 3. Component Implementation Order
1. **Types and Interfaces**
   - Define custom types
   - Create interfaces/protocols
   - Implement type validation

2. **Configuration**
   - Implement config validation
   - Add environment variable handling
   - Document required variables

3. **Client Implementation**
   - Create service client wrapper
   - Implement error handling
   - Add rate limiting

4. **Sender Implementation**
   - Implement core functionality
   - Add input validation
   - Handle service responses

5. **Verifier Implementation**
   - Add verification logic
   - Implement validation rules
   - Handle verification errors

## 📋 Implementation Requirements

### 1. Code Structure

> ℹ️ All configurations and structured data must be implemented using Pydantic models. Avoid using plain dictionaries to pass data between components or layers. Always prefer strongly typed, validated structures.

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class Config(BaseModel):
    """Configuration for the service"""
    account_sid: str = Field(..., description="Twilio Account SID")
    auth_token: str = Field(..., description="Twilio Auth Token")
    from_number: str = Field(..., description="Sender phone number")
    
    @validator('from_number')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            raise ValueError('Phone number must start with +')
        return v
```

- **Type Hints**
  ```python
  def send_message(
      phone: str, 
      message: str
  ) -> "MessageResult":
      """Send SMS message"""
  ```

### 2. Error Handling

- **Custom Exceptions**
  ```python
  class ServiceError(Exception):
      """Base exception for service errors"""
      
      def __init__(self, message: str, code: str = None):
          self.code = code
          super().__init__(message)

  class InvalidPhoneNumberError(ServiceError):
      """Raised when phone number is invalid"""
      
      def __init__(self, phone: str):
          super().__init__(f"Invalid phone number: {phone}", "INVALID_PHONE")
  ```

> ℹ️ All logging should use StructLog. This ensures consistent, structured logs throughout the application.

- **Logging**
  ```python
  import structlog
  
  logger = structlog.get_logger()
  
  def handle_error(error: Exception):
      logger.error(
          "Service error occurred",
          error_type=type(error).__name__,
          error_message=str(error),
          error_code=getattr(error, 'code', None),
          trace_id=get_trace_id()
      )
  ```

### 3. Documentation
- **Module-Level**
  ```python
  """
  Module implementing Twilio SMS functionality.
  
  This module provides a clean interface for sending SMS messages
  through Twilio's API, with proper error handling and validation.
  """
  ```

- **Function-Level**
  ```python
  def send_message(phone: str, message: str) -> "MessageResult":
      """
      Send SMS message to specified phone number.
      
      Args:
          phone: Recipient phone number (must start with +)
          message: Message content (max 1600 characters)
      
      Returns:
          MessageResult: Result of the message sending operation
      
      Raises:
          InvalidPhoneNumberError: If phone number is invalid
          ServiceError: If message sending fails
      """
  ```

## 🛠️ Implementation Checklist

### Environment Setup
- [ ] Virtual environment activated
- [ ] Project root path verified
- [ ] Dependencies installed via Poetry
- [ ] Package versions verified
- [ ] Environment variables set

### Core Implementation
- [ ] Types and interfaces defined
- [ ] Configuration handling implemented
- [ ] Client wrapper created
- [ ] Sender functionality implemented
- [ ] Verifier functionality implemented

### Testing
- [ ] Unit tests written
- [ ] Integration tests implemented
- [ ] Mocks properly isolated
- [ ] Test coverage verified

### 🔌 Phase 3 — Integration Testing (Optional by Flag)

- Integration tests should reside in `tests/integration/`
- Must be skipped by default
- Enable using `INTEGRATION_TESTS_ENABLED=1`

### Documentation
- [ ] Code documented
- [ ] Tests documented
- [ ] Integration requirements documented
- [ ] Error handling documented

### Quality Assurance
- [ ] Type checking passed
- [ ] Linting completed
- [ ] Code review performed
- [ ] Performance verified

### Package Management
- [ ] All dependencies in pyproject.toml
- [ ] Package versions pinned
- [ ] No global package conflicts
- [ ] Environment isolation verified

## 📝 Implementation Notes

1. **Follow Documentation First**
   - Always reference the library documentation
   - Maintain consistency with established patterns
   - Document any deviations from guidelines

2. **Use TDD Strictly**
   - Never implement without a failing test
   - Keep tests isolated and focused
   - Document test assumptions clearly

3. **Maintain Code Quality**
   - Use consistent naming conventions
   - Follow type hinting requirements
   - Keep code DRY and modular

4. **Document Everything**
   - Document code, tests, and integration
   - Include setup instructions
   - Note any special requirements

5. **Review and Validate**
   - Review implementation against documentation
   - Verify test coverage
   - Validate integration points
   - Document any findings

6. **Respect Engineering Best Practices**
   - Apply SOLID principles consistently
   - Use meaningful names and clear interfaces
   - Prefer composition over inheritance
   - Keep each module small and understandable (KISS)
   - Avoid complex inheritance or dynamic behaviors unless strictly needed

7. **Use StructLog and Pydantic as Defaults**
   - StructLog is mandatory for all logging implementations
   - Pydantic is mandatory for all structured data, including request/response objects, configs, and internal models
   - Do not use `dict` to transfer data between layers—prefer type-safe Pydantic models

---

This guide ensures that LLM-assisted implementations follow the established patterns and maintain high quality standards while providing clear structure for both development and documentation.
