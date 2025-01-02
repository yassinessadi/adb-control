from adb_control.core.base import ADBBase
from adb_control.core.utils.params import ADB_PATH


class AndroidScreenMirroring(ADBBase):
    def __init__(
        self,
        width=420,
        height=960,
        bit_rate=1000000,
        buffer_size=1024,
        screen_title="Android Screen",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.width = width
        self.adb_path = ADB_PATH
        self.height = height
        self.bit_rate = bit_rate
        self.buffer_size = buffer_size
        self.screen_title = screen_title

    def start_mirroring(self):
        try:
            # Build ADB and FFmpeg commands
            adb_command = self._build_adb_command()
            ffmpeg_command = self._build_ffmpeg_command()

            # Combine commands
            full_command = f"{adb_command} | {ffmpeg_command}"

            # Start the mirroring process
            self._execute_command(full_command)
        except KeyboardInterrupt:
            print("\nMirroring stopped by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _build_adb_command(self):
        """Constructs the ADB command for screen recording."""
        return (
            f"exec-out screenrecord --size {self.width}x{self.height} "
            f"--bit-rate={self.bit_rate} --output-format=h264 -"
        )

    def _build_ffmpeg_command(self):
        """Constructs the FFmpeg command for displaying the screen."""
        return (
            f"ffmpeg -loglevel debug -i - "
            f"-buffer_size {self.buffer_size} "
            f'-f sdl "{self.screen_title}"'
        )

    def _execute_command(self, command):
        """Executes the given shell command."""
        process = self.open_command(command)
        process.wait()

    def update_resolution(self, width, height):
        self.width = width
        self.height = height
        print(f"Resolution updated to {self.width}x{self.height}.")

    def update_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        print(f"Bit rate updated to {self.bit_rate}.")

    def update_buffer_size(self, buffer_size):
        """Updates the buffer size."""
        self.buffer_size = buffer_size
        print(f"Buffer size updated to {self.buffer_size}.")
