from __future__ import annotations

import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from gpiozero import Button

SHUTTER_BUTTON_PIN = 17  # BCM pin 17, physical pin 11
SAVE_DIRECTORY = Path.home() / "Pictures" / "PI-Pixel"
CAMERA_COMMANDS = ("rpicam-still", "libcamera-still")
CAPTURE_FLAGS = ("--immediate", "--nopreview")

is_capturing = False


def ensure_save_directory() -> None:
    SAVE_DIRECTORY.mkdir(parents=True, exist_ok=True)


def get_camera_command() -> str:
    for command in CAMERA_COMMANDS:
        if shutil.which(command):
            return command
    raise RuntimeError("No camera command found. Install rpicam-apps or libcamera-apps.")


def show_splash_screen() -> None:
    print("Camera ready. Press the shutter button to take a shot.")


def show_capture_feedback() -> None:
    print("Capturing photo...")


def capture_image() -> None:
    global is_capturing

    if is_capturing:
        return

    is_capturing = True
    try:
        show_capture_feedback()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = SAVE_DIRECTORY / f"IMG_{timestamp}.jpg"
        command = [get_camera_command(), "-o", str(filename), *CAPTURE_FLAGS]

        subprocess.run(command, check=True)
        print(f"Image saved to {filename}")
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Camera capture failed: {error}")
    finally:
        is_capturing = False
        show_splash_screen()


def main() -> None:
    ensure_save_directory()
    show_splash_screen()

    shutter_button = Button(SHUTTER_BUTTON_PIN, pull_up=True, bounce_time=0.1)
    shutter_button.when_pressed = capture_image

    print("Waiting for shutter press... Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down cleanly.")


if __name__ == "__main__":
    main()