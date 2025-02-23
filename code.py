import time
import board
from adafruit_magtag.magtag import MagTag
import displayio

display = board.DISPLAY

magtag = MagTag()

# Load the image
bitmap = displayio.OnDiskBitmap("usa.bmp")

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
