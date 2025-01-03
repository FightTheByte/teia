import numpy as np
import cv2
import time
import copy
import requests
import threading
import os
import simpleaudio as sa
import onnxruntime as ort
import torch
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
from pynput import keyboard


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# init global variables
mode = 1  
audio_thread = None

# Initialize model and labels
labels = ['obstacle', 'path straight', 'steps', 'zebra crossing']
ort_session = ort.InferenceSession('./most_accurate_model.onnx')
model_id = "gokaygokay/sd3-long-captioner"

# Load the captioning model and processor
caption_model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to('cuda').eval()
processor = AutoProcessor.from_pretrained(model_id)

# Init video source
vid = cv2.VideoCapture(0)

#audio interface
def play_audio_non_blocking(audio_file):
    global audio_thread

    def play_audio():
        wave_obj = sa.WaveObject.from_wave_file(audio_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()  

    if audio_thread and audio_thread.is_alive():
        audio_thread.join()  

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()

# Process frame
def process_image(image):
    image = cv2.resize(image, (400, 400)) 
    image = image.astype(np.float32) / 255.0 
    image = np.expand_dims(image, axis=0)  
    image = np.transpose(image, (0, 2, 1, 3))  
    return image

# Inference function
def path_inference(frame, previous_inference, interval):
    time.sleep(interval)
    # Process image and get input/output
    input = process_image(frame)
    input_info = ort_session.get_inputs()[0]
    input_name = input_info.name
    output_name = ort_session.get_outputs()[0].name
    
    # Run the inference
    predictions = ort_session.run([output_name], {input_name: input})
    probabilities = predictions[0][0]

    hits = []
    playback = []

    for index, value in enumerate(probabilities):        
        if value > 0.5:
            hits.append(labels[index])
    print(previous_inference)
 
    if hits:
        playback = [hit for hit in hits if hit not in previous_inference]

        if playback:
            playthis = ' '.join(playback)
            # Make a call to Watson for embed Text to Speech
            response = requests.post(
                'http://localhost:1080/text-to-speech/api/v1/synthesize',
                json={
                    "voice": "en-GB_KateV3Voice",
                    "output": "output.wav",
                    "text": playthis
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "audio/wav"
                }
            )
            
            if response.status_code == 200:
                with open('output.wav', 'wb') as file:
                    file.write(response.content)
                play_audio_non_blocking('output.wav')
            else:
                print("Error: Failed to synthesize audio")

        previous_inference = copy.deepcopy(hits)

    return previous_inference

# caption function
def caption_inference(frame, interval):
    time.sleep(interval)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
     
    prompt = "<image> describe the scene flip left and right directions <bos>"
    model_inputs = processor(text=prompt, images=image, return_tensors="pt").to('cuda')
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

        print(f"Generated caption: {playthis}")
        # Make a call to Watson for embed Text to Speech
        response = requests.post(
            'http://localhost:1080/text-to-speech/api/v1/synthesize',
            json={
                "voice": "en-GB_KateV3Voice",
                "output": "output.wav",
                "text": "{}".format(playthis)
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "audio/wav"
            }
        )
        if response.status_code == 200:
            with open('output2.wav', 'wb') as file:
                file.write(response.content)
            print("Audio synthesized successfully.")
        else:
            print(f"Error in TTS request: {response.status_code}")

        play_audio_non_blocking('output2.wav')

# Camera loop function with mode switching
def startCameraLoop(interval = 5, previous_inference = []):
    while True:
        global i
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break  

        # Switch between inference modes
        if mode == 0:
            interval = 5
            previous_inference = path_inference(frame, previous_inference, interval)
        elif mode == 1:
            interval = 40
            caption_inference(frame, interval)
        elif mode == 2:
            interval = 5
            time.sleep(interval)


       
# Set key listener
def on_press(key):
    global mode
    if key == keyboard.Key.media_play_pause:
        mode = (mode + 1)%3
        if mode == 0:
            play_audio_non_blocking('path.wav')
        if mode == 1:
            play_audio_non_blocking('caption.wav')
        if mode == 2:
            play_audio_non_blocking('silent.wav')
          


listener = keyboard.Listener(on_press=on_press)
listener.start()


# Start the camera loop
startCameraLoop()

vid.release()
cv2.destroyAllWindows()
