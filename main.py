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

        try:
            apk_path = "facebook_lite_v438.0.0.13.102.apk"
            remote_apk_path = "/sdcard/facebook_lite.apk"
            print(f"Transferring APK: {apk_path} to the device...")
            result = media_manager.transfer_file_to_device(
                local_file_path=apk_path, remote_file_path=remote_apk_path
            )
            print(result)
        except Exception as e:
            print(f"Error during put file to device: {e}")

except Exception as e:
    print(f"Error: {e}")
