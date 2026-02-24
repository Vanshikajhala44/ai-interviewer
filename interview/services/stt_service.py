# from faster_whisper import WhisperModel

# model = WhisperModel("small", device="cpu")  # load once

# def speech_to_text(audio_path):
#     segments, _ = model.transcribe(
#         audio_path,
#         language="en",
#         beam_size=5,
#         vad_filter=True
#     )
#     return " ".join([s.text for s in segments])

# stt_service.py
# from faster_whisper import WhisperModel

# _model = None  # placeholder

# def get_model():
#     global _model
#     if _model is None:
#         print("Loading Whisper model...")
#         _model = WhisperModel("small", device="cpu")
#     return _model

# def speech_to_text(audio_path):
#     model = get_model()
#     segments, _ = model.transcribe(
#         audio_path,
#         language="en",
#         beam_size=5,
#         vad_filter=True
#     )
#     return " ".join([s.text for s in segments])


import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def speech_to_text(audio_file):
    audio_file.seek(0)  # make sure pointer is at start

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcript.text