from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VerificationChannel(str, Enum):
    """Verification channel types supported by Twilio"""
    SMS = "sms"
    CALL = "call"
    EMAIL = "email"


class VerificationStatus(str, Enum):
    """Verification status types returned by Twilio"""
    PENDING = "pending"
    APPROVED = "approved"
    CANCELED = "canceled"
    FAILED = "failed"


class SMSDeliveryResult(BaseModel):
    """Result of an SMS delivery attempt"""
    success: bool = Field(..., description="Whether the SMS was successfully sent")
    to: str = Field(..., description="The phone number the SMS was sent to")
    message_sid: Optional[str] = Field(
        None, description="Twilio message SID if successful"
    )
    error_code: Optional[str] = Field(None, description="Error code if unsuccessful")
    error_message: Optional[str] = Field(
        None, description="Error message if unsuccessful"
    )


class VerificationResult(BaseModel):
    """Result of a verification attempt"""
    success: bool = Field(
        ..., description="Whether the verification was successfully initiated"
    )
    to: str = Field(..., description="The phone number the verification was sent to")
    status: VerificationStatus = Field(
        ..., description="The status of the verification"
    )
    error_code: Optional[str] = Field(None, description="Error code if unsuccessful")
    error_message: Optional[str] = Field(
        None, description="Error message if unsuccessful"
    )
