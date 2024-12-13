import requests

def text_to_speech(stringInput):
    response = requests.post(
                'http://localhost:1080/text-to-speech/api/v1/synthesize',
                json={
                    "voice": "en-GB_KateV3Voice",
                    "output": "output.wav",
                    "text": "{}".format(stringInput)
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "audio/wav"
                }
    )
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error in TTS request: {response.status_code}")