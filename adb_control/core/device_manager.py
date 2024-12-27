from adb_control.core.base import ADBBase


class DeviceManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def list_devices(self):
        """List connected devices."""
        try:
            output = self.run_command("devices")
            # Skip the first line and filter devices from the rest of the output
            devices = [
                line.split("\t")[0]
                for line in output.splitlines()[1:]
                if "\tdevice" in line
            ]
            return {"status": "success", "devices": devices}
        except Exception as e:
            return {"status": "error", "message": str(e)}
