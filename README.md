# Widevine L1 Dumper

A powerful tool for extracting and dumping Widevine L1 DRM keys from Android devices. This tool enables research into DRM systems and content protection mechanisms.

## Features

- **L1 Key Extraction**: Extract Widevine L1 keys from compatible Android devices
- **Device Discovery**: Automatic detection and enumeration of connected devices
- **Key Dumping**: Save extracted keys in multiple formats (JSON, HEX, Base64)
- **License Validation**: Verify and validate extracted licenses
- **Batch Processing**: Process multiple devices in sequence
- **Logging**: Comprehensive logging of all operations

## Requirements

- Python 3.8+
- Android Debug Bridge (ADB)
- Connected Android device with Widevine L1 capability
- Root access or custom ROM with necessary permissions

## Installation

### Prerequisites

1. Install Python 3.8 or higher
2. Install ADB (Android Debug Bridge)
3. Ensure your device has USB debugging enabled

### Setup

```bash
git clone https://github.com/kivanii/widevine-l1-dumper.git
cd widevine-l1-dumper
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python widevine_dumper.py
```

### Command Line Options

```bash
# Dump keys from a specific device
python widevine_dumper.py --device <device_id>

# Specify output format
python widevine_dumper.py --format json  # json, hex, base64

# Save to custom location
python widevine_dumper.py --output /path/to/output

# Verbose logging
python widevine_dumper.py --verbose

# Process multiple devices
python widevine_dumper.py --all-devices

# Extract specific CDM type
python widevine_dumper.py --cdm-type widevine_l1
```

### Example

```bash
# List connected devices
python widevine_dumper.py --list-devices

# Extract L1 keys from first device
python widevine_dumper.py --device emulator-5554 --format json --verbose

# Dump and validate
python widevine_dumper.py --device <id> --validate --output ./keys/
```

## Output Formats

### JSON Format
```json
{
  "device_id": "emulator-5554",
  "device_name": "Android",
  "widevine_version": "1.0",
  "keys": [
    {
      "kid": "...",
      "key": "...",
      "key_type": "content"
    }
  ],
  "timestamp": "2026-09-02T12:00:00Z"
}
```

### HEX Format
```
Device ID: emulator-5554
KID: 0x...
KEY: 0x...
```

## Technical Details

### Widevine DRM Levels

- **L1**: Cryptographic keys stored in Trusted Execution Environment (TEE)
- **L2**: Keys stored in device memory
- **L3**: Software-based key management

This tool focuses on L1 extraction from compatible devices.

### Architecture

```
widevine_dumper/
├── core/
│   ├── device_manager.py      # ADB device communication
│   ├── key_extractor.py       # Key extraction logic
│   └── cdm_parser.py          # CDM data parsing
├── formats/
│   ├── json_formatter.py
│   ├── hex_formatter.py
│   └── base64_formatter.py
├── utils/
│   ├── logger.py
│   └── validators.py
└── widevine_dumper.py         # Main entry point
```

## Security & Legal

⚠️ **Important Notice**

This tool is intended for:
- Research and educational purposes
- Security testing on devices you own
- Legitimate DRM research

Ensure compliance with local laws and regulations. Widevine DRM circumvention may be restricted in your jurisdiction.

## Troubleshooting

### Device Not Found
```bash
# Verify ADB connection
adb devices

# Restart ADB daemon
adb kill-server
adb start-server
```

### Permission Denied
Ensure device is rooted or running custom ROM with appropriate permissions:
```bash
adb root
adb remount
```

### No Keys Found
- Verify device supports Widevine L1
- Check device hasn't encrypted CDM data
- Ensure required services are running

## API Reference

### DeviceManager
```python
from widevine_dumper.core import DeviceManager

manager = DeviceManager()
devices = manager.list_devices()
manager.connect(device_id)
```

### KeyExtractor
```python
from widevine_dumper.core import KeyExtractor

extractor = KeyExtractor(device)
keys = extractor.extract_keys()
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations in their jurisdiction. The authors assume no liability for misuse.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

## References

- [Widevine DRM Documentation](https://www.widevine.com)
- [Android Security & Privacy](https://developer.android.com/security)
- [ADB Documentation](https://developer.android.com/studio/command-line/adb)

---

**Last Updated**: 2026-09-02
