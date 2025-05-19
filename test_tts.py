from tortoise.api import TextToSpeech
import torchaudio

tts = TextToSpeech()

# Generate 3D audio tensor: [1, channels, samples]
audio = tts.tts("This is a test of Tortoise TTS.", voice="alle")

# Convert [1, channels, samples] → [channels, samples]
audio = audio.squeeze(0)

# Save to output.wav
torchaudio.save("output.wav", audio.cpu(), sample_rate=24000)
