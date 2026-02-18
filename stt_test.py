from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu")

audio_file = r"C:\Users\vansh\OneDrive\Desktop\AI interviewer\audiooo.wav"

segments, info = model.transcribe(
    audio_file,
    language="en",   # Force English
    beam_size=5,
    vad_filter=True
)

print("\nTranscription:\n")

for segment in segments:
    print(segment.text)
