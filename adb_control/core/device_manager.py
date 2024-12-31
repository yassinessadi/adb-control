"""
A class to manage Android devices connected via ADB.

This class provides functionality to list all connected devices.
It interacts with ADB to retrieve the list of devices and their statuses.
Inherits from ADBBase to leverage the common ADB command execution functionality.

Attributes:
    adb_path (str): Path to the ADB executable (default is "adb").
"""

from adb_control.core.base import ADBBase
from adb_control.core.utils.params import ADB_PATH, ENCODING


class DeviceManager(ADBBase):
    def list_devices(self) -> dict:
        """List connected devices."""
        try:
            output = self.run_command("devices")
            if output.returncode == 0:
                stdout = output.stdout.decode(ENCODING)
                lines = stdout.splitlines()
                devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]
                return devices
            else:
                return {"status": "error", "message": output.stderr.decode(ENCODING)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
