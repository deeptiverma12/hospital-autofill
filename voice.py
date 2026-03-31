import sounddevice as sd
import scipy.io.wavfile as wav
import whisper
import tempfile
import os

model = whisper.load_model("base")

def record_audio(duration=10, sample_rate=16000):
    print("Recording...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    print("Done recording.")
    return audio, sample_rate

def transcribe_audio():
    audio, sample_rate = record_audio()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
      temp_path = f.name

    wav.write(temp_path, sample_rate, audio)
    result = model.transcribe(temp_path)
    os.unlink(temp_path)
    return result["text"]