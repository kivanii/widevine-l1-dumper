"""CDM (Content Decryption Module) parsing utilities."""

import logging
import struct
from typing import Dict, Any, Optional


class CDMParser:
    """Parse Widevine CDM data structures."""

    def __init__(self):
        """Initialize CDMParser."""
        self.logger = logging.getLogger(__name__)

    def parse_license(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse a Widevine license from binary data.
        
        Args:
            data: Raw license binary data
            
        Returns:
            Parsed license dictionary or None if parsing fails
        """
        try:
            if not data or len(data) < 8:
                self.logger.warning("Invalid license data")
                return None

            # Parse header
            version = struct.unpack('>I', data[0:4])[0]
            flags = struct.unpack('>I', data[4:8])[0]

            return {
                "version": version,
                "flags": flags,
                "data": data.hex()
            }

        except Exception as e:
            self.logger.error(f"Failed to parse license: {e}")
            return None

    def extract_key_id(self, license_data: bytes) -> Optional[str]:
        """Extract Key ID from license data.
        
        Args:
            license_data: Raw license binary data
            
        Returns:
            Hex-encoded Key ID or None
        """
        try:
            # This is a simplified extraction
            # Real implementation would parse protobuf structures
            if len(license_data) >= 16:
                kid = license_data[0:16]
                return kid.hex()
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to extract key ID: {e}")
            return None

    def extract_key_material(self, license_data: bytes) -> Optional[str]:
        """Extract key material from license data.
        
        Args:
            license_data: Raw license binary data
            
        Returns:
            Hex-encoded key material or None
        """
        try:
            # Simplified extraction
            # Real implementation would decrypt and parse key material
            if len(license_data) >= 32:
                key = license_data[16:32]
                return key.hex()
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to extract key material: {e}")
            return None
