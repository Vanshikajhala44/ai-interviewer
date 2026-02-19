# # interview/services/tts_service.py
# import os
# import uuid
# import pyttsx3

# AUDIO_DIR = os.path.join("media", "audio")
# os.makedirs(AUDIO_DIR, exist_ok=True)

# def text_to_audio(text: str) -> str:
#     """
#     Convert text to audio and save it as WAV file.
#     Returns relative URL.
#     """

#     # Create fresh engine every time (IMPORTANT)
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 160)
#     engine.setProperty('volume', 1.0)

#     filename = f"{uuid.uuid4()}.wav"
#     file_path = os.path.join(AUDIO_DIR, filename)

#     engine.save_to_file(text, file_path)
#     engine.runAndWait()
#     engine.stop()

#     return f"/media/audio/{filename}"
# interview/services/tts_service.py

import os
import uuid
from gtts import gTTS

AUDIO_DIR = os.path.join("media", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_audio(text: str) -> str:
    """
    Convert text to audio using gTTS.
    Saves as MP3 file.
    Returns relative URL.
    """

    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)

    try:
        # Generate speech
        tts = gTTS(text=text, lang="en")
        tts.save(file_path)

        return f"/media/audio/{filename}"

    except Exception as e:
        print("TTS Error:", e)
        return None
