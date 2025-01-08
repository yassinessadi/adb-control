import subprocess
from typing import Literal
from adb_control.core.utils.params import ADB_PATH


class ADBBase:
    def __init__(self, adb_path=ADB_PATH):
        self.adb_path = adb_path

    def run_command(self, command) -> subprocess.CompletedProcess:
        """Run a raw ADB command."""
        try:
            process = subprocess.run(
                f"{self.adb_path} {command}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return process
        except Exception as e:
            raise Exception(f"Error: {e}")

    def open_command(self, command):
        """Run a raw ADB command."""
        try:
            process = subprocess.Popen(
                f"{self.adb_path} {command}",
                shell=True,
                stdout=subprocess.PIPE,
            )
            print(self.adb_path, command)
            return process
        except Exception as e:
            raise Exception(f"Error: {e}")

    def start_adb_server(self) -> subprocess.CompletedProcess:
        """Start the ADB server."""
        return self.run_command("start-server")

    def kill_server(self) -> subprocess.CompletedProcess:
        """Kill the ADB server."""
        print("Killing ADB server...")
        return self.run_command("kill-server")

    def shell_command(self, command: str) -> subprocess.CompletedProcess:
        """Run an ADB shell command."""
        return self.run_command(f"shell {command}")

    def transfer_file(
        self,
        local_file_path: str,
        remote_file_path: str,
        direction: Literal["push", "pull"],
        device: str = None,
    ):
        """
        Transfer a file between local and remote paths based on the specified direction.

        Args:
            local_file_path (str): The local file path.
            remote_file_path (str): The remote file path.
            direction (Literal["push", "pull"]): The direction of transfer. Must be "push" or "pull".
            device (str, optional): The device identifier. If not provided, it uses the default device.

        Returns:
            dict: A dictionary containing the status of the operation ("success" or "error") and a message.
        """
        command = f"{direction} {local_file_path if direction == 'push' else remote_file_path} {remote_file_path if direction == 'push' else local_file_path}"
        if device:
            return f"-s {device} {command}"
        try:
            self.run_command(command)
            return {"status": "success", "message": f"File {direction}ed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_file(self, file_path: str) -> subprocess.CompletedProcess:
        """Remove a file from the device."""
        return self.shell_command(f"rm {file_path}")
