#!/usr/bin/env python3
"""Main entry point for Widevine L1 Dumper."""

import sys
import argparse
import os
from pathlib import Path

from widevine_dumper.core import DeviceManager, KeyExtractor
from widevine_dumper.formats import JSONFormatter, HexFormatter, Base64Formatter
from widevine_dumper.utils import Logger


class WidevineL1Dumper:
    """Main application class."""

    def __init__(self):
        """Initialize the dumper."""
        self.device_manager = DeviceManager()
        self.key_extractor = KeyExtractor(self.device_manager)
        self.logger = Logger.get_logger("main")

    def list_devices(self) -> None:
        """List connected Android devices."""
        print("Scanning for connected devices...")
        try:
            devices = self.device_manager.list_devices()
            if not devices:
                print("No devices found.")
                return
            
            print(f"\nFound {len(devices)} device(s):\n")
            for i, device in enumerate(devices, 1):
                print(f"{i}. {device.device_id}")
                print(f"   Name: {device.device_name}")
                print(f"   Android: {device.android_version}")
                print()
        except Exception as e:
            self.logger.error(f"Failed to list devices: {e}")
            sys.exit(1)

    def extract_keys(self, device_id: str, output_format: str = "json", 
                    output_file: str = None) -> None:
        """Extract Widevine L1 keys from device.
        
        Args:
            device_id: Target device ID
            output_format: Output format (json, hex, base64)
            output_file: File to save output (if None, prints to stdout)
        """
        try:
            print(f"Connecting to device: {device_id}")
            if not self.device_manager.connect(device_id):
                self.logger.error(f"Failed to connect to device: {device_id}")
                sys.exit(1)
            
            print("Extracting Widevine L1 keys...")
            result = self.key_extractor.extract_keys()
            
            if result.success:
                print(f"Successfully extracted {len(result.keys)} key(s)")
            else:
                print(f"Extraction failed: {result.error_message}")
                sys.exit(1)
            
            # Format output
            if output_format == "json":
                formatter = JSONFormatter()
            elif output_format == "hex":
                formatter = HexFormatter()
            elif output_format == "base64":
                formatter = Base64Formatter()
            else:
                raise ValueError(f"Unknown format: {output_format}")
            
            output = formatter.format(result)
            
            # Save or print
            if output_file:
                os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
                with open(output_file, "w") as f:
                    f.write(output)
                print(f"Output saved to: {output_file}")
            else:
                print("\nExtracted Keys:")
                print("-" * 80)
                print(output)
        
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Widevine L1 Dumper - Extract Widevine L1 DRM keys from Android devices"
    )
    
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List connected Android devices"
    )
    
    parser.add_argument(
        "--device",
        type=str,
        help="Target device ID for key extraction"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "hex", "base64"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (if not specified, prints to stdout)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--log-file",
        type=str,
        default="widevine_dumper.log",
        help="Log file path"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    Logger.setup(
        log_level=log_level,
        log_file=args.log_file if args.verbose else None,
        console_output=True
    )
    
    dumper = WidevineL1Dumper()
    
    if args.list_devices:
        dumper.list_devices()
    elif args.device:
        dumper.extract_keys(args.device, args.format, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
