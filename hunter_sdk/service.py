"""Service layer for Hunter SDK."""

import re
from typing import Any, Dict, Optional, Pattern

from .client import HunterClient
from .storage import BaseStorage, MemoryStorage
from .exceptions import ValidationError, StorageError


class HunterService:
    """Service for handling Hunter.io operations with storage."""

    # RFC 5322 compliant email regex
    EMAIL_PATTERN: Pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    )

    def __init__(
        self,
        api_key: str,
        storage: Optional[BaseStorage] = None,
    ) -> None:
        """Initialize the Hunter service.

        Args:
            api_key: Hunter.io API key
            storage: Optional storage instance (defaults to MemoryStorage)
        """
        self._client = HunterClient(api_key)
        self._storage = storage or MemoryStorage()

    def verify_and_store_email(
        self,
        email: str,
        update_existing: bool = False,
    ) -> Dict[str, Any]:
        """Verify email and store results.

        Args:
            email: Email address to verify
            update_existing: Whether to update existing records

        Returns:
            Verification results

        Raises:
            ValidationError: If email format is invalid
        """
        email = email.lower().strip()
        if not self._is_valid_email(email):
            raise ValidationError(f'Invalid email format: {email}')

        result = self._client.verify_email(email)

        try:
            if update_existing:
                self._storage.update(email, result)
            else:
                self._storage.create(email, result)
        except StorageError:
            if update_existing:
                self._storage.create(email, result)
            else:
                self._storage.update(email, result)

        return result

    def get_email_verification(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored verification results.

        Args:
            email: Email address to look up

        Returns:
            Stored verification results or None if not found
        """
        email = email.lower().strip()
        return self._storage.read(email)

    def search_domain(
        self,
        domain: str,
        store_results: bool = True,
    ) -> Dict[str, Any]:
        """Search for email addresses on a domain.

        Args:
            domain: Domain to search
            store_results: Whether to store the results

        Returns:
            Domain search results
        """
        domain = domain.lower().strip()
        results = self._client.domain_search(domain)

        if store_results:
            self._storage.create(f'domain:{domain}', results)

        return results

    @classmethod
    def _is_valid_email(cls, email: str) -> bool:
        """Validate email format using RFC 5322 regex.

        Args:
            email: Email address to validate

        Returns:
            True if email format is valid
        """
        return bool(cls.EMAIL_PATTERN.match(email)) 