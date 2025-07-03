import requests
import os

def test_speech_emotion_api():
    """
    Test the speech emotion recognition API with sample files
    """
    base_url = "http://localhost:8000"
    
    # Test model info endpoint
    print("=== Testing Model Info Endpoint ===")
    try:
        response = requests.get(f"{base_url}/speech-emotion/model-info")
        if response.status_code == 200:
            model_info = response.json()
            print("✅ Model info retrieved successfully:")
            print(f"   Model: {model_info.get('model_name', 'Unknown')}")
            print(f"   Supported formats: {model_info.get('supported_formats', [])}")
        else:
            print(f"❌ Failed to get model info: {response.status_code}")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        return
    
    # Test with sample audio files
    print("\n=== Testing Speech Emotion Recognition ===")
    
    # List of sample files to test
    sample_files = [
        "sample_audio.wav",
        "sample_audio/happy_tone.wav",
        "sample_audio/sad_tone.wav",
        "sample_audio/neutral_tone.wav"
    ]
    
    for audio_file in sample_files:
        if os.path.exists(audio_file):
            print(f"\n📄 Testing with: {audio_file}")
            try:
                with open(audio_file, 'rb') as f:
                    files = {'audio_file': (audio_file, f, 'audio/wav')}
                    response = requests.post(
                        f"{base_url}/analyze-speech-emotion-public",
                        files=files
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Analysis successful:")
                    print(f"   Predicted emotion: {result.get('predicted_emotion', 'Unknown')}")
                    print(f"   Confidence: {result.get('confidence', 0):.2%}")
                    print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
                    print(f"   Model: {result.get('model_name', 'Unknown')}")
                    
                    # Show top 3 emotions
                    all_emotions = result.get('all_emotions', {})
                    if all_emotions:
                        sorted_emotions = sorted(all_emotions.items(), key=lambda x: x[1], reverse=True)
                        print("   Top 3 emotions:")
                        for emotion, score in sorted_emotions[:3]:
                            print(f"     {emotion}: {score:.2%}")
                else:
                    print(f"❌ Analysis failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error processing {audio_file}: {e}")
        else:
            print(f"⚠️  File not found: {audio_file}")
    
    print("\n=== Test Complete ===")
    print("Note: The model will be downloaded on first use, which may take some time.")
    print("Subsequent requests will be much faster.")

def test_invalid_file():
    """Test with invalid file types"""
    print("\n=== Testing Invalid File Handling ===")
    
    # Create a fake text file
    with open("test_invalid.txt", "w") as f:
        f.write("This is not an audio file")
    
    try:
        with open("test_invalid.txt", "rb") as f:
            files = {'audio_file': ("test_invalid.txt", f, 'text/plain')}
            response = requests.post(
                "http://localhost:8000/analyze-speech-emotion-public",
                files=files
            )
        
        if response.status_code == 400:
            print("✅ Invalid file type correctly rejected")
            print(f"   Error message: {response.json().get('detail', 'No message')}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing invalid file: {e}")
    
    finally:
        # Clean up
        if os.path.exists("test_invalid.txt"):
            os.remove("test_invalid.txt")

if __name__ == "__main__":
    print("🎤 Speech Emotion Recognition API Test")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server not responding correctly")
            exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        exit(1)
    
    # Run tests
    test_speech_emotion_api()
    test_invalid_file()
    
    print("\n🎉 All tests completed!")
    print("\nTo test manually:")
    print("1. Open http://localhost:8000/docs in your browser")
    print("2. Navigate to the 'analyze-speech-emotion-public' endpoint")
    print("3. Upload one of the generated WAV files")
    print("4. Click 'Execute' to see the emotion analysis results")
