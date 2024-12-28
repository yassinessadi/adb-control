from adb_control.core.base import ADBBase


class DeviceInfo(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, device=None):
        """
        Prepare the adb command with device-specific options.
        """
        if device:
            return f"-s {device} {command}"
        return command

    def device_info(self, device=None):
        """
        Retrieve system properties from the device and filter key information.
        """
        command = self._prepare_command("shell getprop", device)
        try:
            result = self.run_command(command)
            properties = {}
            for line in result.splitlines():
                parts = line.split(": ", maxsplit=1)
                if len(parts) == 2:
                    key = parts[0].strip("[]")
                    value = parts[1].strip("[]")
                    properties[key] = value

            fingerprint = properties.get("ro.build.fingerprint", "Unknown")
            model = properties.get("ro.product.model", "Unknown")
            manufacturer = properties.get("ro.product.manufacturer", "Unknown")
            android_version = properties.get("ro.build.version.release", "Unknown")
            sdk_version = properties.get("ro.build.version.sdk", "Unknown")

            return {
                "status": "success",
                "device_info": {
                    "fingerprint": fingerprint,
                    "model": model,
                    "manufacturer": manufacturer,
                    "android_version": android_version,
                    "sdk_version": sdk_version,
                },
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
