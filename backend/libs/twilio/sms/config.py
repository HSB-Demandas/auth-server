from typing import Optional, Self

from pydantic import BaseModel, field_validator


class TwilioConfig(BaseModel):
    """Configuration for Twilio SMS service"""
    account_sid: str
    auth_token: str
    from_number: str
    service_sid: Optional[str] = None

    @field_validator('from_number')
    def validate_phone(cls: Self, v: str) -> str:
        """Validate that phone number starts with +"""
        if not v.startswith('+'):
            raise ValueError('Phone number must start with +')
        return v
