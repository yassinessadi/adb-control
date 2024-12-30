import pytest
from adb_control.core.device_manager import DeviceManager
from adb_control.core.media_manger import MediaManager


def test_list_devices():
    adb = DeviceManager()
    devices = adb.list_devices()
    assert isinstance(devices, dict)


# def test_take_screenshot():
#     adb = MediaManager()
#     adb.take_screenshot("screenshot.png")
#     # Ensure the screenshot was taken
#     assert "screenshot.png" in adb.list_files()
