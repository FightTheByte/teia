import threading
import simpleaudio as sa
import os

#audio interface
class PlayAudio:
    def __init__(self):
        self.threads = []
        self.currently_playing = threading.Event()
        self.lock = threading.Lock()

    def play_audio(self, audio_file):
        try:
            wave_obj = sa.WaveObject.from_wave_file(audio_file)
            self.currently_playing.set()
            play_obj = wave_obj.play()
            play_obj.wait_done()
            play_obj.stop() 
        except Exception as e:
            print(f'error here {e}') 
        finally:
            if audio_file != 'path.wav' and audio_file != 'silent.wav' and audio_file != 'caption.wav':
                os.remove(audio_file)
            self.currently_playing.clear()

    def append_thread(self, audio_file):
        with self.lock:
            thread = threading.Thread(target=self.play_audio, args=(audio_file,))
            self.threads.append(thread)

    def play_threads(self):
        while True:
            with self.lock:   
                if len(self.threads) < 1: 
                    break
                thread = self.threads.pop(0)  
                thread.start()
                thread.join()

            
                                