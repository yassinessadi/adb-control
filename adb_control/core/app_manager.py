from adb_control.core.base import ADBBase


class AppManager(ADBBase):
    def install_package(self, package_name, device=None):
        """Uninstall a package from the device."""
        command = f"install {package_name}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)

    def uninstall_package(self, package_name, device=None):
        """Uninstall a package from the device."""
        command = f"uninstall {package_name}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)
