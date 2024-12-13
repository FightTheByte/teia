import pytest
import sys
sys.path.append('../modules')
import numpy as np
from PIL import Image
import cv2
from process_image import process_image



class TestClassProcessImage:
    IMAGE_SOURCE = './assets/test.jpg'

    def testIsPathNpArray(self):
        image = self.IMAGE_SOURCE
        image_input = cv2.imread(image)
        np_array = process_image(image_input, 1)
        is_np_array = isinstance(np_array, np.ndarray)

        assert is_np_array

    def testIsCaptionPILImage(self):
        image = self.IMAGE_SOURCE
        image_input = cv2.imread(image)
        pil_image = process_image(image_input, 2)
        is_pil_image = isinstance(pil_image, Image.Image)
        
        assert is_pil_image

    def testPathNpArrayShape(self):
        image = self.IMAGE_SOURCE
        image_input = cv2.imread(image)
        np_array = process_image(image_input, 1)
        np_shape = np_array.shape
        is_correct_shape = True if np_shape == (1,224,224,3) else False

        assert is_correct_shape

    def testCaptionImageSize(self):
        image = self.IMAGE_SOURCE
        image_input = cv2.imread(image)
        pil_image = process_image(image_input, 2)
        width, height = pil_image.size
        is_correct_dimensions = True if width == 224 and height == 224 else False

        assert is_correct_dimensions



    