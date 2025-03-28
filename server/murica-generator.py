#!/usr/bin/env python3

import datetime
import os
import requests
from openai import OpenAI
from PIL import Image

api_key=os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)

response = client.images.generate(
    model="dall-e-3",
    prompt="a patriotic image representing the United States of America to be displayed on a small, black and white, low resolution display, so include fewer, larger items and not too much background detail",
    size="1024x1024",
    quality="standard",
    n=1,
)

image_url = response.data[0].url

# Retrieve and save the generated image
image_response = requests.get(image_url)
if image_response.status_code == 200:
    with open("generated_image.png", "wb") as f:
        f.write(image_response.content)
else:
    print("Failed to retrieve the image")

# Open the saved image
image = Image.open("generated_image.png")

timestamp = int(datetime.datetime.now().timestamp())

# Write the original image out to disk
image.save(f"/opt/murica/{timestamp}-original.png")

# Resize the image
resized_image = image.resize((128, 128), Image.LANCZOS)

# Convert the image to an indexed bitmap
indexed_image = resized_image.convert("P", palette=Image.ADAPTIVE)

# Save the indexed bitmap
indexed_image.save("/opt/murica/murica.bmp")
indexed_image.save (f"/opt/murica/{timestamp}-bitmap.bmp")
