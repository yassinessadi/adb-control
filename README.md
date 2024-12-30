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


## Setup ADB
To use this package, you must have ADB set up on your machine. Follow the instructions below to get started:

### Install ADB:

On Windows: Download the ADB platform-tools and extract them to a folder.
On macOS/Linux: You can install ADB through your package
### manager:

```bash
# For macOS
brew install android-platform-tools

# For Ubuntu/Linux
sudo apt update
sudo apt install android-tools-adb
```
### Enable Developer Mode on your Android device:
Go to Settings > About phone and tap "Build number" seven times to enable Developer Options.
Go to Settings > Developer options, then enable "USB debugging."
Connect your device:

Connect your Android device via USB cable.
Verify the connection with the following command:
```bash
adb devices
```

If it's your first time connecting, you may need to authorize your computer on your Android device.
Wireless Debugging (optional):

To connect wirelessly, make sure both your computer and Android device are on the same network.
Run the following command to connect wirelessly:

```bash
adb tcpip 5555
adb connect <device_ip_address>:<port>
```
You can now use the package to interact with the device wirelessly.

## Example Usage

Below is an example of how to use the package to interact with connected Android devices:

```python
from adb_control import (
    DeviceManager,
    AppManager,
    MediaManager,
    ConnectManager,
    InputManager,
    SystemButton,
    AlphanumericButton,
    MediaButton,
    DeviceInfo
)
import time

device_manager = DeviceManager()
app_manager = AppManager()
media_manager = MediaManager()
connect_manager = ConnectManager()
input_manager = InputManager()
device_info = DeviceInfo()

try:
    connect_manager.connect("your_phone_ip_address", 5555)
    devices = device_manager.list_devices()
    # print("Connected Devices:", devices)

    if not devices:
        print("No devices connected. Please connect a device and try again.")
    else:
        screenshot_path = "EC.png"
        # print(f"Taking screenshot and saving as {screenshot_path}")
        # loc = media_manager.take_screenshot(screenshot_path)
        try:
            input_manager.keyevent(keyevent=SystemButton.KEYCODE_POWER.value)
            time.sleep(1.5)
            input_manager.swipe(500 ,1920 ,500 ,500)
            time.sleep(1.5)
            input_manager.text("123123")
            time.sleep(1.5)
            input_manager.keyevent(keyevent=SystemButton.KEYCODE_ENTER.value)

            print(media['message'])
        except Exception as e:
            print(f"Error during put file to device: {e}")

except Exception as e:
    print(f"Error: {e}")
```

## Example: Pull and Push Multiple Files

Below is an example of how to use the package to pull and push multiple files from and to your connected Android devices:

```python
from adb_control import DeviceManager, MediaManager

device_manager = DeviceManager()
media_manager = MediaManager()

try:
    connect_manager.connect("ip_address", 5555)
    devices = device_manager.list_devices()
    if not devices:
        print("No devices connected. Please connect a device and try again.")
    else:
        files = media_manager.list_media_files(remote_directory="/sdcard/DCIM/Screenshots")['files']
        for file in files:
            result = media_manager.transfer_file(local_file_path=f"images/{file}", direction='pull', remote_file_path="/sdcard/DCIM/Screenshots/"+file)
            print(result)

except Exception as e:
    print(f"Error: {e}")
```

# Contributing
We welcome contributions to improve this package! If you would like to contribute, please follow these steps:

Fork the repository: Click the "Fork" button on GitHub to create a copy of the repository on your own account.
We follow a simple code review process and will notify you once your changes are merged!
