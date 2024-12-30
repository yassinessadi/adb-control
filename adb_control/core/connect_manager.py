"""
A class to manage connections to Android devices over the network using ADB.

This class provides methods to connect and disconnect from devices using their IP address and port.
It builds and executes the necessary ADB commands to establish and close connections.
Inherits from ADBBase to leverage existing ADB command functionality.

Attributes:
    adb_path (str): Path to the ADB executable (default is "adb").
"""

from adb_control.core.base import ADBBase


class ConnectManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, device_ip=None, port=5555):
        """Helper method to build the connection command."""
        if device_ip:
            device_target = f"{device_ip}:{port}"
            return f"{command} {device_target}"
        return command

    def connect(self, device_ip: str, port: int = 5555):
        """
        Connect to a specific device by its IP address and port.
        """
        command = self._prepare_command("connect", device_ip, port)
        try:
            result = self.run_command(command)
            return {"status": "success", "message": f"Connected to {device_ip}:{port}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def disconnect(self, device_ip: str = None, port: int = 5555):
        """
        Disconnect from a specific device or all devices.
        """
        command = self._prepare_command("disconnect", device_ip, port)
        try:
            result = self.run_command(command)
            return {
                "status": "success",
                "message": "Disconnected"
                if not device_ip
                else f"Disconnected from {device_ip}:{port}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
