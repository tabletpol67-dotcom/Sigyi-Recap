# Streamlit Edge TTS bridge

The Streamlit host embeds the built Vite UI in a custom component. The component relays only `sigyi-tts-request` messages to Python and returns MP3 bytes as a correlated response. `src/lib/tts.js` decodes those bytes with `OfflineAudioContext` and creates the WAV timeline in the browser, preserving the existing client-side audio timeline code.

- Python dependency: `edge-tts` in `requirements.txt`.
- Voices: `my-MM-NilarNeural`, `my-MM-ThihaNeural`.
- Request limit: 4,500 characters per segment; component timeout is 120 seconds.
- The bridge returns errors to the UI and avoids placing Gemini API keys in Streamlit state.
- Validate in the deployed Streamlit Community Cloud app. This environment cannot validate Edge TTS network access or Android WebView decoding end-to-end.
