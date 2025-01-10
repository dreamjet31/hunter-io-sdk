"""Storage implementations for Hunter SDK."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import threading

from .exceptions import StorageError


class BaseStorage(ABC):
    """Abstract base class for storage implementations."""

    @abstractmethod
    def create(self, key: str, value: Any) -> None:
        """Create a new record."""
        pass

    @abstractmethod
    def read(self, key: str) -> Optional[Any]:
        """Retrieve a record."""
        pass

    @abstractmethod
    def update(self, key: str, value: Any) -> None:
        """Update an existing record."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a record."""
        pass


class MemoryStorage(BaseStorage):
    """Thread-safe in-memory storage using dictionary."""

    def __init__(self) -> None:
        """Initialize empty storage with thread lock."""
        self._storage: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def create(self, key: str, value: Any) -> None:
        """Create a new record in storage.

        Args:
            key: Unique identifier for the record
            value: Data to store

        Raises:
            StorageError: If key already exists
        """
        with self._lock:
            if key in self._storage:
                raise StorageError(f'Record already exists: {key}')
            self._storage[key] = value

    def read(self, key: str) -> Optional[Any]:
        """Retrieve a record from storage.

        Args:
            key: Unique identifier for the record

        Returns:
            The stored value or None if not found
        """
        with self._lock:
            return self._storage.get(key)

    def update(self, key: str, value: Any) -> None:
        """Update an existing record.

        Args:
            key: Unique identifier for the record
            value: New data to store

        Raises:
            StorageError: If key doesn't exist
        """
        with self._lock:
            if key not in self._storage:
                raise StorageError(f'Record not found: {key}')
            self._storage[key] = value

    def delete(self, key: str) -> None:
        """Delete a record from storage.

        Args:
            key: Unique identifier for the record

        Raises:
            StorageError: If key doesn't exist
        """
        with self._lock:
            if key not in self._storage:
                raise StorageError(f'Record not found: {key}')
            del self._storage[key] 