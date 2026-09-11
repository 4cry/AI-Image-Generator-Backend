import os
import requests
import urllib.parse
import random
from PIL import Image
import io

project_path = os.path.dirname(os.path.abspath(__file__))
_image_dir = os.path.join(project_path, "images")
os.makedirs(_image_dir, exist_ok=True)
_image_cache = set(os.listdir(_image_dir))


def generate_image(prompt='an anime cat with a yellow and white colour scheme', width=50, height=50):
    encoded_prompt = urllib.parse.quote(prompt)
    filename = f"{encoded_prompt}.jpg"
    path = os.path.join(_image_dir, filename)

    if filename in _image_cache:
        with open(path, "rb") as f:
            data = f.read()
    else:
        params = {
            "seed": random.randint(0, 100000),
            "nologo": "true",
            "private": "true",
            "safe": "true",
            "model": "flux",
            "width": "500",
            "height": "500",
        }
        resp = requests.get(f"https://image.pollinations.ai/prompt/{encoded_prompt}", params=params, timeout=30)
        if resp.status_code != 200:
            return None
        data = resp.content
        with open(path, "wb") as f:
            f.write(data)
        _image_cache.add(filename)

    img = Image.open(io.BytesIO(data)).convert("RGB")
    del data
    img = img.resize((50, 50))
    pixels = img.getdata()
    rgb_string = "".join(f"{r:03}{g:03}{b:03}" for r, g, b in pixels)
    img.close()
    return rgb_string
