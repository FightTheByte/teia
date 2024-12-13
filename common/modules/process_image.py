import cv2
import numpy as np 
from PIL import Image

# Process frame
def process_image(image, mode):
    #path mode
    if mode == 0:
        image = cv2.resize(image, (400, 400)) 
        image = image.astype(np.float32) / 255.0 
        image = np.expand_dims(image, axis=0)  
        image = np.transpose(image, (0, 2, 1, 3))
        np_array = image

        return np_array
    # caption mode
    else: 
        image = cv2.resize(image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return image
    