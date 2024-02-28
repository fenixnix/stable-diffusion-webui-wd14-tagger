import io,re,base64
from PIL import Image

def base64_to_image(base64_str: str) -> Image.Image:
    #base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_str)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    return img