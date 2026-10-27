# Hosting migration note: Streamlit

The current project is a Vite JavaScript application with a Node-style `/api/tts` endpoint. It cannot simply be uploaded to Streamlit Community Cloud and expected to run unchanged.

Two supported architecture directions are possible:

## Option A — Keep the Vite UI (recommended for this product)
- Host the built static UI on a static host.
- Run a compatible TTS API separately.
- Keep Gemini calls client-side if users bring their own keys.
- Later wrap the same UI with Capacitor and add a native Android render bridge.

## Option B — Use Streamlit as the Python service
- Create a Streamlit Python app with explicit API operations for TTS/job coordination.
- Add a compatible HTTP interface if the Android app will call it directly; Streamlit UI interactions alone are not a general-purpose REST API.
- Do not assume `ffmpeg` or other system binaries are available unless the deployment image explicitly installs them.
- Never store one user's Gemini key in shared Streamlit session/global state in a way another user could read. Avoid logging keys and use HTTPS.

For the stated goal (large touch-friendly editing UI and native local rendering), a static Vite/Capacitor front end plus a small Python/HTTP service is usually the cleaner separation than rebuilding the editing interface in Streamlit.
