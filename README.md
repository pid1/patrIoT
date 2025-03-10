# patrIoT

Daily AI generated patriotic images on the Adafruit MagTag

![Demo Image](demo.png)

## Client Requirements

Use the included boot.py to remount the internal storage as read/write after boot.
Hold down the A / left-most face button (D15) to disable this and instead allow your PC write to the circuitpy drive over USB.

MagTag code is written in CircuitPython. The following libraries are required:

- Adafruit MagTag
- Adafruit MagTag Libraries
  - adafruit_bitmap_font
  - adafruit_imageload
  - adafruit_io
  - adafruit_magtag
  - adafruit_minimqtt
  - adafruit_requests
  - adafruit_ticks
  - simpleio
  - socketpool
  - ssl
  - wifi

## Server Requirements

See `server/requirements.txt`

## Usage

The server-side code runs as a systemd timer once every 24 hours. It generates a new patriotic image via the OpenAI DALL-E-3 API.

The MagTag reaches out to the server every 24 hours to get the latest image and display it.
