import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import librosa
import numpy as np

def debug_model():
    """Debug the emotion recognition model to understand its capabilities"""
    
    model_name = "firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3"
    
    print("🔍 Debugging Speech Emotion Recognition Model")
    print("=" * 50)
    
    try:
        # Load model and feature extractor
        print("Loading model...")
        model = AutoModelForAudioClassification.from_pretrained(model_name)
        feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
        
        print(f"✅ Model loaded successfully")
        print(f"📋 Model name: {model_name}")
        print(f"📋 Model type: {type(model).__name__}")
        
        # Check model configuration
        config = model.config
        print(f"\n🔧 Model Configuration:")
        print(f"   Num labels: {config.num_labels}")
        
        # Check emotion labels
        if hasattr(config, 'id2label'):
            print(f"\n🏷️  Emotion Labels:")
            for id, label in config.id2label.items():
                print(f"   {id}: {label}")
        else:
            print("⚠️  No emotion labels found in model config")
        
        # Check feature extractor
        print(f"\n🎤 Feature Extractor:")
        print(f"   Sampling rate: {feature_extractor.sampling_rate}")
        print(f"   Feature size: {feature_extractor.feature_size if hasattr(feature_extractor, 'feature_size') else 'Unknown'}")
        
        # Test with a sample audio file
        print(f"\n🧪 Testing with sample audio...")
        
        # Load a sample audio file
        sample_files = [
            "sample_audio/happy_sample_1.wav",
            "sample_audio/angry_sample_1.wav",
            "sample_audio/sad_sample_1.wav"
        ]
        
        for sample_file in sample_files:
            try:
                print(f"\n📁 Testing: {sample_file}")
                
                # Load and preprocess audio
                audio, sr = librosa.load(sample_file, sr=feature_extractor.sampling_rate)
                print(f"   Audio length: {len(audio)} samples ({len(audio)/sr:.2f} seconds)")
                print(f"   Audio range: [{audio.min():.3f}, {audio.max():.3f}]")
                
                # Extract features
                inputs = feature_extractor(
                    audio, 
                    sampling_rate=feature_extractor.sampling_rate, 
                    return_tensors="pt",
                    padding=True
                )
                
                print(f"   Input shape: {inputs.input_values.shape}")
                
                # Make prediction
                with torch.no_grad():
                    outputs = model(**inputs)
                    logits = outputs.logits
                    predictions = torch.nn.functional.softmax(logits, dim=-1)
                
                print(f"   Logits shape: {logits.shape}")
                print(f"   Predictions shape: {predictions.shape}")
                print(f"   Raw logits: {logits[0].tolist()}")
                print(f"   Softmax probs: {predictions[0].tolist()}")
                
                # Get predicted emotion
                predicted_id = predictions.argmax().item()
                confidence = predictions.max().item()
                
                if hasattr(config, 'id2label'):
                    predicted_emotion = config.id2label[predicted_id]
                    print(f"   🎯 Predicted: {predicted_emotion} (confidence: {confidence:.3f})")
                else:
                    print(f"   🎯 Predicted ID: {predicted_id} (confidence: {confidence:.3f})")
                
                break  # Just test one file for now
                
            except Exception as e:
                print(f"   ❌ Error testing {sample_file}: {e}")
                continue
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        
        # Try alternative approach - check if model exists
        try:
            from huggingface_hub import model_info
            info = model_info(model_name)
            print(f"\n📋 Model Info from Hub:")
            print(f"   Tags: {info.tags}")
            print(f"   Task: {info.pipeline_tag}")
            print(f"   Downloads: {info.downloads}")
        except Exception as e2:
            print(f"❌ Could not get model info: {e2}")

def test_alternative_models():
    """Test some alternative emotion recognition models"""
    
    alternative_models = [
        "superb/hubert-large-superb-er",
        "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
        "Emotional/wav2vec2-large-robust-12-ft-emotion-msp-dim"
    ]
    
    print("\n🔄 Testing Alternative Models:")
    print("=" * 40)
    
    for model_name in alternative_models:
        try:
            print(f"\n📋 Testing: {model_name}")
            model = AutoModelForAudioClassification.from_pretrained(model_name)
            
            config = model.config
            print(f"   ✅ Model loaded successfully")
            print(f"   Num labels: {config.num_labels}")
            
            if hasattr(config, 'id2label'):
                print(f"   Emotions: {list(config.id2label.values())}")
            else:
                print(f"   No emotion labels found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    debug_model()
    test_alternative_models()
