import os
import tempfile
from typing import Dict, Any
import torch
import librosa
import soundfile as sf
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import numpy as np

class SpeechEmotionRecognizer:
    def __init__(self):
        self.model_name = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
        self.model = None
        self.feature_extractor = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model and feature extractor"""
        try:
            print(f"Loading model: {self.model_name}")
            self.model = AutoModelForAudioClassification.from_pretrained(self.model_name)
            self.feature_extractor = AutoFeatureExtractor.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
    
    def preprocess_audio(self, audio_path: str, target_sample_rate: int = 16000) -> np.ndarray:
        """
        Preprocess audio file for emotion recognition
        """
        try:
            # Load audio file
            audio, sr = librosa.load(audio_path, sr=target_sample_rate)
            
            # Ensure audio is not empty
            if len(audio) == 0:
                raise ValueError("Audio file is empty")
            
            # Normalize audio
            audio = audio / np.max(np.abs(audio))
            
            return audio
        except Exception as e:
            print(f"Error preprocessing audio: {e}")
            raise e
    
    def predict_emotion(self, audio_path: str) -> Dict[str, Any]:
        """
        Predict emotion from audio file
        """
        try:
            # Preprocess audio
            audio = self.preprocess_audio(audio_path)
            
            # Extract features
            inputs = self.feature_extractor(
                audio, 
                sampling_rate=16000, 
                return_tensors="pt",
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get the predicted emotion
            predicted_class_id = predictions.argmax().item()
            confidence = predictions.max().item()
            
            # Map class ID to emotion label
            emotion_labels = self.model.config.id2label
            predicted_emotion = emotion_labels[predicted_class_id]
            
            # Get all emotion probabilities
            all_emotions = {}
            for class_id, emotion in emotion_labels.items():
                all_emotions[emotion] = float(predictions[0][class_id].item())
            
            return {
                "predicted_emotion": predicted_emotion,
                "confidence": float(confidence),
                "all_emotions": all_emotions,
                "model_name": self.model_name
            }
            
        except Exception as e:
            print(f"Error predicting emotion: {e}")
            raise e
    
    def predict_emotion_from_bytes(self, audio_bytes: bytes, filename: str = "temp.wav") -> Dict[str, Any]:
        """
        Predict emotion from audio bytes
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            # Predict emotion
            result = self.predict_emotion(temp_path)
            return result
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

# Global instance
speech_emotion_recognizer = None

def get_speech_emotion_recognizer() -> SpeechEmotionRecognizer:
    """Get or create the global speech emotion recognizer instance"""
    global speech_emotion_recognizer
    if speech_emotion_recognizer is None:
        speech_emotion_recognizer = SpeechEmotionRecognizer()
    return speech_emotion_recognizer
