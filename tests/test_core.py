import pytest
from adb_control.core import ADBController


def test_list_devices():
    adb = ADBController()
    devices = adb.list_devices()
    assert isinstance(devices, list)  # Ensure it returns a list
