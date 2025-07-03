import asyncio
import edge_tts
import os
from pathlib import Path
import random

class EmotionalSpeechGenerator:
    def __init__(self):
        # Different voice models for different emotions
        self.emotional_voices = {
            "happy": {
                "voice": "en-US-JennyNeural",
                "style": "cheerful",
                "texts": [
                    "I'm so excited about this wonderful opportunity!",
                    "This is absolutely fantastic and amazing!",
                    "I feel so happy and joyful today!",
                    "What a beautiful and wonderful day this is!",
                    "I'm thrilled to share this good news with everyone!"
                ]
            },
            "sad": {
                "voice": "en-US-JennyNeural", 
                "style": "sad",
                "texts": [
                    "I feel so disappointed and heartbroken about this situation.",
                    "This is really difficult for me to accept.",
                    "I'm feeling quite down and melancholy today.",
                    "It's hard to find motivation when things go wrong.",
                    "I wish things could have turned out differently."
                ]
            },
            "angry": {
                "voice": "en-US-JennyNeural",
                "style": "angry", 
                "texts": [
                    "I'm absolutely furious about this unacceptable behavior!",
                    "This is completely outrageous and infuriating!",
                    "I cannot tolerate this kind of treatment anymore!",
                    "This situation makes me incredibly angry and upset!",
                    "I'm fed up with these constant problems and issues!"
                ]
            },
            "neutral": {
                "voice": "en-US-JennyNeural",
                "style": "normal",
                "texts": [
                    "Today's weather forecast shows partly cloudy skies.",
                    "The meeting is scheduled for three o'clock this afternoon.",
                    "Please review the document and send your feedback.",
                    "The quarterly report has been submitted on time.",
                    "The system maintenance will begin at midnight tonight."
                ]
            },
            "surprised": {
                "voice": "en-US-JennyNeural",
                "style": "excited",
                "texts": [
                    "Oh my goodness, I can't believe this happened!",
                    "What an unexpected and surprising turn of events!",
                    "I never saw this coming, what a shock!",
                    "This is absolutely incredible and unbelievable!",
                    "Wow, I'm completely amazed by this revelation!"
                ]
            },
            "fearful": {
                "voice": "en-US-JennyNeural",
                "style": "terrified",
                "texts": [
                    "I'm really scared and worried about what might happen.",
                    "This situation fills me with fear and anxiety.",
                    "I'm terrified of the potential consequences ahead.",
                    "The uncertainty makes me feel nervous and afraid.",
                    "I can't shake this feeling of dread and concern."
                ]
            }
        }
    
    async def generate_emotional_speech(self, emotion: str, output_dir: str = "sample_audio"):
        """Generate emotional speech using Edge TTS"""
        if emotion not in self.emotional_voices:
            raise ValueError(f"Emotion '{emotion}' not supported. Available: {list(self.emotional_voices.keys())}")
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        emotion_config = self.emotional_voices[emotion]
        voice = emotion_config["voice"]
        style = emotion_config["style"]
        texts = emotion_config["texts"]
        
        generated_files = []
        
        for i, text in enumerate(texts):
            output_file = os.path.join(output_dir, f"{emotion}_sample_{i+1}.wav")
            
            # Create SSML with emotion style
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
                   xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
                <voice name="{voice}">
                    <mstts:express-as style="{style}" styledegree="2">
                        {text}
                    </mstts:express-as>
                </voice>
            </speak>
            """
            
            try:
                # Generate speech
                communicate = edge_tts.Communicate(ssml, voice)
                await communicate.save(output_file)
                generated_files.append(output_file)
                print(f"Generated: {output_file}")
                
            except Exception as e:
                print(f"Error generating {emotion} sample {i+1}: {e}")
        
        return generated_files
    
    async def generate_all_emotions(self, output_dir: str = "sample_audio"):
        """Generate sample audio files for all emotions"""
        print("Generating emotional speech samples...")
        
        all_files = []
        for emotion in self.emotional_voices.keys():
            print(f"\nGenerating {emotion} samples...")
            try:
                files = await self.generate_emotional_speech(emotion, output_dir)
                all_files.extend(files)
            except Exception as e:
                print(f"Error generating {emotion} samples: {e}")
        
        print(f"\nGenerated {len(all_files)} audio files in '{output_dir}' directory")
        return all_files

# Alternative using gTTS (Google Text-to-Speech) - simpler but less emotional control
class SimpleSpeechGenerator:
    def __init__(self):
        self.emotional_texts = {
            "happy": [
                "I'm so excited and happy about this wonderful news!",
                "This is absolutely fantastic and brings me so much joy!",
                "I feel incredibly cheerful and optimistic today!"
            ],
            "sad": [
                "I feel so disappointed and heartbroken about this.",
                "This makes me feel really down and melancholy.",
                "I'm struggling with these difficult emotions."
            ],
            "angry": [
                "I'm absolutely furious about this situation!",
                "This is completely unacceptable and makes me angry!",
                "I cannot tolerate this kind of behavior anymore!"
            ],
            "neutral": [
                "The weather forecast shows partly cloudy skies today.",
                "Please review the document and provide your feedback.",
                "The meeting is scheduled for three o'clock this afternoon."
            ],
            "surprised": [
                "Oh my goodness, I cannot believe this happened!",
                "What an unexpected and surprising turn of events!",
                "This is absolutely incredible and amazing!"
            ]
        }
    
    def generate_simple_speech(self, emotion: str, output_dir: str = "simple_audio"):
        """Generate speech using gTTS (less emotional but simpler)"""
        from gtts import gTTS
        import io
        from pydub import AudioSegment
        
        if emotion not in self.emotional_texts:
            raise ValueError(f"Emotion '{emotion}' not supported")
        
        Path(output_dir).mkdir(exist_ok=True)
        
        texts = self.emotional_texts[emotion]
        generated_files = []
        
        for i, text in enumerate(texts):
            try:
                # Generate speech with gTTS
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save to BytesIO buffer
                mp3_buffer = io.BytesIO()
                tts.write_to_fp(mp3_buffer)
                mp3_buffer.seek(0)
                
                # Convert MP3 to WAV using pydub
                audio = AudioSegment.from_mp3(mp3_buffer)
                
                # Apply basic emotion simulation through audio manipulation
                if emotion == "happy":
                    # Higher pitch, faster speed
                    audio = audio.speedup(playback_speed=1.1)
                    audio = audio + 2  # Slightly louder
                elif emotion == "sad":
                    # Lower pitch, slower speed
                    audio = audio.speedup(playback_speed=0.9)
                    audio = audio - 3  # Slightly quieter
                elif emotion == "angry":
                    # Louder, slightly distorted
                    audio = audio + 5
                elif emotion == "surprised":
                    # Higher pitch, variable speed
                    audio = audio.speedup(playback_speed=1.15)
                    audio = audio + 3
                
                # Export as WAV
                output_file = os.path.join(output_dir, f"{emotion}_simple_{i+1}.wav")
                audio.export(output_file, format="wav")
                generated_files.append(output_file)
                print(f"Generated: {output_file}")
                
            except Exception as e:
                print(f"Error generating {emotion} sample {i+1}: {e}")
        
        return generated_files

async def main():
    """Generate emotional speech samples"""
    print("🎤 Emotional Speech Generator")
    print("=" * 50)
    
    # Try Edge TTS first (more advanced)
    try:
        print("\n🚀 Generating high-quality emotional speech with Edge TTS...")
        generator = EmotionalSpeechGenerator()
        await generator.generate_all_emotions("sample_audio")
        print("\n✅ Edge TTS generation completed!")
        
    except Exception as e:
        print(f"❌ Edge TTS failed: {e}")
        print("\n🔄 Falling back to simple gTTS generation...")
        
        # Fallback to gTTS
        try:
            simple_generator = SimpleSpeechGenerator()
            for emotion in ["happy", "sad", "angry", "neutral", "surprised"]:
                print(f"\nGenerating {emotion} samples with gTTS...")
                simple_generator.generate_simple_speech(emotion, "simple_audio")
            print("\n✅ Simple TTS generation completed!")
            
        except Exception as e2:
            print(f"❌ Simple TTS also failed: {e2}")
            print("Please install required dependencies: pip install gTTS pydub edge-tts")

if __name__ == "__main__":
    asyncio.run(main())
