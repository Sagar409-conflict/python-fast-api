import numpy as np
import soundfile as sf
from scipy import signal
import os

def generate_sample_audio(filename="sample_audio.wav", duration=3, sample_rate=16000):
    """
    Generate a simple sample audio file for testing purposes.
    This creates a combination of tones that might simulate speech patterns.
    """
    
    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a combination of frequencies to simulate speech-like patterns
    # Lower frequencies for vowel-like sounds
    f1 = 250  # Fundamental frequency
    f2 = 800  # First formant
    f3 = 1200 # Second formant
    
    # Generate base signal with harmonics
    signal_wave = (
        0.3 * np.sin(2 * np.pi * f1 * t) +      # Fundamental
        0.2 * np.sin(2 * np.pi * f2 * t) +      # First formant
        0.1 * np.sin(2 * np.pi * f3 * t) +      # Second formant
        0.05 * np.sin(2 * np.pi * f1 * 2 * t)   # Harmonic
    )
    
    # Add some amplitude modulation to simulate speech rhythm
    envelope = 0.5 * (1 + np.sin(2 * np.pi * 2 * t))  # 2 Hz modulation
    signal_wave = signal_wave * envelope
    
    # Add a bit of noise to make it more realistic
    noise = 0.02 * np.random.normal(0, 1, len(signal_wave))
    signal_wave = signal_wave + noise
    
    # Apply a simple envelope to avoid clicks
    fade_samples = int(0.1 * sample_rate)  # 100ms fade
    signal_wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
    signal_wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Normalize
    signal_wave = signal_wave / np.max(np.abs(signal_wave)) * 0.8
    
    # Save as WAV file
    sf.write(filename, signal_wave, sample_rate)
    print(f"Sample audio file generated: {filename}")
    print(f"Duration: {duration}s, Sample rate: {sample_rate}Hz")
    return filename

def generate_multiple_samples():
    """Generate multiple sample files for testing different scenarios"""
    
    # Create samples directory
    os.makedirs("sample_audio", exist_ok=True)
    
    # Generate different samples
    samples = [
        ("sample_audio/happy_tone.wav", 2, {"f1": 300, "f2": 900, "modulation": 4}),
        ("sample_audio/sad_tone.wav", 3, {"f1": 200, "f2": 600, "modulation": 1}),
        ("sample_audio/neutral_tone.wav", 2.5, {"f1": 250, "f2": 800, "modulation": 2}),
    ]
    
    for filename, duration, params in samples:
        # Generate with different parameters to simulate different emotions
        t = np.linspace(0, duration, int(16000 * duration), False)
        
        f1 = params["f1"]
        f2 = params["f2"]
        mod_freq = params["modulation"]
        
        signal_wave = (
            0.3 * np.sin(2 * np.pi * f1 * t) +
            0.2 * np.sin(2 * np.pi * f2 * t) +
            0.1 * np.sin(2 * np.pi * f1 * 1.5 * t)
        )
        
        envelope = 0.5 * (1 + np.sin(2 * np.pi * mod_freq * t))
        signal_wave = signal_wave * envelope
        
        noise = 0.02 * np.random.normal(0, 1, len(signal_wave))
        signal_wave = signal_wave + noise
        
        # Apply fade
        fade_samples = int(0.1 * 16000)
        signal_wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
        signal_wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        # Normalize
        signal_wave = signal_wave / np.max(np.abs(signal_wave)) * 0.8
        
        sf.write(filename, signal_wave, 16000)
        print(f"Generated: {filename}")

if __name__ == "__main__":
    # Generate a simple sample
    generate_sample_audio()
    
    # Generate multiple samples
    print("\nGenerating multiple sample files...")
    generate_multiple_samples()
    
    print("\nSample files generated! You can now test the speech emotion recognition API.")
    print("Try uploading these files to the /analyze-speech-emotion-public endpoint.")
