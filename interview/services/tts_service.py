import io
from gtts import gTTS
from django.http import HttpResponse

import io
from gtts import gTTS

def text_to_audio_bytes(text: str) -> bytes:
    buf = io.BytesIO()
    tts = gTTS(text=text, lang="en")
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()
