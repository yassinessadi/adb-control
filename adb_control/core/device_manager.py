from adb_control.core.base import ADBBase


class DeviceManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def list_devices(self) -> dict:
        """List connected devices."""
        try:
            output = self.run_command("devices")
            if output.returncode == 0:
                stdout = output.stdout.decode("utf-8")
                lines = stdout.splitlines()
                devices = [line.split("\t")[0] for line in lines if "\tdevice" in line]
                return devices
            else:
                return {"status": "error", "message": output.stderr.decode("utf-8")}
        except Exception as e:
            return {"status": "error", "message": str(e)}
