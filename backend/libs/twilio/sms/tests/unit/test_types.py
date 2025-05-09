import pytest
from enum import Enum

from libs.twilio.sms.types import (
    VerificationChannel, VerificationStatus, SMSDeliveryResult, VerificationResult
)


def test_verification_channel_enum():
    """Test that VerificationChannel is properly defined as an Enum"""
    assert issubclass(VerificationChannel, Enum)
    assert VerificationChannel.SMS.value == "sms"
    assert VerificationChannel.CALL.value == "call"
    assert VerificationChannel.EMAIL.value == "email"


def test_verification_status_enum():
    """Test that VerificationStatus is properly defined as an Enum"""
    assert issubclass(VerificationStatus, Enum)
    assert VerificationStatus.PENDING.value == "pending"
    assert VerificationStatus.APPROVED.value == "approved"
    assert VerificationStatus.CANCELED.value == "canceled"
    assert VerificationStatus.FAILED.value == "failed"


def test_sms_delivery_result():
    """Test that SMSDeliveryResult is properly defined"""
    # Create an instance with minimal required fields
    result = SMSDeliveryResult(
        success=True,
        message_sid="SM123456",
        to="+1234567890"
    )

    assert result.success is True
    assert result.message_sid == "SM123456"
    assert result.to == "+1234567890"
    assert result.error_code is None
    assert result.error_message is None

    # Create an instance with error information
    error_result = SMSDeliveryResult(
        success=False,
        to="+1234567890",
        error_code="E123",
        error_message="Invalid phone number"
    )

    assert error_result.success is False
    assert error_result.to == "+1234567890"
    assert error_result.error_code == "E123"
    assert error_result.error_message == "Invalid phone number"
    assert error_result.message_sid is None


def test_verification_result():
    """Test that VerificationResult is properly defined"""
    # Create an instance with minimal required fields
    result = VerificationResult(
        success=True,
        to="+1234567890",
        status=VerificationStatus.PENDING
    )

    assert result.success is True
    assert result.to == "+1234567890"
    assert result.status == VerificationStatus.PENDING
    assert result.error_code is None
    assert result.error_message is None

    # Create an instance with error information
    error_result = VerificationResult(
        success=False,
        to="+1234567890",
        status=VerificationStatus.FAILED,
        error_code="E456",
        error_message="Verification failed"
    )

    assert error_result.success is False
    assert error_result.to == "+1234567890"
    assert error_result.status == VerificationStatus.FAILED
    assert error_result.error_code == "E456"
    assert error_result.error_message == "Verification failed"
