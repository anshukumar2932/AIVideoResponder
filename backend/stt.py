print("Script started...")
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import time

# -------------------------------
# Load Whisper Model (CPU)
# -------------------------------
print("Loading Whisper model...")
model = whisper.load_model("base")  # Good balance of speed & accuracy
print("Model loaded successfully.\n")

# -------------------------------
# Record Audio from Microphone
# -------------------------------

def record_audio(filename="input.wav", sample_rate=16000,
                 silence_threshold=400, silence_duration=3.5):
    
    print("Recording... Speak now.")
    
    recording = []
    silence_counter = 0
    chunk_duration = 0.1  # 100ms chunks
    chunk_size = int(sample_rate * chunk_duration)
    
    with sd.InputStream(samplerate=sample_rate,
                        channels=1,
                        dtype='int16') as stream:
        
        while True:
            audio_chunk, _ = stream.read(chunk_size)
            recording.append(audio_chunk)
            
            # Calculate RMS (energy)
            rms = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))
            
            if rms < silence_threshold:
                silence_counter += chunk_duration
            else:
                silence_counter = 0
            
            # Stop if silence longer than threshold
            if silence_counter >= silence_duration:
                print("Silence detected. Stopping recording.")
                break
    
    audio_data = np.concatenate(recording, axis=0)
    write(filename, sample_rate, audio_data)
    print("Recording complete.\n")
# -------------------------------
# Convert Speech to Text
# -------------------------------
def speech_to_text(filename="input.wav"):
    if not os.path.exists(filename):
        print("Audio file not found.")
        return ""
    
    print("Transcribing...")
    start_time = time.time()
    
    result = model.transcribe(filename, language="en")
    
    end_time = time.time()
    print(f"Transcription complete. Time taken: {round(end_time - start_time, 2)} seconds\n")
    
    return result["text"].strip()

# -------------------------------
# Main Execution
# -------------------------------

from tts import generate_audio

if __name__ == "__main__":
    record_audio()
    text = speech_to_text()
    
    print("You said:", text)
    speak(text)
