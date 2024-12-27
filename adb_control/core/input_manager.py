from adb_control.core.base import ADBBase
import time


class InputManager(ADBBase):
    def __init__(self, adb_path="adb"):
        super().__init__(adb_path)

    def tap(self, x, y, device=None):
        """
        Tap on the screen at the given coordinates.
        """
        command = f"shell input tap {x} {y}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)

    def swipe(self, x1, y1, x2, y2, duration=1000, device=None):
        """
        Swipe from one point to another on the screen.
        """
        command = f"shell input swipe {x1} {y1} {x2} {y2} {duration}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)

    def text(self, text, device=None):
        """Input text on the device."""
        command = f"shell input text {text}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)

    def keyevent(self, keyevent, device=None):
        """Send a key event to the device."""
        command = f"shell input keyevent {keyevent}"
        if device:
            command = f"-s {device} {command}"
        return self.run_command(command)

    def repeat_tap(self, x, y, times=7, delay=500, device=None):
        for _ in range(times):
            self.tap(x, y, device)
            time.sleep(delay / 1000.0)
        return True
