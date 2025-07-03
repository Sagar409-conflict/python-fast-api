import requests
import os
import glob
from pathlib import Path
import json

def test_speech_emotion_api():
    """Test the speech emotion recognition API with generated human speech samples"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Server is not running. Please start the FastAPI server first.")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the FastAPI server first.")
        print("Run: python main.py")
        return
    
    print("🎤 Testing Speech Emotion Recognition API")
    print("=" * 50)
    
    # Get model info
    try:
        response = requests.get(f"{base_url}/speech-emotion/model-info")
        model_info = response.json()
        print(f"📋 Model: {model_info['model_name']}")
        print(f"📋 Description: {model_info['description']}")
        print()
    except Exception as e:
        print(f"⚠️  Could not get model info: {e}")
    
    # Test with generated human speech samples
    sample_dir = Path("sample_audio")
    if not sample_dir.exists():
        print(f"❌ Sample audio directory '{sample_dir}' not found.")
        print("Please run 'python generate_emotional_speech.py' first.")
        return
    
    # Group files by emotion
    emotions = {}
    for wav_file in sample_dir.glob("*_sample_*.wav"):
        emotion = wav_file.stem.split('_sample_')[0]
        if emotion not in emotions:
            emotions[emotion] = []
        emotions[emotion].append(wav_file)
    
    if not emotions:
        print("❌ No emotional speech samples found.")
        return
    
    print(f"🎯 Found {len(emotions)} different emotions with sample files")
    print()
    
    # Test each emotion
    results = {}
    
    for emotion, files in emotions.items():
        print(f"🧪 Testing {emotion.upper()} emotion...")
        emotion_results = []
        
        # Test up to 2 samples per emotion to avoid spam
        test_files = files[:2]
        
        for file_path in test_files:
            try:
                # Test public endpoint (no authentication)
                with open(file_path, 'rb') as audio_file:
                    response = requests.post(
                        f"{base_url}/analyze-speech-emotion-public",
                        files={"audio_file": (file_path.name, audio_file, "audio/wav")}
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    emotion_results.append(result)
                    
                    print(f"  📁 File: {file_path.name}")
                    print(f"  🎯 Predicted: {result['predicted_emotion']} ({result['confidence']:.3f})")
                    print(f"  ⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
                    
                    # Show top 3 emotions
                    sorted_emotions = sorted(result['all_emotions'].items(), 
                                           key=lambda x: x[1], reverse=True)
                    print(f"  📊 Top 3 emotions:")
                    for emo, conf in sorted_emotions[:3]:
                        print(f"     {emo}: {conf:.3f}")
                    print()
                    
                else:
                    print(f"  ❌ Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Error processing {file_path.name}: {e}")
        
        results[emotion] = emotion_results
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 30)
    
    correct_predictions = 0
    total_predictions = 0
    
    for true_emotion, emotion_results in results.items():
        if not emotion_results:
            continue
            
        correct_count = 0
        for result in emotion_results:
            total_predictions += 1
            predicted = result['predicted_emotion'].lower()
            
            # Check if prediction matches (allowing for some variation)
            if (true_emotion in predicted or predicted in true_emotion or
                (true_emotion == "fearful" and "fear" in predicted) or
                (true_emotion == "surprised" and "surprise" in predicted)):
                correct_count += 1
                correct_predictions += 1
        
        accuracy = (correct_count / len(emotion_results)) * 100 if emotion_results else 0
        print(f"{true_emotion.capitalize()}: {correct_count}/{len(emotion_results)} correct ({accuracy:.1f}%)")
    
    overall_accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    print(f"\n🎯 Overall Accuracy: {correct_predictions}/{total_predictions} ({overall_accuracy:.1f}%)")
    
    # Save detailed results
    with open("emotion_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed results saved to 'emotion_test_results.json'")

def test_with_custom_audio(file_path: str):
    """Test the API with a custom audio file"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    base_url = "http://localhost:8000"
    
    print(f"🎤 Testing custom audio file: {file_path}")
    
    try:
        with open(file_path, 'rb') as audio_file:
            response = requests.post(
                f"{base_url}/analyze-speech-emotion-public",
                files={"audio_file": (os.path.basename(file_path), audio_file, "audio/wav")}
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"🎯 Predicted emotion: {result['predicted_emotion']}")
            print(f"🔢 Confidence: {result['confidence']:.3f}")
            print(f"⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
            print("\n📊 All emotion scores:")
            
            sorted_emotions = sorted(result['all_emotions'].items(), 
                                   key=lambda x: x[1], reverse=True)
            for emotion, confidence in sorted_emotions:
                print(f"  {emotion}: {confidence:.3f}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Speech Emotion Recognition API Tester")
    print("=" * 50)
    
    # Test with generated samples
    test_speech_emotion_api()
    
    # Optionally test with a specific file
    # test_with_custom_audio("sample_audio/happy_sample_1.wav")
