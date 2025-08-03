import requests
import urllib.parse
import random
from PIL import Image
import io
import os

project_path = "" # replace with the path you put your project into

def generate_image(prompt='an anime cat with a yellow and white colour scheme', width=50, height=50):
    encoded_prompt = urllib.parse.quote(prompt)

    params = {
        'seed': random.randint(0, 100000),
        'nologo': 'true',
        'private': 'true',
        'safe': 'true', # props to pollinations.ai for including this! honestly it's a lot better than any word blacklisting you could think of
        'model': 'flux',
        'width': '500',
        'height': '500',
    }
    path = f'{project_path}/images/{encoded_prompt}.jpg'
    if f'{encoded_prompt}.jpg' in os.listdir(f'{project_path}/images'):
        with open(path, 'rb') as f:
            response = f.read()
        img = Image.open(io.BytesIO(response)).convert('RGB')
    else:
        url = f'https://image.pollinations.ai/prompt/{encoded_prompt}'
        response = requests.get(url, params=params)
        
        if response.status_code < 200 or response.status_code > 299: # anything not in the 200s is likely an error
            return
        
        with open(path, 'wb') as f:
            f.write(response.content)
        img = Image.open(io.BytesIO(response.content)).convert('RGB')

    img = img.resize((50, 50)) # image is resized to 50x50 px, you could just enter 50x50 in to the request params, but i prefer to store higher resolution images for future use, e.g. training a student model.
    pixels = list(img.getdata()) # here we convert from .jpg to raw pixels, which we can send over to scratch without any encoding, since RGB values are already numbers!
    rgb_string = ''.join(f'{r:03}{g:03}{b:03}' for r, g, b in pixels)
    return rgb_string
