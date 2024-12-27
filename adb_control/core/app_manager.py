from adb_control.core.base import ADBBase


class AppManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, package_name, device=None):
        """Helper method to prepare the command with optional device argument."""
        if device:
            return f"-s {device} {command} {package_name}"
        return f"{command} {package_name}"

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
        command = "shell pm list packages"
        if device:
            command = f"-s {device} {command}"
        try:
            output = self.run_command(command)
            return {"status": "success", "packages": output.splitlines()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
