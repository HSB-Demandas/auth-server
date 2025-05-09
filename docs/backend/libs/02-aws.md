# 📦 AWS Integration Library — `libs.aws_messaging`

A structured abstraction over AWS SNS and SQS for implementing a generic, extensible pub/sub mechanism with Pydantic validation.

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Module Structure](#module-structure)
- [Components](#components)
- [Testing Strategy](#testing-strategy)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)

## 🏗 Architecture

### Core Principles

1. **Type Safety**: Uses Pydantic for message validation
2. **Async Support**: Built for async operations
3. **Extensibility**: Flexible subscription system
4. **Error Handling**: Robust error management
5. **Testability**: Mockable interfaces

## 📁 Module Structure

```
libs/
└── aws/
    └── messaging/
        ├── __init__.py
        ├── config.py            # Configuration and settings
        ├── client.py            # AWS client wrapper
        ├── producer.py          # Message publishing
        ├── consumer.py          # Message consumption
        ├── subscription.py      # Event handling
        ├── exceptions.py        # Error handling
        ├── types.py             # Message types and enums
        └── tests/
            ├── unit/
            │   ├── test_producer.py
            │   ├── test_consumer.py
            │   └── test_subscription.py
            └── integration/
                ├── test_publish_real.py
                └── test_consume_real.py
```

## ⚙️ Components

### 1. Configuration (`config.py`)

- **Purpose**: AWS service configuration
- **Key Components**:
  - `AWSMessagingConfig` pydantic model
  - Service endpoint configuration
  - Retry strategy settings

### 2. Client (`client.py`)

- **Purpose**: AWS service integration
- **Features**:
  - SNS and SQS client initialization
  - Request retry logic
  - Error handling
  - Connection pooling

### 3. Producer (`producer.py`)

- **Purpose**: Message publishing
- **API**:
  ```python
  def publish[
      T: BaseModel,
      Topic: str
  ](config: AWSMessagingConfig, data: T) -> None
  ```
- **Features**:
  - Message validation
  - Topic routing
  - Error handling
  - Retry logic

### 4. Consumer (`consumer.py`)

- **Purpose**: Message consumption
- **API**:
  ```python
  async def consume[
      T: BaseModel,
      Queue: str
  ](config: AWSMessagingConfig, handler: Callable[[T], Awaitable[None]]) -> None
  ```
- **Features**:
  - Async message processing
  - Message validation
  - Error handling
  - Retry management

### 5. Subscription (`subscription.py`)

- **Purpose**: Event handling registration
- **API**:
  ```python
  def subscribe[
      T: BaseModel,
      Topic: str
  ](handler: Callable[[T], Awaitable[None]]) -> None
  ```
- **Features**:
  - Typed event registration
  - Handler management
  - Topic routing
  - Error handling

### 6. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `InvalidMessageError`
  - `ValidationFailedError`
  - `SubscriptionNotFoundError`
  - `AWSConnectionError`
  - `MessageProcessingError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Message validation
  - Topic routing
  - Error handling
  - Retry logic
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Async operations

### Integration Tests

- **Real Integration**:
  - SNS message publishing
  - SQS message consumption
  - Error handling
  - Retry logic
- **Requirements**:
  - AWS test credentials
  - Test topics and queues
  - Mock AWS services
  - Test messages

## 🔐 Environment Variables

No direct environment variable access inside the library. Configuration must be passed through `AWSMessagingConfig`.

If required by the consuming app, recommended environment variables:

| Variable Name     | Purpose                      | Required | Default |
|-------------------|------------------------------|----------|---------|
| `AWS_ACCESS_KEY_ID`  | AWS access key ID           | ✅       | —       |
| `AWS_SECRET_ACCESS_KEY`   | AWS secret access key      | ✅       | —       |
| `AWS_REGION_NAME`  | AWS region name              | ✅       | —       |
| `AWS_TOPIC_MAP`    | JSON mapping of topics       | ❌       | —       |
| `AWS_QUEUE_MAP`    | JSON mapping of queues       | ❌       | —       |
| `AWS_RETRY_ATTEMPTS` | Retry attempts              | ❌       | 3       |
| `AWS_TIMEOUT`      | Operation timeout (seconds)  | ❌       | 30      |

## 🔄 Usage Examples

### Basic Message Publishing

```python
from libs.aws.config import AWSMessagingConfig
from libs.aws.producer import publish
from pydantic import BaseModel

class UserCreatedEvent(BaseModel):
    user_id: str
    email: str
    created_at: datetime

config = AWSMessagingConfig(
    aws_access_key_id="your_key",
    aws_secret_access_key="your_secret",
    region_name="us-east-1"
)

# Publish event
await publish[
    UserCreatedEvent,
    "user-events"
](
    config=config,
    data=UserCreatedEvent(
        user_id="123",
        email="user@example.com",
        created_at=datetime.now()
    )
)
```

### Message Consumption

```python
from libs.aws.config import AWSMessagingConfig
from libs.aws.consumer import consume
from pydantic import BaseModel

async def handle_user_created(event: UserCreatedEvent):
    # Process the event
    pass

config = AWSMessagingConfig(
    aws_access_key_id="your_key",
    aws_secret_access_key="your_secret",
    region_name="us-east-1"
)

# Start consumer
await consume[
    UserCreatedEvent,
    "user-events-queue"
](
    config=config,
    handler=handle_user_created
)
```

## 🛡 Security Considerations

- **Message Encryption**: Support for encrypted messages
- **Access Control**: IAM role management
- **Error Masking**: Secure error handling
- **Audit Logging**: Message tracking
- **Rate Limiting**: AWS service rate limits
- **Connection Security**: TLS/SSL enforcement

## 🚀 Performance Considerations

- **Connection Pooling**: Efficient AWS connections
- **Batch Processing**: Optimized message handling
- **Retry Strategy**: Exponential backoff
- **Message Validation**: Early validation
- **Error Handling**: Fast failure paths
- **Async Operations**: Non-blocking I/O

---

> **Note**: This library is designed for production use with AWS services. For development, use AWS LocalStack or similar test environments.

> These must be injected via `AWSMessagingConfig`, never read directly with `os.environ`.

⚠️ **Note**: This library is designed to operate with one topic per runtime process. Each topic will implicitly correspond to a single SQS queue for consumption. The queue name is derived from the topic name and environment, and does not need to be specified manually.

## 🤖 LLM Implementation Tips

- Use `Generic[T: BaseModel]` in producers and consumers
- Ensure async polling runs continuously with proper backoff or error handling
- Allow dependency injection of client and config for tests
- Expose simple façades: `publish_event(...)`, `run_consumer(...)`
- Avoid direct `boto3` usage outside of `client.py`

---
