"""Validation utilities."""

import logging
import re
from typing import Any


class Validator:
    """Validate data structures and formats."""

    def __init__(self):
        """Initialize Validator."""
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def is_valid_device_id(device_id: str) -> bool:
        """Validate Android device ID format.
        
        Args:
            device_id: Device ID string
            
        Returns:
            True if valid, False otherwise
        """
        if not device_id:
            return False
        # Device IDs are alphanumeric, may contain colons or hyphens
        return bool(re.match(r'^[a-zA-Z0-9:_-]+$', device_id))

    @staticmethod
    def is_valid_hex(hex_string: str) -> bool:
        """Validate hexadecimal string.
        
        Args:
            hex_string: String to validate
            
        Returns:
            True if valid hex, False otherwise
        """
        try:
            int(hex_string, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_key_format(key: str) -> bool:
        """Validate key format.
        
        Args:
            key: Key string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not key:
            return False
        # Keys should be hex or base64
        return Validator.is_valid_hex(key) or Validator.is_valid_base64(key)

    @staticmethod
    def is_valid_base64(data: str) -> bool:
        """Validate Base64 format.
        
        Args:
            data: String to validate
            
        Returns:
            True if valid base64, False otherwise
        """
        import base64
        try:
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False
