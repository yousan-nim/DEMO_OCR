import re 
import base64

import numpy as np 

from PIL import Image 
from io import BytesIO 

def base64_to_pil(image_base64): 
    # Convert base64 image data to PIL image 
    image_data = re.sub('^data:image/.+;base64,', '', image_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image


def np_to_base64(image_np): 
    # Convert numpy image (RGB) to base64 string
    image = Image.fromarray(image_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return u"data:image/png;base64" + base64.b64encode(buffered.getvalue()).decode("ascii")