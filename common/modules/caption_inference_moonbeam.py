import cv2
import time
import torch 
from PIL import Image

# caption function
def caption_inference(processor, caption_model, frame = None):
    if frame is None:
        return ''
     
    prompt = "<image> describe the scene flip left and right directions <bos>"
    model_inputs = processor(text=prompt, images=frame, return_tensors="pt", do_rescale=False).to('cuda')
    input_len = model_inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = caption_model.generate(
            **model_inputs,
            max_new_tokens=250,  
            do_sample=False,
            repetition_penalty=1.2 
        )
        generation = generation[0][input_len:]
        playthis = processor.decode(generation, skip_special_tokens=True)

        return playthis