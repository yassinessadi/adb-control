from adb_control import DeviceManager, AppManager, MediaManager

device_manager = DeviceManager()
app_manager = AppManager()
media_manager = MediaManager()

try:
    devices = device_manager.list_devices()
    print("Connected Devices:", devices)

    if not devices:
        print("No devices connected. Please connect a device and try again.")
    else:
        screenshot_path = "jane.png"
        print(f"Taking screenshot and saving as {screenshot_path}")
        media_manager.take_screenshot(screenshot_path)

except Exception as e:
    print(f"Error: {e}")
