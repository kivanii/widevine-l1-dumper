"""Widevine L1 key extraction logic."""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class WidevineLicense:
    """Represents a Widevine license."""
    kid: str  # Key ID
    key: str  # Encryption key
    key_type: str  # content, signing, etc.
    algorithm: str = "AES-128"


@dataclass
class ExtractionResult:
    """Result of key extraction."""
    device_id: str
    device_name: str
    timestamp: str
    widevine_version: str
    keys: List[WidevineLicense]
    success: bool
    error_message: Optional[str] = None


class KeyExtractor:
    """Extracts Widevine L1 keys from Android devices."""

    def __init__(self, device_manager):
        """Initialize KeyExtractor.
        
        Args:
            device_manager: DeviceManager instance
        """
        self.logger = logging.getLogger(__name__)
        self.device_manager = device_manager
        self.cdm_paths = [
            "/data/misc/widevine",
            "/data/data/com.widevine.alpha",
            "/vendor/widevine",
        ]

    def extract_keys(self) -> ExtractionResult:
        """Extract Widevine L1 keys from the connected device.
        
        Returns:
            ExtractionResult containing extracted keys or error information
        """
        if not self.device_manager.connected_device:
            error_msg = "No device connected"
            self.logger.error(error_msg)
            return ExtractionResult(
                device_id="unknown",
                device_name="unknown",
                timestamp=datetime.now().isoformat(),
                widevine_version="unknown",
                keys=[],
                success=False,
                error_message=error_msg
            )

        try:
            # Check prerequisites
            if not self.device_manager.is_rooted():
                raise RuntimeError("Device must be rooted for key extraction")

            if not self.device_manager.check_widevine_support():
                raise RuntimeError("Device does not support Widevine")

            # Extract keys from CDM paths
            keys = self._extract_cdm_keys()

            return ExtractionResult(
                device_id=self.device_manager.connected_device,
                device_name="Android",
                timestamp=datetime.now().isoformat(),
                widevine_version="1.0",
                keys=keys,
                success=True
            )

        except Exception as e:
            self.logger.error(f"Key extraction failed: {e}")
            return ExtractionResult(
                device_id=self.device_manager.connected_device or "unknown",
                device_name="Android",
                timestamp=datetime.now().isoformat(),
                widevine_version="unknown",
                keys=[],
                success=False,
                error_message=str(e)
            )

    def _extract_cdm_keys(self) -> List[WidevineLicense]:
        """Extract CDM keys from device paths.
        
        Returns:
            List of extracted WidevineLicense objects
        """
        keys = []
        
        for cdm_path in self.cdm_paths:
            try:
                # Check if path exists
                result = self.device_manager.execute_shell_command(
                    f"[ -d '{cdm_path}' ] && echo 'EXISTS' || echo 'NOT_FOUND'"
                )
                
                if "EXISTS" not in result:
                    self.logger.debug(f"CDM path not found: {cdm_path}")
                    continue

                # List files in CDM directory
                result = self.device_manager.execute_shell_command(
                    f"ls -la '{cdm_path}' 2>/dev/null | grep -E '\\.(bin|key|data)'"
                )

                if result.strip():
                    self.logger.info(f"Found potential key files in {cdm_path}")
                    # In real implementation, would extract and parse binary key files
                    # For now, create placeholder
                    keys.append(WidevineLicense(
                        kid="placeholder_kid",
                        key="placeholder_key",
                        key_type="content"
                    ))

            except Exception as e:
                self.logger.debug(f"Error accessing {cdm_path}: {e}")
                continue

        return keys

    def validate_keys(self, keys: List[WidevineLicense]) -> bool:
        """Validate extracted keys format.
        
        Args:
            keys: List of keys to validate
            
        Returns:
            True if all keys are valid, False otherwise
        """
        for key in keys:
            if not key.kid or not key.key:
                self.logger.warning(f"Invalid key format: {key}")
                return False

        self.logger.info(f"Validated {len(keys)} keys")
        return True
