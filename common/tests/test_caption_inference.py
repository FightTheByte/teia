import pytest
import sys
import cv2
sys.path.append('../modules')
from caption_inference import caption_inference
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

class TestCaptionInference:
    IMAGE_SOURCE = './assets/test.jpg'
    model_id = "gokaygokay/sd3-long-captioner"
    caption_model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to('cuda').eval()
    processor = AutoProcessor.from_pretrained(model_id)

    def testReturnsString(self):
        image_source = self.IMAGE_SOURCE
        image = cv2.imread(image_source)
        inference = caption_inference(self.processor, self.caption_model, image)
        assert type(inference) == str

    def testReturnsContent(self):
        image_source = self.IMAGE_SOURCE
        image = cv2.imread(image_source)
        inference = caption_inference(self.processor, self.caption_model, image)
        assert len(inference) > 5

    def testHandlesNone(self):
        inference = caption_inference(self.processor, self.caption_model)
        assert len(inference) == 0