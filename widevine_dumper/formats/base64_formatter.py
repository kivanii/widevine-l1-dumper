"""Base64 output formatter for extracted keys."""

import base64
import logging
from typing import List, Any


class Base64Formatter:
    """Format extracted keys in Base64 encoding."""

    def __init__(self):
        """Initialize Base64Formatter."""
        self.logger = logging.getLogger(__name__)

    def format(self, result: Any) -> str:
        """Format extraction result as Base64.
        
        Args:
            result: ExtractionResult object
            
        Returns:
            Base64 encoded string
        """
        lines = []
        lines.append(f"Device={result.device_id}")
        lines.append(f"Name={result.device_name}")
        lines.append(f"Time={result.timestamp}")
        lines.append(f"Version={result.widevine_version}")
        
        for key in result.keys:
            kid_b64 = base64.b64encode(key.kid.encode()).decode()
            key_b64 = base64.b64encode(key.key.encode()).decode()
            lines.append(f"KID[{key.key_type}]={kid_b64}")
            lines.append(f"KEY[{key.key_type}]={key_b64}")
        
        return "\n".join(lines)

    def format_keys(self, keys: List[Any]) -> str:
        """Format just the keys list as Base64.
        
        Args:
            keys: List of key objects
            
        Returns:
            Base64 encoded string
        """
        lines = []
        for i, key in enumerate(keys, 1):
            kid_b64 = base64.b64encode(key.kid.encode()).decode()
            key_b64 = base64.b64encode(key.key.encode()).decode()
            lines.append(f"Key{i}_KID={kid_b64}")
            lines.append(f"Key{i}_DATA={key_b64}")
        
        return "\n".join(lines)
