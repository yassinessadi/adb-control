from adb_control.core.base import ADBBase


class ConnectManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def Connect(self, device_ip: str, port: int = 5555):
        device_target = f"{device_ip}:{port}"
        command = f"connect {device_target}"
        return self.run_command(command)
