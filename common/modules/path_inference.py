from process_image import process_image
import onnxruntime as ort
import copy
# Inference function
def path_inference(frame = None, previous_inference = []):
    if frame is None: 
        playback = []
        return previous_inference, playback
    
    labels = ['obstacle', 'path straight', 'steps', 'zebra crossing']
    ort_session = ort.InferenceSession('./most_accurate_model.onnx')
    # Process image and get input/output
    input_info = ort_session.get_inputs()[0]
    input_name = input_info.name
    output_name = ort_session.get_outputs()[0].name
    
    # Run the inference
    predictions = ort_session.run([output_name], {input_name: frame})
    probabilities = predictions[0][0]

    hits = []
    playback = []

    for index, value in enumerate(probabilities):        
        if value > 0.5:
            hits.append(labels[index])
 
    if hits:
        playback = [hit for hit in hits if hit not in previous_inference]
        previous_inference = copy.deepcopy(hits)

    return previous_inference, playback