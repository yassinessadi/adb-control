from enum import Enum


class SystemButton(Enum):
    KEYCODE_HOME = 3  # Home button
    KEYCODE_BACK = 4  # Back button
    KEYCODE_MENU = 82  # Menu button
    KEYCODE_SEARCH = 84  # Search button
    KEYCODE_POWER = 26  # Power button
    KEYCODE_ENTER = 66  # Enter button


class MediaButton(Enum):
    KEYCODE_VOLUME_UP = 24  # Volume up button
    KEYCODE_VOLUME_DOWN = 25  # Volume down button
    KEYCODE_MUTE = 91  # Mute button
    KEYCODE_NOTIFICATION = 83  # Notification button
    KEYCODE_PAGE_UP = 92  # Page up button
    KEYCODE_PAGE_DOWN = 93  # Page down button


class AlphanumericButton(Enum):
    KEYCODE_A = 29  # 'A' key
    KEYCODE_B = 30  # 'B' key
    KEYCODE_C = 31  # 'C' key
    KEYCODE_1 = 8  # '1' key
    KEYCODE_2 = 9  # '2' key
    KEYCODE_3 = 10  # '3' key
    KEYCODE_4 = 11  # '4' key
    KEYCODE_5 = 12  # '5' key
    KEYCODE_6 = 13  # '6' key
    KEYCODE_7 = 14  # '7' key
    KEYCODE_8 = 15  # '8' key
    KEYCODE_9 = 16  # '9' key
