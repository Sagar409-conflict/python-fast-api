import pytest
import io
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_model_info():
    """Test getting model information"""
    response = client.get("/api/v1/speech-emotion/info")
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition" in data["model_name"]

def test_speech_emotion_public_no_file():
    """Test speech emotion endpoint without file"""
    response = client.post("/api/v1/speech-emotion/analyze-public")
    assert response.status_code == 422  # Unprocessable Entity (missing file)

def test_speech_emotion_public_invalid_file_type():
    """Test speech emotion endpoint with invalid file type"""
    # Create a fake text file
    fake_file = io.BytesIO(b"This is not an audio file")
    
    response = client.post(
        "/api/v1/speech-emotion/analyze-public",
        files={"audio_file": ("test.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
    assert "Only WAV audio files are supported" in response.json()["detail"]

def test_speech_emotion_public_empty_file():
    """Test speech emotion endpoint with empty WAV file"""
    # Create an empty file with WAV extension
    empty_file = io.BytesIO(b"")
    
    response = client.post(
        "/api/v1/speech-emotion/analyze-public",
        files={"audio_file": ("empty.wav", empty_file, "audio/wav")}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_speech_emotion_protected_without_auth():
    """Test protected speech emotion endpoint without authentication"""
    fake_file = io.BytesIO(b"fake audio content")
    
    response = client.post(
        "/api/v1/speech-emotion/analyze",
        files={"audio_file": ("test.wav", fake_file, "audio/wav")}
    )
    assert response.status_code == 403  # Forbidden (no auth)

# Note: Testing with real audio files would require:
# 1. A sample WAV file
# 2. The actual model to be loaded (which takes time and resources)
# For CI/CD, you might want to mock the speech_emotion module

@pytest.mark.skip(reason="Requires actual WAV file and model loading")
def test_speech_emotion_with_real_audio():
    """Test speech emotion with a real WAV file (skipped by default)"""
    # This test would require a real WAV file and model loading
    # Uncomment and modify when you have a test audio file
    
    # with open("test_audio.wav", "rb") as audio_file:
    #     response = client.post(
    #         "/api/v1/speech-emotion/analyze-public",
    #         files={"audio_file": ("test.wav", audio_file, "audio/wav")}
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert "predicted_emotion" in data
    #     assert "confidence" in data
    #     assert "all_emotions" in data
    #     assert "model_used" in data
    #     assert isinstance(data["confidence"], float)
    #     assert 0 <= data["confidence"] <= 1
    pass
