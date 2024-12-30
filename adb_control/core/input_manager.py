"""
A class to manage input actions on Android devices using ADB.

This class provides methods to simulate touch gestures and key events on Android devices.
It supports tapping, swiping, entering text, sending key events, and performing repeated taps.
Inherits from ADBBase to leverage common ADB command functionality.

Attributes:
    adb_path (str): Path to the ADB executable (default is "adb").
"""

import time

from adb_control.core.base import ADBBase


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

        Simulates a swipe gesture from the starting coordinates (x1, y1) to the ending coordinates (x2, y2),
        with an optional duration.

        Args:
            x1 (int): The x-coordinate of the starting point.
            y1 (int): The y-coordinate of the starting point.
            x2 (int): The x-coordinate of the ending point.
            y2 (int): The y-coordinate of the ending point.
            duration (int, optional): The duration of the swipe in milliseconds. Default is 1000 ms.
            device (str, optional): The device identifier. If not provided, the command will run on the default device.

        Returns:
            dict: A dictionary containing the status of the operation ("success" or "error") and a message.
        """
        try:
            command = f"shell input swipe {x1} {y1} {x2} {y2} {duration}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def text(self, text, device=None):
        """
        Input text on the device.

        Simulates typing the specified text on the device.

        Args:
            text (str): The text to input.
            device (str, optional): The device identifier. If not provided, the command will run on the default device.

        Returns:
            dict: A dictionary containing the status of the operation ("success" or "error") and a message.
        """
        try:
            command = f"shell input text {text}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def keyevent(self, keyevent, device=None):
        """
        Send a key event to the device.

        Simulates pressing a key on the device using a key event.

        Args:
            keyevent (int): The key event code to simulate.
            device (str, optional): The device identifier. If not provided, the command will run on the default device.

        Returns:
            dict: A dictionary containing the status of the operation ("success" or "error") and a message.
        """
        try:
            command = f"shell input keyevent {keyevent}"
            command = self._prepare_command(command, device)
            return self.run_command(command)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def repeat_tap(self, x, y, times=7, delay=5000, device=None):
        """
        Tap repeatedly at the given coordinates.

        Simulates multiple tap gestures at the same coordinates with a delay between each tap.

        Args:
            x (int): The x-coordinate of the screen where the tap should occur.
            y (int): The y-coordinate of the screen where the tap should occur.
            times (int, optional): The number of times to repeat the tap. Default is 7.
            delay (int, optional): The delay between taps in milliseconds. Default is 5000 ms (5 seconds).
            device (str, optional): The device identifier. If not provided, the command will run on the default device.

        Returns:
            dict: A dictionary containing the status of the operation ("success" or "error") and a message.
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
