"""JSON output formatter for extracted keys."""

import json
import logging
from typing import Dict, Any, List
from dataclasses import asdict


class JSONFormatter:
    """Format extracted keys as JSON."""

    def __init__(self):
        """Initialize JSONFormatter."""
        self.logger = logging.getLogger(__name__)

    def format(self, result: Any) -> str:
        """Format extraction result as JSON.
        
        Args:
            result: ExtractionResult object
            
        Returns:
            JSON string
        """
        try:
            data = asdict(result)
            # Convert dataclass objects to dicts
            if "keys" in data and data["keys"]:
                data["keys"] = [asdict(key) for key in data["keys"]]
            
            return json.dumps(data, indent=2)
        except Exception as e:
            self.logger.error(f"JSON formatting failed: {e}")
            return json.dumps({"error": str(e)})

    def format_keys(self, keys: List[Any]) -> str:
        """Format just the keys list as JSON.
        
        Args:
            keys: List of key objects
            
        Returns:
            JSON string
        """
        try:
            keys_data = [asdict(key) for key in keys]
            return json.dumps({"keys": keys_data}, indent=2)
        except Exception as e:
            self.logger.error(f"Key formatting failed: {e}")
            return json.dumps({"error": str(e)})
