# patrIoT

Daily AI generated patriotic images on the AdaFruit MagTag

![Demo Image](demo.png)

## Client Requirements

Use the included `boot.py` to remount the internal storage as read/write after boot.
Hold down the left-most face button (D15) to disable this and instead allow your PC write to the CircuitPy drive over USB.

MagTag code is written in CircuitPython. The following libraries are required:

- adafruit_bitmap_font
- adafruit_io
- adafruit_magtag
- adafruit_minimqtt
- adafruit_requests
- adafruit_ticks
- simpleio

## Server Requirements

See `server/requirements.txt`

## Usage

The server-side code runs as a `systemd` timer once every 24 hours. It generates a new patriotic image via the OpenAI image generation API.

Pressing the right-most face button (D11) on the MagTag will trigger red, white, and blue LEDs, play the star spangled banner, and display the most recent image.
