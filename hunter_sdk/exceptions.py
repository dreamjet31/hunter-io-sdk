"""Custom exceptions for the Hunter SDK."""


class HunterAPIError(Exception):
    """Base exception for Hunter API errors."""


class StorageError(Exception):
    """Base exception for storage errors."""


class ValidationError(Exception):
    """Base exception for validation errors.""" 