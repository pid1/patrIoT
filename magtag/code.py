import displayio
import wifi
import os
from adafruit_magtag.magtag import MagTag
import adafruit_requests
import socketpool
import ssl
import storage
import board
import random
import alarm
import time

magtag = MagTag()

magtag.peripherals.buttons[3].deinit()
pin_alarm = alarm.pin.PinAlarm(pin=board.D11, value=False, pull=True)

note_1 = 233
note_2 = 294
note_3 = 330
note_4 = 349
note_5 = 392
note_6 = 440
note_7 = 466
note_8 = 523
note_9 = 587
note_10 = 622
note_11 = 698

try:
    # Set NeoPixel colors using MagTag's built-in NeoPixel management
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels[2] = (0, 0, 255)      # Bright blue
    magtag.peripherals.neopixels[3] = (0, 0, 255)      # Bright blue
    magtag.peripherals.neopixels[1] = (255, 0, 0)      # Bright red
    magtag.peripherals.neopixels[0] = (255, 255, 255)  # Bright white
    magtag.peripherals.neopixels.show()
except:
    pass

try:
    mult = 0.5 # Allow for easily speeding up or slowing down the tones
    magtag.peripherals.play_tone(note_4, mult*0.75)
    magtag.peripherals.play_tone(note_2, mult*0.25)
    magtag.peripherals.play_tone(note_1, mult)
    magtag.peripherals.play_tone(note_2, mult)
    magtag.peripherals.play_tone(note_4, mult)
    magtag.peripherals.play_tone(note_7, mult*2)
    magtag.peripherals.play_tone(note_9, mult*0.75)
    magtag.peripherals.play_tone(note_8, mult*0.25)
    magtag.peripherals.play_tone(note_7, mult)
    magtag.peripherals.play_tone(note_2, mult)
    magtag.peripherals.play_tone(note_3, mult)
    magtag.peripherals.play_tone(note_4, mult*2)

except:
    pass

if storage.getmount('/').readonly:
    magtag.add_text(
        text_position=(
        (magtag.graphics.display.width // 2) - 1,
        random.uniform(0,magtag.graphics.display.height)
        ),
        text_scale=random.randint(1,5),
        text_anchor_point=(0.5, 0.5),
        )
    magtag.set_text("> USB mode")
    magtag.exit_and_deep_sleep(120)

try:
    # Connect to WiFi
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

    # URL of the bitmap image
    url = "http://137.184.19.28:80/murica.bmp"

    # Download the image
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    response = requests.get(url)
    if response.status_code == 200:
        with open("/murica.bmp", "wb") as file:
            file.write(response.content)
        time.sleep(5)
    else:
        print("Failed to download the image")
except:
    pass

try:
    bitmap = displayio.OnDiskBitmap("murica.bmp")

    # Create a TileGrid to hold the image
    x = bitmap.pixel_shader

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=x)
    tile_flipped = displayio.TileGrid(bitmap, pixel_shader=x)

    # Calculate the position to center the image
    # MagTag display is 296x128 pixels
    image_width = bitmap.width
    image_height = bitmap.height
    display_width = magtag.display.width
    display_height = magtag.display.height

    x = (display_width - image_width) // 2
    y = (display_height - image_height) // 2

    x = (display_width - image_width * 2 ) // 2

    # Set the position of the TileGrid
    tile_grid.x = x
    tile_grid.y = y

    tile_flipped.x = x + image_width
    tile_flipped.y = y
    tile_flipped.flip_x = True

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)
    group.append(tile_flipped)

    # Show the Group on the display
    magtag.splash.append(group)

    # Refresh the display to show the image
    magtag.display.refresh()

    # Wait for the display to finish updating
    while board.DISPLAY.busy:
        pass
except:
    pass

time.sleep(10)

try:
    magtag.peripherals.neopixels.fill((0, 0, 0))  # Turn off all NeoPixels
    magtag.peripherals.neopixels.show()
    magtag.peripherals.neopixel_disable = True
except:
    pass

# go into sleep mode until we press D11 again
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
