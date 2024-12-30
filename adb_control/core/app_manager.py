"""
This module provides the AppManager class, which offers utilities for managing
applications on Android devices using ADB (Android Debug Bridge). It allows for
installing, uninstalling, listing installed packages, and launching apps on a
connected Android device.

Functions:
    - install_package: Installs an app package on the device.
    - uninstall_package: Uninstalls an app package from the device.
    - list_installed_packages: Lists all installed packages on the device.
    - installed_package: Checks if a specific package is installed.
    - launch_app: Launches an app using its package name.
"""

from adb_control.core.base import ADBBase


class AppManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, package_name=None, device=None):
        """
        Helper method to prepare the command with optional device and package_name arguments.
        """
        if device:
            command = f"-s {device} {command}"
        if package_name:
            command = f"{command} {package_name}"
        return command

    def install_package(self, package_name, device=None):
        """Install a package on the device."""
        command = self._prepare_command("install", package_name, device)
        try:
            result = self.run_command(command)
            return {
                "status": "success",
                "message": f"Package {package_name} installed.",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def uninstall_package(self, package_name, device=None):
        """Uninstall a package from the device."""
        command = self._prepare_command("uninstall", package_name, device)
        try:
            result = self.run_command(command)
            return {
                "status": "success",
                "message": f"Package {package_name} uninstalled.",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_installed_packages(self, device=None):
        """List all installed packages on the device."""
        command = self._prepare_command("shell pm list packages", device=device)
        try:
            output = self.run_command(command)
            if output.returncode == 0:
                stdout = output.stdout.decode("utf-8")
                lines = stdout.splitlines()
                packages = [line for line in lines]
            return {"status": "success", "packages": packages}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def installed_package(self, device=None, package_name=None) -> dict:
        """List all installed packages on the device.
        package_name: str
        function will return only the package_name
        :return: dict
        """
        try:
            output = self.list_installed_packages(device)
            if output["status"] == "success":
                return {
                    "status": "success",
                    "message": "Installed packages listed.",
                    "packages": [
                        package
                        for package in output["packages"]
                        if package == package_name
                    ],
                }
            else:
                return {"status": "error", "message": output["message"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def launch_app(self, package_name, device=None):
        """
        Open an app using its package name.
        """
        command = self._prepare_command(
            f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1",
            device=device,
        )
        try:
            result = self.run_command(command)
            return {
                "status": "success",
                "message": f"App {package_name} opened.",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
