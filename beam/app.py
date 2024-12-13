from beam import endpoint, Image, env
import io
import base64
from PIL import Image as PILImage
import onnxruntime as ort
import copy
import numpy as np
import cv2

MODE_PATH = './most_accurate_model.onnx'
LABELS = ['obstacle', 'path straight', 'steps', 'zebra crossing']
ORT_SESSION = ort.InferenceSession('most_accurate_model.onnx')

@endpoint(
    name="inference",
    cpu=1,
    memory="5Gi",
    gpu="T4",
    image = (
        Image(
            python_version="python3.8",
            python_packages=[
                "onnxruntime-gpu",
                "numpy",
                "opencv-python",
                "Pillow"
            ]
        )
        .add_commands([
            "apt-get update -y",
            "apt-get install -y libgl1 libglib2.0-0"
        ])
    )
)
def inference(frame: str):
   
    if not frame:
        return {"error": "no file"}
    
    previous_inference = []

    frame = np.array(frame)

    def process_image(image):
        image_data = base64.b64decode(image)
        image = PILImage.open(io.BytesIO(image_data))
        image = np.array(image)
        image = cv2.resize(image, (400, 400))  
        image = image.astype(np.float32) / 255.0  
        image = np.expand_dims(image, axis=0)  
        image = np.transpose(image, (0, 2, 1, 3)) 
        return image

    try:
        # Process image and get input/output
        input = process_image(frame)
        input_info = ORT_SESSION.get_inputs()[0]
        input_name = input_info.name
        output_name = ORT_SESSION.get_outputs()[0].name
        
        # Run the inference
        predictions = ORT_SESSION.run([output_name], {input_name: input})
        probabilities = predictions[0][0]

        hits = []
        playback = []

        for index, value in enumerate(probabilities):        
            if value > 0.5:
                hits.append(LABELS[index])
    
        if hits:
            playback = [hit for hit in hits if hit not in previous_inference]

        if playback:
            playthis = ' '.join(playback)

        previous_inference = copy.deepcopy(hits)

        return {"result": playback, "previous_inference": previous_inference}
    except ValueError:
        return {"result": "error during inference" }
    

            


