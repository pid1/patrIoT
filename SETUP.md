# PatrIoT Setup Guide

## Prerequisites

1. **OpenAI API Key**: You'll need an OpenAI API key with access to DALL-E image generation
2. **GitHub Repository**: This code should be in a GitHub repository with Actions enabled
3. **AdaFruit MagTag**: For displaying the generated images

## GitHub Repository Setup

### 1. Configure GitHub Secrets

Add the following secret to your repository:

1. Go to your repository on GitHub
2. Click `Settings` → `Secrets and variables` → `Actions`
3. Click `New repository secret`
4. Add:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key

### 2. Enable GitHub Pages (Optional but Recommended)

For easy browsing of generated images:

1. Go to `Settings` → `Pages`
2. Under "Source", select "GitHub Actions"
3. The pages will be automatically deployed when images are generated

### 3. Test the Workflow

You can manually trigger the image generation workflow:

1. Go to `Actions` tab in your repository
2. Select "Generate Daily Patriotic Image"
3. Click "Run workflow" → "Run workflow"

## MagTag Setup

### 1. Install Required Libraries

Install these CircuitPython libraries on your MagTag:

- adafruit_bitmap_font
- adafruit_io
- adafruit_magtag
- adafruit_minimqtt
- adafruit_requests
- adafruit_ticks
- simpleio

### 2. Configure WiFi

Create a `settings.toml` file on your MagTag with your WiFi credentials:

```toml
CIRCUITPY_WIFI_SSID = "YourWiFiName"
CIRCUITPY_WIFI_PASSWORD = "YourWiFiPassword"
```

### 3. Deploy Code

Copy the contents of the `magtag/` directory to your MagTag device.

## File Structure

```
patrIoT/
├── .github/workflows/
│   ├── generate-patriotic-image.yml  # Daily image generation
│   └── deploy-pages.yml              # GitHub Pages deployment
├── images/                           # Generated images
│   ├── murica.bmp                   # Current image (for MagTag)
│   ├── index.html                   # Web browsing interface
│   ├── YYYYMMDD-original.png        # Archived original images
│   └── YYYYMMDD-bitmap.bmp          # Archived bitmap images
├── magtag/                          # MagTag CircuitPython code
│   ├── boot.py
│   └── code.py
├── scripts/
│   └── generate_image.py            # Image generation script
└── README.md
```

## How It Works

1. **Daily Generation**: GitHub Action runs at midnight UTC every day
2. **Image Creation**: Calls OpenAI DALL-E API with patriotic prompt
3. **Processing**: Resizes to 128x128px and converts to indexed bitmap
4. **Storage**: Saves current image as `murica.bmp` and archives with timestamp
5. **Web Access**: Images are accessible via GitHub raw URLs and GitHub Pages
6. **MagTag Display**: Device downloads and displays the current image when button is pressed

## Troubleshooting

### Workflow Fails
- Check that `OPENAI_API_KEY` is correctly set in repository secrets
- Verify the API key has sufficient credits and DALL-E access
- Check the Actions tab for detailed error logs

### MagTag Connection Issues
- Verify WiFi credentials in `settings.toml`
- Check that the GitHub raw URL is accessible
- Ensure all required CircuitPython libraries are installed

### Image Not Updating
- The workflow runs once per day at midnight UTC
- You can manually trigger it from the Actions tab
- Check if there were any recent commits to the `images/` directory