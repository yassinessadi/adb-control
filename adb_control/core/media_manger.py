from adb_control.core.base import ADBBase
import subprocess
import time
import cv2


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

                command = f"{self.adb_path} exec-out screencap -p > {screenshot_path}"
                if device:
                    command = f"{self.adb_path} -s {device} exec-out screencap -p > {screenshot_path}"

                result = subprocess.run(
                    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
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

    def transfer_file_to_device(self, local_file_path, remote_file_path, device=None):
        command = self._prepare_command(
            f"push {local_file_path} {remote_file_path}", device
        )
        try:
            self.run_command(command)
            return {
                "status": "success",
                "message": f"File {local_file_path} pushed to {remote_file_path}",
            }
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

    def list_media_files(self, remote_directory="/sdcard/", device=None):
        command = self._prepare_command(f"shell ls {remote_directory}", device)
        try:
            result = self.run_command(command)
            return {"status": "success", "files": result}
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
