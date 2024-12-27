from adb_control.core.base import ADBBase
import os
import time
import subprocess


class MediaManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, device=None):
        """Helper method to prepend device flag if provided."""
        if device:
            return f"-s {device} {command}"
        return command

    def take_screenshot(self, output_path, device=None):
        tmp_path = "/sdcard/screenshot.png"
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

    def record_video(self, output_path, duration=10, device=None):
        tmp_path = "/sdcard/screen_record.mp4"
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

    def get_device_storage_info(self, device=None):
        command = self._prepare_command("shell df -h", device)
        try:
            result = self.run_command(command)
            return {"status": "success", "storage_info": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def mirror_screen(self, output_folder, device=None, interval=1):
        """Simulate screen mirroring by periodically capturing screenshots."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        tmp_path = "/sdcard/screenshot.png"
        try:
            while True:
                # Capture the screenshot on the device
                command = f"shell screencap -p {tmp_path}"
                if device:
                    command = f"-s {device} {command}"
                self.run_command(command)

                # Pull the screenshot to the local machine
                local_file_path = os.path.join(output_folder, "screenshot.png")
                pull_command = f"pull {tmp_path} {local_file_path}"
                if device:
                    pull_command = f"-s {device} {pull_command}"
                self.run_command(pull_command)

                subprocess.run(["start", local_file_path], check=True, shell=True)

                self.run_command(f"shell rm {tmp_path}")

                time.sleep(interval)
        except KeyboardInterrupt:
            return {"status": "success", "message": "Screen mirroring stopped."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
