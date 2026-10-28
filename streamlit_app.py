"""Streamlit Community Cloud host for SiGyi Recap Studio.

The Vite UI is served as a static asset inside a Streamlit custom component.
A small, request/response bridge routes Edge TTS calls to Python because Streamlit
Community Cloud does not expose arbitrary Flask/FastAPI routes from an app.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import tempfile
import subprocess
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
UI = ROOT / "static" / "index.html"
COMPONENT = components.declare_component(
    "sigyi_recap_host",
    path=str(ROOT / "streamlit_component" / "frontend"),
)

st.set_page_config(page_title="Si Gyi Recap Studio", page_icon="🎬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(
    """<style>
    [data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"],footer,#MainMenu{display:none!important}
    .block-container{padding:0!important;max-width:100%!important}
    iframe{border:0!important}
    </style>""",
    unsafe_allow_html=True,
)

if not UI.exists():
    st.error("Frontend build မတွေ့ပါ။ GitHub Actions build သို့မဟုတ် `npm run build:streamlit` ကို အရင် run လုပ်ပါ။")
    st.code("npm install && npm run build:streamlit")
    st.stop()


def edge_tts_mp3(text: str, voice: str, rate: float) -> bytes:
    """Generate Edge TTS MP3 and convert it to browser-friendly WAV."""
    import edge_tts

    voice_map = {
        "Nilar Neural": "my-MM-NilarNeural",
        "Thiha Neural": "my-MM-ThihaNeural",
    }
    selected_voice = voice_map.get(voice, "my-MM-NilarNeural")
    percent = round((float(rate) - 1.0) * 100)
    rate_string = f"{percent:+d}%"

    async def synthesize() -> bytes:
        with tempfile.TemporaryDirectory() as folder:
            mp3_path = Path(folder) / "voice.mp3"
            wav_path = Path(folder) / "voice.wav"

            communicate = edge_tts.Communicate(
                text=text, voice=selected_voice, rate=rate_string
            )
            await communicate.save(str(mp3_path))

            if not mp3_path.exists() or mp3_path.stat().st_size < 1000:
                raise RuntimeError("Edge TTS က MP3 အသံဒေတာ မပြန်ပေးပါ။")

            result = subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(mp3_path),
                    "-ac", "1", "-ar", "24000",
                    "-c:a", "pcm_s16le", str(wav_path),
                ],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    "MP3 မှ WAV ပြောင်းမရပါ: " + (result.stderr[-800:] or "FFmpeg error")
                )

            data = wav_path.read_bytes()
            if len(data) < 1000 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
                raise RuntimeError("WAV အသံဖိုင် မမှန်ပါ။")
            return data

    return asyncio.run(synthesize())


if "sigyi_tts_last_request" not in st.session_state:
    st.session_state.sigyi_tts_last_request = None
if "sigyi_tts_response" not in st.session_state:
    st.session_state.sigyi_tts_response = None

request = COMPONENT(tts_response=st.session_state.sigyi_tts_response, key="sigyi_recap_component", default=None)
if isinstance(request, dict) and request.get("kind") == "tts":
    request_id = str(request.get("requestId", ""))
    if request_id and request_id != st.session_state.sigyi_tts_last_request:
        st.session_state.sigyi_tts_last_request = request_id
        try:
            text_value = str(request.get("text", "")).strip()
            if not text_value:
                raise ValueError("TTS စာသား မရှိပါ။")
            if len(text_value) > 4500:
                raise ValueError("TTS စာပိုဒ်တစ်ခုမှာ စာလုံး ၄၅၀၀ ထက် မကျော်စေပါနှင့်။")
            audio = edge_tts_mp3(text_value, str(request.get("voice", "Nilar Neural")), float(request.get("rate", 1.25)))
            st.session_state.sigyi_tts_response = {
                "requestId": request_id,
                "ok": True,
                "mimeType": "audio/wav",
                "audioBase64": base64.b64encode(audio).decode("ascii"),
            }
        except Exception as exc:  # return the failure to the UI instead of crashing the app
            st.session_state.sigyi_tts_response = {
                "requestId": request_id,
                "ok": False,
                "error": f"Edge TTS error: {type(exc).__name__}: {exc}",
            }
        st.rerun()
