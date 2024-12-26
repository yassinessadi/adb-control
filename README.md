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
from adb_control import DeviceManager, AppManager, MediaManager,ConnectManager,InputManager,KeyEvent
import time
device_manager = DeviceManager()
app_manager = AppManager()
media_manager = MediaManager()
connect_manager = ConnectManager()
input_manager = InputManager()

try:
    devices = device_manager.list_devices()
    print("Connected Devices:", devices)

    if not devices:
        print("No devices connected. Please connect a device and try again.")
    else:
        screenshot_path = "EC.png"
        print(f"Taking screenshot and saving as {screenshot_path}")
        media_manager.take_screenshot(screenshot_path)
        try:
            input_manager.keyevent(keyevent=KeyEvent.KEYCODE_POWER.value)
            time.sleep(1.5)
            input_manager.swipe(500 ,1920 ,500 ,500)
            time.sleep(1.5)
            input_manager.text("123456")
            time.sleep(1.5)
            input_manager.keyevent(keyevent=KeyEvent.KEYCODE_ENTER.value)

        except Exception as e:
            print(f"Error during put file to device: {e}")

except Exception as e:
    print(f"Error: {e}")
```
