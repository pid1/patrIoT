#!/usr/bin/env python3

import base64
import datetime
import os
import random
import sys
from pathlib import Path
from openai import OpenAI
from PIL import Image

def main():
    # Check for required API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Create images directory if it doesn't exist
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)

    print("Generating patriotic image using OpenAI...")

    subjects = [
        "the Statue of Liberty",
        "a bald eagle in profile",
        "Abraham Lincoln's portrait",
        "George Washington's portrait", 
        "an American flag waving",
        "the Liberty Bell",
        "Mount Rushmore",
        "The Capitol Building dome",
        "Uncle Sam pointing",
        "An American bison",
        "An Apollo astronaut with helmet",
        "Benjamin Franklin's portrait",
        "Theodore Roosevelt's portrait",
        "A Revolutionary War minuteman with musket",
        "The Space Shuttle",
        "NASA astronauts",
        "saturn V rocket",
    ]
    
    subject = random.choice(subjects)
    
    try:
        # Generate image using the same prompt as the original server
        response = client.images.generate(
            model="gpt-image-1.5",
            prompt = (
                f"Children's book illustration of {subject}, close-up filling most of the frame. "
                "Hand-drawn style with bold outlines, high contrast suitable for greyscale dithering. "
                "Simple, minimal background. No text or watermarks. 128x128 pixel e-ink display target."
            )
            size="1024x1024",
            quality="high",
            n=1,
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        with open("temp_generated.png", "wb") as f:
            f.write(image_bytes)
        
        # Generate timestamp for archival
        timestamp = int(datetime.datetime.now().timestamp())
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        print(f"Processing image for {date_str}...")

        # Save the original high-resolution image for archival
        original_path = images_dir / f"{timestamp}-original.png"
        image = Image.open("temp_generated.png")
        image.save(original_path)
        print(f"Saved original image: {original_path}")

        # Resize the image to 128x128 for the MagTag display
        resized_image = image.resize((128, 128), Image.LANCZOS)

        # Convert the image to an indexed bitmap
        indexed_image = resized_image.convert("P", palette=Image.ADAPTIVE)

        # Save the current bitmap (this is what the MagTag will fetch)
        current_bmp_path = images_dir / "murica.bmp"
        indexed_image.save(current_bmp_path)
        print(f"Saved current bitmap: {current_bmp_path}")
        
        # Also save an archived version with timestamp
        archived_bmp_path = images_dir / f"{timestamp}-bitmap.bmp"
        indexed_image.save(archived_bmp_path)
        print(f"Saved archived bitmap: {archived_bmp_path}")

        # Clean up temporary file
        Path("temp_generated.png").unlink()
        
        print("Image generation and processing completed successfully!")
        
        # Create or update index file for easy browsing
        create_image_index(images_dir)
        
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)

def create_image_index(images_dir):
    """Create an HTML index file for browsing historical images"""
    index_path = images_dir / "index.html"
    
    # Get all image files
    original_images = sorted(images_dir.glob("*-original.png"), reverse=True)    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>PatrIoT - Daily Patriotic Images</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .current { background: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
        .archive { margin-top: 30px; }
        .image-entry { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .timestamp { color: #666; font-size: 0.9em; }
        img { max-width: 200px; height: auto; margin: 10px; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h1>🇺🇸 PatrIoT - Daily Patriotic Images</h1>
    
    <div class="current">
        <h2>Current Image (for MagTag display)</h2>
        <p>This is the latest image that the MagTag device will download and display.</p>
        <img src="murica.bmp" alt="Current patriotic image" />
        <br>
        <a href="murica.bmp" download>Download murica.bmp</a>
    </div>
    
    <div class="archive">
        <h2>Image Archive</h2>
        <p>Historical patriotic images generated daily by AI.</p>
"""
    
    # Add archived images
    for i, original_path in enumerate(original_images[:30]):  # Show last 30 images
        timestamp = original_path.stem.split('-')[0]
        try:
            date = datetime.datetime.fromtimestamp(int(timestamp))
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, IndexError):
            date_str = "Unknown date"
            
        bitmap_path = images_dir / f"{timestamp}-bitmap.bmp"
        
        html_content += f"""
        <div class="image-entry">
            <div class="timestamp">{date_str}</div>
            <img src="{original_path.name}" alt="Original image from {date_str}" />
            <img src="{bitmap_path.name}" alt="Bitmap version from {date_str}" />
            <br>
            <a href="{original_path.name}" download>Original PNG</a> | 
            <a href="{bitmap_path.name}" download>Bitmap BMP</a>
        </div>
"""
    
    html_content += """
    </div>
    
    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; color: #666;">
        <p>Generated automatically by GitHub Actions using OpenAI DALL-E</p>
        <p>Part of the <a href="https://github.com/pid1/patrIoT">PatrIoT project</a> - Daily AI-generated patriotic images for AdaFruit MagTag</p>
    </footer>
</body>
</html>
"""
    
    with open(index_path, 'w') as f:
        f.write(html_content)
    
    print(f"Created image index: {index_path}")

if __name__ == "__main__":
    main()
