"""Tests for Hunter SDK service."""

import pytest

from hunter_sdk.service import HunterService
from hunter_sdk.exceptions import ValidationError


def test_email_validation():
    """Test email validation logic."""
    service = HunterService(api_key="dummy_key")
    
    # Valid email should pass
    assert service._is_valid_email("test@example.com") is True
    
    # Invalid emails should fail
    assert service._is_valid_email("invalid-email") is False
    assert service._is_valid_email("@example.com") is False
    assert service._is_valid_email("test@") is False


def test_verify_email_validation_error():
    """Test that invalid emails raise ValidationError."""
    service = HunterService(api_key="dummy_key")
    
    with pytest.raises(ValidationError):
        service.verify_and_store_email("invalid-email") 