import pytest
import sys
sys.path.append('../modules')
import struct
import tempfile
from text_to_speech import text_to_speech


class TestClassTTS:
    STRING_INPUT = "hello world"
    STRING_INPUT_NULL = ''
    FORMAT_TYPE = b''

    def test_returns_Wav(self):
        format_type = self.FORMAT_TYPE
        stringInput = self.STRING_INPUT

        with tempfile.TemporaryFile() as f:
            f.write(text_to_speech(stringInput))
            f.seek(8)
            
            header = f.read(4)
            format_type = struct.unpack('<4s', header)[0]
            
        assert format_type == b'WAVE'

    def test_handles_null(self):
        stringInputNull = self.STRING_INPUT_NULL
        try:
            ttsWav = text_to_speech(stringInputNull)
            assert True
        except RuntimeError: 
            pytest.fail(f"Exception raise on null input {RuntimeError}")

    def test_content_file_size_not_null(self):
        stringInput = self.STRING_INPUT

        with tempfile.TemporaryFile() as f:
            f.write(text_to_speech(stringInput))
            f.seek(40)
            
            header = f.read(4)
            content_size = struct.unpack('<I', header)[0]

        assert content_size > 0
        assert content_size < 4000000



