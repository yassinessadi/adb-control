import subprocess

from adb_control.core.utils.params import ADB_PATH


class ADBBase:
    def __init__(self, adb_path=ADB_PATH):
        self.adb_path = adb_path

    def run_command(self, command):
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
            )
            print(self.adb_path, command)
            return process
        except Exception as e:
            raise Exception(f"Error: {e}")

    def start_adb_server(self):
        """Start the ADB server."""
        return self.run_command("start-server")

    def kill_server(self):
        """Kill the ADB server."""
        print("Killing ADB server...")
        return self.run_command("kill-server")
