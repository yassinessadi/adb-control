import subprocess


class ADBBase:
    def __init__(self, adb_path="adb"):
        self.adb_path = adb_path

    def run_command(self, command):
        """Run a raw ADB command."""
        result = subprocess.run(
            f"{self.adb_path} {command}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr.decode('utf-8')}")
        return result.stdout.decode("utf-8")

    def start_adb_server(self):
        """Start the ADB server."""
        return self.run_command("start-server")

    def kill_server(self):
        """Kill the ADB server."""
        print("Killing ADB server...")
        return self.run_command("kill-server")
