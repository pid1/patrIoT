# patrIoT

Daily AI generated patriotic images on the Adafruit MagTag

## Requirements

- Adafruit MagTag
- Adafruit MagTag Libraries
  - adafruit_magtag
  - adafruit_bitmap_font
  - adafruit_io
  - adafruit_minimqtt
  - adafruit_ticks
  - simpleio

## Usage

The server-side code runs as a cron job once every 24 hours. It generates a new patriotic image via the OpenAI DALL-E-3 API.

The MagTag reaches out to the server every 24 hours to get the latest image and display it.
