# 📦 AWS Integration Library — `libs.aws_messaging`

This module provides a structured abstraction over AWS SNS and SQS to implement a generic, extensible pub/sub mechanism. It enables both publishing typed events and consuming typed messages asynchronously using Pydantic validation.

---

## 📁 Module Structure

```
libs/
└── aws/
    └── messaging/
        ├── __init__.py
        ├── config.py            # Defines AWS config dataclass (region, keys, etc.)
        ├── client.py            # Wrapper for boto3 SNS and SQS clients
        ├── producer.py          # Generic publisher using Pydantic data
        ├── consumer.py          # Async consumer runner and dispatch system
        ├── subscription.py      # Registers actions to topics using Pydantic models
        ├── exceptions.py        # Custom exceptions
        └── tests/
            ├── unit/
            │   ├── test_producer.py
            │   ├── test_consumer.py
            │   └── test_subscription.py
            └── integration/
                ├── test_publish_real.py
                └── test_consume_real.py
```

---

## ⚙️ Component Overview

### `config.py`
- Contains `AWSMessagingConfig`:
  - `aws_access_key_id`
  - `aws_secret_access_key`
  - `region_name`
  - Optional: topic/queue name mappings
- Passed as an injected config to client and runners

### `client.py`
- Initializes `boto3` SNS and SQS clients using the config
- Wrapped to allow mocking for unit tests

### `producer.py`
- Generic publisher using Pydantic models and type hints
- Example façade:
  ```python
  def publish[T: BaseModel](topic: str, data: T) -> None
  ```

### `consumer.py`
- Manages async polling of a specific SQS queue
- Deserializes messages and validates with Pydantic model
- Invokes an action (callable) defined via subscription
- Handles retries and visibility timeout extension (future scope)

### `subscription.py`
- Allows registering handlers:
  ```python
  subscribe[T: BaseModel](topic: str, handler: Callable[[T], Awaitable[None]])
  ```

### `exceptions.py`
- Custom errors:
  - `InvalidMessageError`
  - `ValidationFailedError`
  - `SubscriptionNotFoundError`

---

## ✅ Testing Strategy (TDD)

### 🔹 Unit Tests

#### `test_producer.py`
- Should serialize valid Pydantic models into JSON
- Should send correctly to SNS using mocked boto3
- Should raise error if topic not found or credentials invalid

#### `test_consumer.py`
- Should poll and process valid SQS messages using mocked boto3
- Should validate payload with correct model and call the handler
- Should log or raise error for validation failure

#### `test_subscription.py`
- Should register multiple handlers for different topics
- Should dispatch messages to correct handler

---

### 🔸 Integration Tests (disabled by default)

#### `test_publish_real.py`
- Publishes real SNS message using valid credentials
- Verifies receipt in connected SQS queue

#### `test_consume_real.py`
- Listens to real queue, processes message and invokes action
- Should run end-to-end with live AWS topics and queues

---

## 🔐 Environment Variables (injected via config)

| Variable Name              | Purpose                            | Required | Default |
|----------------------------|------------------------------------|----------|---------|
| `AWS_ACCESS_KEY_ID`        | AWS credentials                    | ✅       | —       |
| `AWS_SECRET_ACCESS_KEY`    | AWS credentials                    | ✅       | —       |
| `AWS_REGION`               | Default AWS region                 | ✅       | —       |
| `AWS_TOPIC_NAME`           | The SNS topic name to publish to or consume from | ✅       | —       |

> These must be injected via `AWSMessagingConfig`, never read directly with `os.environ`.

⚠️ **Note**: This library is designed to operate with one topic per runtime process. Each topic will implicitly correspond to a single SQS queue for consumption. The queue name is derived from the topic name and environment, and does not need to be specified manually.

---

## 🤖 LLM Implementation Tips

- Use `Generic[T: BaseModel]` in producers and consumers
- Ensure async polling runs continuously with proper backoff or error handling
- Allow dependency injection of client and config for tests
- Expose simple façades: `publish_event(...)`, `run_consumer(...)`
- Avoid direct `boto3` usage outside of `client.py`

---
