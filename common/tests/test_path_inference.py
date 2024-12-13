import pytest
import sys
from PIL import Image
import cv2
sys.path.append('../modules')
from path_inference import path_inference


class TestClassPathInference:
    IMAGE_SOURCE = './assets/test.jpg'

    def testPreviousInferenceArrayReturned(self):
        image_source = self.IMAGE_SOURCE
        image = cv2.imread(image_source)
        previous_inference, playback = path_inference(image)
        
        assert type(previous_inference) == list
    def testIsPlaybackArrayReturned(self):
        image = cv2.imread('./assets/test.jpg')
        previous_inference, playback = path_inference(image)

        assert type(playback) == list

    def testPlaybackElementsCorrect(self):
        image_source = self.IMAGE_SOURCE
        image = cv2.imread(image_source)
        previous_inference, playback = path_inference(image)
        assertion = True if 'path straight' and 'steps' in playback else False
        assert assertion

    def testPreviousInferenceElementsCorrect(self):
        image_source = self.IMAGE_SOURCE
        image = cv2.imread(image_source)
        previous_inference, playback = path_inference(image)
        assertion_prev = True if 'path straight' and 'steps' in playback else False
        previous_inference, playback = path_inference(image, previous_inference)
        assertion = True if len(playback) == 0 else False
        assert assertion_prev  
        assert assertion  

    def testHandlesEmptyInput(self):
        previous_inference, playback = path_inference()

        assert len(previous_inference) == 0
        assert len(playback) == 0
    
    