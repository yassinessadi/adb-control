"""
A class to manage connections to Android devices over the network using ADB.

This class provides methods to connect and disconnect from devices using their IP address and port.
It builds and executes the necessary ADB commands to establish and close connections.
Inherits from ADBBase to leverage existing ADB command functionality.

Attributes:
    adb_path (str): Path to the ADB executable (default is "adb").
"""

from adb_control.core.base import ADBBase
from adb_control.core.utils.params import DEFAULT_PORT


class ConnectManager(ADBBase):
    def _prepare_command(self, command, device_ip, port):
        """Helper method to build the connection command."""
        if device_ip:
            device_target = f"{device_ip}:{port}"
            return f"{command} {device_target}"
        return command

    def connect(self, device_ip: str = "", port: int = DEFAULT_PORT):
        """
        Connect to a specific device by its IP address and port.
        """
        command = self._prepare_command("connect", device_ip, port)
        try:
            result = self.run_command(command)

            # Check the stdout or stderr for success or failure
            if "connected" in result.stdout.decode().lower():
                return {
                    "status": "success",
                    "message": f"Connected to {device_ip}:{port}",
                }
            else:
                return {
                    "status": "error",
                    "message": result.stdout.decode() or result.stderr.decode(),
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def disconnect(self, device_ip: str = "", port: int = DEFAULT_PORT):
        """
        Disconnect from a specific device or all devices.
        If `device_ip` is not provided, it disconnects from all devices.
        """
        # Prepare the command based on whether a device IP is provided
        command = (
            self._prepare_command("disconnect")
            if not device_ip
            else self._prepare_command("disconnect", device_ip, port)
        )

        try:
            result = self.run_command(command)

            # Check stdout for success or failure messages
            if "disconnected" in result.stdout.decode().lower():
                return {
                    "status": "success",
                    "message": (
                        "Disconnected from all devices"
                        if not device_ip
                        else f"Disconnected from {device_ip}:{port}"
                    ),
                }
            else:
                # Return the output as an error message if disconnection failed
                return {
                    "status": "error",
                    "message": result.stdout.decode() or result.stderr.decode(),
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
