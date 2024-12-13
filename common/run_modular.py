import cv2
import time
import threading
import os
import sys
import tempfile
sys.path.append('./modules')
from caption_inference import caption_inference
from path_inference import path_inference
from play_audio import PlayAudio
from process_image import process_image
from text_to_speech import text_to_speech
from pynput import keyboard
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# init global variables
mode = 1  
model_id = "gokaygokay/sd3-long-captioner"
caption_model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to('cuda').eval()
processor = AutoProcessor.from_pretrained(model_id)

# Init video source
vid = cv2.VideoCapture(0)

play_audio = PlayAudio()

def startCameraLoop(interval=5, previous_inference=[]):
    while True:
        global i
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break  

        if mode == 0:
            time.sleep(5)
            frame_path = process_image(frame, mode)
            previous_inference, playback = path_inference(frame_path, previous_inference)
            
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    audio_data = text_to_speech(playback)
                    f.write(audio_data)
                    if f.tell() == 78:
                        f.close()
                        os.remove(f.name)
                        continue
                    if os.path.getsize(f.name) == 0:
                        raise ValueError("Generated audio file is empty.")
                    play_audio.append_thread(f.name)   
                play_audio.play_threads()
                
            except Exception as e:
                print(f'error: {e}')

        elif mode == 1:
            time.sleep(40)
            frame_cap = process_image(frame, mode)
            playback = caption_inference(processor, caption_model, frame_cap)
            
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    audio_data = text_to_speech(playback)
                    f.write(audio_data)
                    if f.tell() == 78:
                        f.close()
                        os.remove(f.name)
                        continue
                    if os.path.getsize(f.name) == 0:
                        raise ValueError("Generated audio file is empty.")
                    play_audio.append_thread(f.name)   
                play_audio.play_threads()
                
            except Exception as e:
                print(f'error: {e}')

        elif mode == 2:
            interval = 5
            time.sleep(interval)


       
# Set key listener
def on_press(key):
    global mode
    if key == keyboard.Key.media_play_pause:
        mode = (mode + 1)%3
        if mode == 0:
            play_audio.append_thread('path.wav')
            thread = threading.Thread(target=play_audio.play_threads())
            thread.start()
        if mode == 1:
            play_audio.append_thread('caption.wav')
            thread = threading.Thread(target=play_audio.play_threads())
            thread.start()
        if mode == 2:
            play_audio.append_thread('silent.wav')
            thread = threading.Thread(target=play_audio.play_threads())
            thread.start()
          


listener = keyboard.Listener(on_press=on_press)
listener.start()


# Start the camera loop
startCameraLoop()

vid.release()
cv2.destroyAllWindows()
