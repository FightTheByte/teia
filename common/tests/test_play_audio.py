import pytest
import sys
import time
sys.path.append('../modules')
import threading
from play_audio import PlayAudio



class TestClassAudio: 
    AUDIO_SOURCE = './assets/output2.wav'
    AUDIO_SOURCE2 = './assets/path.wav'

    def testIsAnInstanceOfPlayAudio(self):
        play_audio = PlayAudio()
        is_audio_instance = isinstance(play_audio, PlayAudio)

        assert is_audio_instance

    def testIsThreadTrackArrayAppending(self):
        audio_source = self.AUDIO_SOURCE
        audio_instance = PlayAudio()

        length_before = len(audio_instance.threads)
        audio_instance.append_thread(audio_source)
        audio_instance.append_thread(audio_source)
        length_after = len(audio_instance.threads)

        threads_length_before_and_after_matching = True if length_before == 0 and length_after == 2 else False
        
        assert threads_length_before_and_after_matching

    def testIsAudioPlaying(self):
        audio_source = self.AUDIO_SOURCE2
        audio_instance = PlayAudio()
        audio_instance.append_thread(audio_source)
        thread = threading.Thread(target=audio_instance.play_threads())
        thread.start()

        audio_is_playing = audio_instance.currently_playing
    
        assert audio_is_playing

    def testAudioThreadsAreNotConcurrent(self):
        audio_source = self.AUDIO_SOURCE
        audio_source2 = self.AUDIO_SOURCE2
        audio_instance = PlayAudio()
        audio_instance.append_thread(audio_source)
        audio_instance.append_thread(audio_source2)

        assert len(audio_instance.threads) == 2

        thread = threading.Thread(target=audio_instance.play_threads)  # Pass method reference
        thread.start()

        time.sleep(1)
        audio_instance.append_thread(audio_source2)
        audio_instance.append_thread(audio_source2)
        assert len(audio_instance.threads) == 3

        thread.join()  

        assert len(audio_instance.threads) == 0
        
        



