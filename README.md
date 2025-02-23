# patrIoT

Daily AI generated patriotic images on the Adafruit MagTag

## Client Requirements

This assumes that the MagTag storage is remounted read/write after boot using boot.py.

```python
import storage

storage.remount("/", readonly=False)
```

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

## Server Requirements

See `server/requirements.txt`

## Usage

The server-side code runs as a systemd timer once every 24 hours. It generates a new patriotic image via the OpenAI DALL-E-3 API.

The MagTag reaches out to the server every 24 hours to get the latest image and display it.
