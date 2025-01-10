"""Tests for Hunter SDK client."""

import pytest
import responses

from hunter_sdk.client import HunterClient
from hunter_sdk.exceptions import HunterAPIError


@pytest.fixture
def client():
    """Create a HunterClient instance for testing."""
    return HunterClient(api_key="test_key")


@responses.activate
def test_verify_email_request(client):
    """Test email verification request formatting."""
    email = "test@example.com"
    mock_response = {
        "data": {
            "email": email,
            "score": 80,
            "status": "valid",
        },
    }
    
    responses.add(
        responses.GET,
        "https://api.hunter.io/v2/email-verifier",
        json=mock_response,
        status=200,
    )
    
    result = client.verify_email(email)
    assert result["email"] == email
    assert result["status"] == "valid"


@responses.activate
def test_client_error_handling(client):
    """Test client error handling."""
    responses.add(
        responses.GET,
        "https://api.hunter.io/v2/email-verifier",
        json={"errors": ["Invalid API key"]},
        status=401,
    )
    
    with pytest.raises(HunterAPIError) as exc:
        client.verify_email("test@example.com")
    assert "API request failed" in str(exc.value) 