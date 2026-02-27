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


# # import whisper

# model = whisper.load_model("tiny")  # tiny is fastest

# def speech_to_text(audio_file):
#     audio_file.seek(0)

#     with open("temp_audio.webm", "wb") as f:
#         f.write(audio_file.read())

#     result = model.transcribe("temp_audio.webm")

#     return result["text"]