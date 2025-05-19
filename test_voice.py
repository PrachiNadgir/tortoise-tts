import torchaudio
from tortoise.api import TextToSpeech

# Initialize Tortoise
tts = TextToSpeech()

# Generate speech audio (returns a tensor)
audio = tts.tts("Hello! This is my cloned voice.", voice="alle")

# Save the audio as a WAV file
torchaudio.save("output.wav", audio.squeeze(0).cpu(), sample_rate=24000)
