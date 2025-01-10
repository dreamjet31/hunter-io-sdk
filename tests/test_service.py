"""Tests for Hunter SDK service."""

import pytest
import responses

from hunter_sdk.service import HunterService
from hunter_sdk.exceptions import ValidationError, HunterAPIError
from hunter_sdk.storage import MemoryStorage


@pytest.fixture
def service():
    """Create a HunterService instance for testing."""
    return HunterService(api_key="test_key")


@pytest.fixture
def mock_storage():
    """Create a clean MemoryStorage instance."""
    return MemoryStorage()


def test_email_validation(service):
    """Test email validation logic."""
    # Valid emails
    assert service._is_valid_email("test@example.com") is True
    assert service._is_valid_email("user.name+tag@example.co.uk") is True
    assert service._is_valid_email("x@y.z") is True
    
    # Invalid emails
    assert service._is_valid_email("invalid-email") is False
    assert service._is_valid_email("@example.com") is False
    assert service._is_valid_email("test@") is False
    assert service._is_valid_email("test@.com") is False
    assert service._is_valid_email("") is False


def test_verify_email_validation_error(service):
    """Test that invalid emails raise ValidationError."""
    with pytest.raises(ValidationError) as exc:
        service.verify_and_store_email("invalid-email")
    assert "Invalid email format" in str(exc.value)


@responses.activate
def test_verify_email_success(service):
    """Test successful email verification."""
    email = "test@example.com"
    mock_response = {
        "data": {
            "email": email,
            "score": 80,
            "status": "valid",
        },
    }
    
    # Mock the API response
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier",
        json=mock_response,
        status=200,
    )
    
    result = service.verify_and_store_email(email)
    assert result["email"] == email
    assert result["status"] == "valid"
    
    # Verify it was stored
    stored = service.get_email_verification(email)
    assert stored == result


@responses.activate
def test_verify_email_api_error(service):
    """Test handling of API errors."""
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/email-verifier",
        json={"errors": ["API Error"]},
        status=400,
    )
    
    with pytest.raises(HunterAPIError):
        service.verify_and_store_email("test@example.com")


def test_storage_operations(mock_storage):
    """Test storage CRUD operations."""
    key = "test@example.com"
    data = {"status": "valid"}
    
    # Create
    mock_storage.create(key, data)
    assert mock_storage.read(key) == data
    
    # Update
    new_data = {"status": "invalid"}
    mock_storage.update(key, new_data)
    assert mock_storage.read(key) == new_data
    
    # Delete
    mock_storage.delete(key)
    assert mock_storage.read(key) is None


@responses.activate
def test_domain_search(service):
    """Test domain search functionality."""
    domain = "example.com"
    mock_response = {
        "data": {
            "domain": domain,
            "emails": [
                {"value": "test1@example.com"},
                {"value": "test2@example.com"},
            ],
        },
    }
    
    responses.add(
        responses.GET,
        f"https://api.hunter.io/v2/domain-search",
        json=mock_response,
        status=200,
    )
    
    result = service.search_domain(domain)
    assert result["domain"] == domain
    assert len(result["emails"]) == 2
    
    # Verify domain results were stored
    stored = service.get_email_verification(f"domain:{domain}")
    assert stored == result


def test_update_existing_verification(service):
    """Test updating existing email verification."""
    email = "test@example.com"
    initial_data = {"status": "valid"}
    updated_data = {"status": "invalid"}
    
    # Store initial data
    service._storage.create(email, initial_data)
    assert service.get_email_verification(email) == initial_data
    
    # Update with new data
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier",
            json={"data": updated_data},
            status=200,
        )
        service.verify_and_store_email(email, update_existing=True)
    
    assert service.get_email_verification(email) == updated_data


def test_email_normalization(service):
    """Test email address normalization."""
    original = "Test.User+TAG@Example.COM"
    normalized = "test.user+tag@example.com"
    
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"https://api.hunter.io/v2/email-verifier",
            json={"data": {"email": normalized}},
            status=200,
        )
        service.verify_and_store_email(original)
    
    # Should be able to retrieve using either format
    assert service.get_email_verification(original) == service.get_email_verification(normalized) 