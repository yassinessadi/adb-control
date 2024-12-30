"""
    A class to manage media operations on Android devices using ADB.

    This class provides methods for taking screenshots, recording videos, transferring files,
    listing media files, and removing files or folders on Android devices. It uses ADB commands
    to interact with the device and perform these operations.

    Attributes:
        adb_path (str): The path to the ADB executable (default is "adb").
"""

import time
from typing import Literal

from adb_control.core.base import ADBBase


class MediaManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, device=None):
        """Helper method to prepend device flag if provided."""
        if device:
            return f"-s {device} {command}"
        return command

    def take_screenshot(
        self, output_path, device=None, tmp_path="/sdcard/screenshot.png"
    ):
        command = self._prepare_command(f"shell screencap -p {tmp_path}", device)

        try:
            self.run_command(command)
            pull_command = self._prepare_command(
                f"pull {tmp_path} {output_path}", device
            )
            self.run_command(pull_command)
            self.run_command(self._prepare_command(f"shell rm {tmp_path}", device))
            return {
                "status": "success",
                "message": f"Screenshot saved to {output_path}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def take_screenshots(
        self, output_path, device=None, num_screenshots=7, interval=0.05
    ):
        """Capture multiple screenshots and store them locally using exec-out."""
        try:
            for i in range(num_screenshots):
                screenshot_path = f"{output_path}/screenshot_{i + 1}.png"

                command = self._prepare_command(
                    f"exec-out screencap -p > {screenshot_path}", device
                )

                result = self.run_command(command)
                if result.returncode != 0:
                    raise RuntimeError(
                        f"ADB command failed: {result.stderr.decode('utf-8')}"
                    )

                print(f"Screenshot saved to {screenshot_path}")
                time.sleep(interval)
            return {
                "status": "success",
                "message": f"{num_screenshots} screenshots saved to {output_path}",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

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
        command = self._prepare_command(command, device)
        try:
            self.run_command(command)
            return {"status": "success", "message": f"File {direction}ed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def record_video(
        self,
        output_path,
        duration=10,
        device=None,
        tmp_path="/sdcard/screen_record.mp4",
    ):
        command = self._prepare_command(
            f"shell screenrecord --time-limit {duration} {tmp_path}", device
        )
        try:
            self.run_command(command)
            pull_command = self._prepare_command(
                f"pull {tmp_path} {output_path}", device
            )
            self.run_command(pull_command)
            self.run_command(self._prepare_command(f"shell rm {tmp_path}", device))
            return {"status": "success", "message": f"Video saved to {output_path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_media_files(self, remote_directory="/", device=None):
        command = self._prepare_command(f"shell ls {remote_directory}", device)
        try:
            result = self.run_command(command)
            if result.returncode == 0:
                stdout = result.stdout.decode("utf-8")
                lines = stdout.splitlines()
            return {"status": "success", "files": lines}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def remove_file(self, remote_file_path, folder=False, device=None):
        """
        Remove a specific file or folder on the Android device.

        :param remote_file_path: The full path to the file or folder to remove (e.g., /sdcard/essadi.png)
        :param folder: Whether the path is a folder (True) or a file (False)
        :param device: The specific device ID to use for the adb command.
        :return: A dictionary with status and message.
        """
        try:
            if folder:
                remove_command = self._prepare_command(
                    f"shell rm -rf {remote_file_path}", device
                )
            else:
                remove_command = self._prepare_command(
                    f"shell rm {remote_file_path}", device
                )
            self.run_command(remove_command)
            return {
                "status": "success",
                "message": f"File or folder {remote_file_path} removed.",
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
