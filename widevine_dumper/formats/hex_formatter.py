"""Hexadecimal output formatter for extracted keys."""

import logging
from typing import List, Any
from dataclasses import asdict


class HexFormatter:
    """Format extracted keys in hexadecimal format."""

    def __init__(self):
        """Initialize HexFormatter."""
        self.logger = logging.getLogger(__name__)

    def format(self, result: Any) -> str:
        """Format extraction result as HEX.
        
        Args:
            result: ExtractionResult object
            
        Returns:
            Formatted HEX string
        """
        lines = []
        lines.append(f"Device ID: {result.device_id}")
        lines.append(f"Device Name: {result.device_name}")
        lines.append(f"Timestamp: {result.timestamp}")
        lines.append(f"Widevine Version: {result.widevine_version}")
        lines.append(f"Success: {result.success}")
        
        if result.error_message:
            lines.append(f"Error: {result.error_message}")
        
        lines.append("\nKeys:")
        lines.append("-" * 80)
        
        for key in result.keys:
            lines.append(f"KID: 0x{key.kid}")
            lines.append(f"KEY: 0x{key.key}")
            lines.append(f"Type: {key.key_type}")
            lines.append(f"Algorithm: {key.algorithm}")
            lines.append("-" * 80)
        
        return "\n".join(lines)

    def format_keys(self, keys: List[Any]) -> str:
        """Format just the keys list as HEX.
        
        Args:
            keys: List of key objects
            
        Returns:
            Formatted HEX string
        """
        lines = []
        for i, key in enumerate(keys, 1):
            lines.append(f"Key #{i}")
            lines.append(f"  KID: 0x{key.kid}")
            lines.append(f"  KEY: 0x{key.key}")
            lines.append(f"  Type: {key.key_type}")
            lines.append()
        
        return "\n".join(lines)
