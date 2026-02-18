from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu")  # load once

def speech_to_text(audio_path):
    segments, _ = model.transcribe(
        audio_path,
        language="en",
        beam_size=5,
        vad_filter=True
    )
    return " ".join([s.text for s in segments])

