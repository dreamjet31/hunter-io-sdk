"""HTTP client for Hunter.io API."""

from typing import Any, Dict
import requests
from requests.exceptions import RequestException

from .exceptions import HunterAPIError


class HunterClient:
    """Client for interacting with Hunter.io API."""

    def __init__(self, api_key: str, base_url: str = 'https://api.hunter.io/v2') -> None:
        """Initialize the Hunter API client.

        Args:
            api_key: Your Hunter.io API key
            base_url: Base URL for the API (useful for testing)
        """
        self._api_key = api_key
        self._base_url = base_url.rstrip('/')
        self._session = requests.Session()

    def verify_email(self, email: str) -> Dict[str, Any]:
        """Verify email address using Hunter.io API.

        Args:
            email: Email address to verify

        Returns:
            Dict containing verification results

        Raises:
            HunterAPIError: If API request fails
        """
        try:
            response = self._make_request(
                'get',
                '/email-verifier',
                params={'email': email},
            )
            return response['data']
        except RequestException as exc:
            raise HunterAPIError(f'Email verification failed: {exc}') from exc

    def domain_search(
        self,
        domain: str,
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Search for email addresses on a domain.

        Args:
            domain: Domain to search
            limit: Maximum number of results (default: 10)
            offset: Results offset for pagination

        Returns:
            Dict containing search results

        Raises:
            HunterAPIError: If API request fails
        """
        try:
            response = self._make_request(
                'get',
                '/domain-search',
                params={
                    'domain': domain,
                    'limit': limit,
                    'offset': offset,
                },
            )
            return response['data']
        except RequestException as exc:
            raise HunterAPIError(f'Domain search failed: {exc}') from exc

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Hunter API.

        Args:
            method: HTTP method to use
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            JSON response from the API

        Raises:
            HunterAPIError: If the request fails
        """
        kwargs.setdefault('params', {})
        kwargs['params']['api_key'] = self._api_key

        response = self._session.request(
            method,
            f'{self._base_url}{endpoint}',
            **kwargs,
        )

        try:
            response.raise_for_status()
            return response.json()
        except (RequestException, ValueError) as exc:
            raise HunterAPIError(f'API request failed: {exc}') from exc 