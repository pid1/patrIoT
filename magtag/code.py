import time
import displayio
import wifi
import os
from adafruit_magtag.magtag import MagTag
import adafruit_requests
import socketpool
import ssl
from adafruit_imageload import load
from io import BytesIO

magtag = MagTag()

# Connect to WiFi
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

# URL of the bitmap image
url = "http://137.184.19.28:80/murica.bmp"

# Download the image
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
response = requests.get(url)
if response.status_code == 200:
    image_data = response.content
else:
    print("Failed to download the image")
    image_data = None

if image_data:
    # Save the image to a file
    with open("/murica.bmp", "wb") as file:
        file.write(image_data)

    # Load the image
    bitmap = displayio.OnDiskBitmap("murica.bmp")

    # Create a TileGrid to hold the image
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    # Calculate the position to center the image
    # MagTag display is 296x128 pixels
    image_width = bitmap.width
    image_height = bitmap.height
    display_width = magtag.display.width
    display_height = magtag.display.height

    x = (display_width - image_width) // 2
    y = (display_height - image_height) // 2

    # Set the position of the TileGrid
    tile_grid.x = x
    tile_grid.y = y

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Show the Group on the display
    magtag.splash.append(group)

    # Refresh the display to show the image
    magtag.display.refresh()

    # Wait for the display to finish updating
    time.sleep(10)

    # go into sleep mode until we rotate
    # the photo 24 hours later
    magtag.exit_and_deep_sleep(86400)
