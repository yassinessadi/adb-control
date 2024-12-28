from adb_control.core.base import ADBBase
import time


class InputManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def _prepare_command(self, command, device=None):
        """
        Prepare the adb command with device-specific options.
        """
        if device:
            return f"-s {device} {command}"
        return command

    def tap(self, x, y, device=None):
        """
        Tap on the screen at the given coordinates.
        """
        try:
            command = f"shell input tap {x} {y}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def swipe(self, x1, y1, x2, y2, duration=1000, device=None):
        """
        Swipe from one point to another on the screen.
        """
        try:
            command = f"shell input swipe {x1} {y1} {x2} {y2} {duration}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def text(self, text, device=None):
        """Input text on the device."""
        try:
            command = f"shell input text {text}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def keyevent(self, keyevent, device=None):
        """Send a key event to the device."""
        try:
            command = f"shell input keyevent {keyevent}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def repeat_tap(self, x, y, times=7, delay=5000, device=None):
        """
        Tap repeatedly at the given coordinates.
        """
        try:
            for _ in range(times):
                self.tap(x, y, device)
                time.sleep(delay / 1000.0)
                return {
                    "status": "success",
                    "message": f"Tapped {times} times at ({x}, {y})",
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
