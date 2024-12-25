from adb_control.core.base import ADBBase


class DeviceManager(ADBBase):
    def list_devices(self):
        """List connected devices."""
        output = self.run_command("devices")
        devices = [
            line.split("\t")[0] for line in output.splitlines() if "\tdevice" in line
        ]
        return devices
