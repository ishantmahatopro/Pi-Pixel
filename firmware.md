# Firmware

This is the firmware guide for PI-Pixel. The goal is simple: boot the Pi, wait for the shutter button, capture a frame, and save it with a clean timestamped filename.

## Current firmware

The active script lives in [firmware/pipixel.py](firmware/pipixel.py).

What it does:

- Creates the save folder under `~/Pictures/PI-Pixel/`
- Waits for the shutter button on BCM 17
- Captures a still image with `rpicam-still` or `libcamera-still`
- Saves files as `IMG_YYYYMMDD_HHMMSS.jpg`

## Dependencies

Install the Python and camera packages on Raspberry Pi OS:

```bash
sudo apt update
sudo apt install -y python3-gpiozero rpicam-apps
```

If your image does not have `rpicam-apps`, use `libcamera-apps` instead.

## Wiring used by the firmware

- Shutter button: BCM 17 to GND
- Button mode: pull-up input

The wider hardware notes in [JOURNAL.md](JOURNAL.md) include the display, LED, power, and camera wiring used for the full build.

## Run manually

From the repository root on the Pi:

```bash
python3 firmware/pipixel.py
```

If the camera command is missing, install the camera app package first and try again.

## Run on boot with systemd

Create the service file:

```bash
sudo nano /etc/systemd/system/pi-pixel.service
```

Paste this:

```ini
[Unit]
Description=PI-Pixel Camera Firmware
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/pi/PI-Pixel
ExecStart=/usr/bin/python3 /home/pi/PI-Pixel/firmware/pipixel.py
Restart=on-failure
RestartSec=3
User=pi

[Install]
WantedBy=multi-user.target
```

Then enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pi-pixel.service
sudo systemctl start pi-pixel.service
```

To check logs:

```bash
sudo journalctl -u pi-pixel.service -f -n 50
```

## Troubleshooting

- No photos saved: check the save folder exists and the Pi user can write to `~/Pictures/PI-Pixel/`.
- Camera command not found: install `rpicam-apps` or `libcamera-apps`.
- Button does nothing: confirm BCM 17 is wired to the switch and the other side goes to GND.

## Notes

The firmware is intentionally lean. The display and extra peripherals are documented in the journal, but the capture loop stays focused on the shutter path so it boots clean and is easy to debug.