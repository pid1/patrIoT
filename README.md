# patrIoT

Daily AI generated patriotic images on the AdaFruit MagTag

![Demo Image](demo.png)

## How It Works

This project uses GitHub Actions to automatically generate patriotic images using OpenAI's DALL-E API once per day. The images are processed and stored in the repository, making them accessible via GitHub's raw content URLs.

Clicking the right-most face button (D11) button on the MagTag plays the star spangled banner, lights red, white, and blue LEDs, and grabs the latest image from the server.

## MagTag Requirements

Use the included `boot.py` to remount the internal storage as read/write after boot. This allows for querying, storing, and displaying the Bitmap file from GitHub.

Hold down the left-most face button (D15) to disable this and instead allow your PC write to the CircuitPy drive over USB.

MagTag code is written in CircuitPython. The following libraries are required:

- adafruit_bitmap_font
- adafruit_io
- adafruit_magtag
- adafruit_minimqtt
- adafruit_requests
- adafruit_ticks
- simpleio

## Setup

1. **Configure GitHub Secrets**: Add your OpenAI API key as a repository secret named `OPENAI_API_KEY`
2. **Enable GitHub Pages** (optional): For easier browsing of the image archive via the auto-generated `images/index.html`
3. **Deploy MagTag Code**: Copy the contents of the `magtag/` directory to your MagTag device

## Architecture

- **GitHub Action**: Runs daily at midnight UTC to generate new images
- **Image Processing**: Automatically resizes and converts images to MagTag-compatible format
- **Image Storage**: Current image saved as `images/murica.bmp`, historical images archived with timestamps
- **Web Access**: Images are accessible via GitHub raw URLs and browsable via `images/index.html`
