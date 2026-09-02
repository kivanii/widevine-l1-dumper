"""Device management and ADB communication."""

import subprocess
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Device:
    """Represents an Android device."""
    device_id: str
    device_name: str
    android_version: str
    is_rooted: bool = False
    widevine_support: bool = False


class DeviceManager:
    """Manages ADB device connections and communication."""

    def __init__(self):
        """Initialize DeviceManager."""
        self.logger = logging.getLogger(__name__)
        self.connected_device: Optional[str] = None
        self.devices: Dict[str, Device] = {}

    def list_devices(self) -> List[Device]:
        """List all connected Android devices.
        
        Returns:
            List of connected devices
        """
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip() and not line.startswith('*'):
                    parts = line.split()
                    if len(parts) >= 2:
                        device_id = parts[0]
                        device = Device(
                            device_id=device_id,
                            device_name="Unknown",
                            android_version="Unknown"
                        )
                        self.devices[device_id] = device
                        devices.append(device)
            
            self.logger.info(f"Found {len(devices)} device(s)")
            return devices
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to list devices: {e}")
            raise
        except FileNotFoundError:
            self.logger.error("ADB not found. Please install Android SDK Platform Tools.")
            raise

    def connect(self, device_id: str) -> bool:
        """Connect to a specific device.
        
        Args:
            device_id: The device ID to connect to
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Check if device is online
            result = subprocess.run(
                ["adb", "-s", device_id, "get-state"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip() == "device":
                self.connected_device = device_id
                self.logger.info(f"Connected to device: {device_id}")
                return True
            else:
                self.logger.warning(f"Device {device_id} is not in online state: {result.stdout.strip()}")
                return False
                
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to connect to device {device_id}: {e}")
            return False

    def is_rooted(self) -> bool:
        """Check if connected device is rooted.
        
        Returns:
            True if device is rooted, False otherwise
        """
        if not self.connected_device:
            self.logger.warning("No device connected")
            return False
            
        try:
            result = subprocess.run(
                ["adb", "-s", self.connected_device, "shell", "su", "-c", "id"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            is_root = "uid=0" in result.stdout
            self.logger.info(f"Device root status: {is_root}")
            return is_root
            
        except subprocess.TimeoutExpired:
            self.logger.warning("Root check timed out")
            return False
        except subprocess.CalledProcessError:
            return False

    def check_widevine_support(self) -> bool:
        """Check if device has Widevine L1 support.
        
        Returns:
            True if Widevine L1 is supported, False otherwise
        """
        if not self.connected_device:
            self.logger.warning("No device connected")
            return False
            
        try:
            # Check for widevine CDM property
            result = subprocess.run(
                ["adb", "-s", self.connected_device, "shell", 
                 "getprop", "ro.com.widevine.cachesize"],
                capture_output=True,
                text=True,
                check=True
            )
            
            has_widevine = len(result.stdout.strip()) > 0
            self.logger.info(f"Widevine support: {has_widevine}")
            return has_widevine
            
        except subprocess.CalledProcessError:
            self.logger.warning("Could not determine Widevine support")
            return False

    def execute_shell_command(self, command: str) -> str:
        """Execute a shell command on the connected device.
        
        Args:
            command: The shell command to execute
            
        Returns:
            Command output
            
        Raises:
            RuntimeError: If no device is connected
        """
        if not self.connected_device:
            raise RuntimeError("No device connected")
            
        try:
            result = subprocess.run(
                ["adb", "-s", self.connected_device, "shell", command],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Shell command failed: {e}")
            raise

    def push_file(self, local_path: str, remote_path: str) -> bool:
        """Push a file to the device.
        
        Args:
            local_path: Local file path
            remote_path: Remote device path
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected_device:
            self.logger.warning("No device connected")
            return False
            
        try:
            subprocess.run(
                ["adb", "-s", self.connected_device, "push", local_path, remote_path],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Pushed {local_path} to {remote_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to push file: {e}")
            return False

    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """Pull a file from the device.
        
        Args:
            remote_path: Remote device path
            local_path: Local file path to save to
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected_device:
            self.logger.warning("No device connected")
            return False
            
        try:
            subprocess.run(
                ["adb", "-s", self.connected_device, "pull", remote_path, local_path],
                check=True,
                capture_output=True
            )
            self.logger.info(f"Pulled {remote_path} to {local_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to pull file: {e}")
            return False
