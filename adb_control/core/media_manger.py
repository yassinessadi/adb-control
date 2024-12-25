from adb_control.core.base import ADBBase


class MediaManager(ADBBase):
    def take_screenshot(self, output_path, device=None):
        """Take a screenshot and save it to the computer."""
        tmp_path = "/sdcard/screenshot.png"
        command = f"shell screencap -p {tmp_path}"
        if device:
            command = f"-s {device} {command}"
        self.run_command(command)
        pull_command = f"pull {tmp_path} {output_path}"
        if device:
            pull_command = f"-s {device} {pull_command}"
        self.run_command(pull_command)
        self.run_command(f"shell rm {tmp_path}")
        return f"Screenshot saved to {output_path}"
