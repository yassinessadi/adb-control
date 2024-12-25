# ADB Control

`adb-control` is a Python package that allows you to interact with Android devices through ADB (Android Debug Bridge). It provides various utilities such as listing devices, installing/uninstalling apps, and taking screenshots remotely from your connected Android devices.

## Features

- List connected devices
- Install and uninstall APKs
- Take screenshots on Android devices
- Manage media on Android devices

## Installation

You can install the `adb-control` package using pip.

```bash
pip install adb-control
```


Or you can clone the repository and install it locally:

```bash
git clone https://github.com/yassinessadi/adb-control.git
cd adb-control
pip install .
```

## Example Usage

Below is an example of how to use the package to interact with connected Android devices:

```python
from adb_control import DeviceManager, AppManager, MediaManager

# Initialize the managers
device_manager = DeviceManager()
app_manager = AppManager()
media_manager = MediaManager()

try:
    # List connected devices
    devices = device_manager.list_devices()
    print("Connected Devices:", devices)

    # Check if devices are connected
    if not devices:
        print("No devices connected. Please connect a device and try again.")
    else:
        # Take a screenshot on the first connected device
        screenshot_path = "screenshot.png"
        print(f"Taking screenshot and saving as {screenshot_path}")
        media_manager.take_screenshot(screenshot_path)

except Exception as e:
    print(f"Error: {e}")
```
