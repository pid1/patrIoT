import board
import digitalio
import storage

# MagTag A button / D15
switch = digitalio.DigitalInOut(board.D15)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the A button is held down during boot, filesystem is read-only to MagTag
storage.remount("/", readonly=not switch.value)
