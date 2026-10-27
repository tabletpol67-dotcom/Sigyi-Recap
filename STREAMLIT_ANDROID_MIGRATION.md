# SiGyi Recap Studio — Streamlit + Android migration

## Included
- Existing Vite UI source/CSS retained unchanged.
- Streamlit Community Cloud entrypoint (`streamlit_app.py`).
- Static-serving configuration and build/copy script.
- Capacitor configuration for an Android app shell.
- Streamlit custom-component Edge TTS request/response bridge.
- Native FFmpeg dependency notes and explicit remaining integration work.

## Streamlit deployment
1. Push this repository to GitHub.
2. On a machine with npm access, run `npm install`.
3. Run `npm run build:streamlit` and commit the generated `static/` folder.
4. Create a Streamlit Community Cloud app pointing to `streamlit_app.py`.

Streamlit static files are served from `/app/static/`. This serves the built Vite UI while retaining its source design.

## Streamlit Edge TTS bridge
A custom-component bridge now relays browser TTS requests to Python `edge-tts` and returns MP3 bytes to the existing browser audio timeline. Validate the deployed app because this workspace cannot verify Streamlit Cloud network access or Android WebView decoding end-to-end.

Do not put users' Gemini keys into shared Streamlit globals, app secrets, logs, or persistent files. Existing Gemini analysis remains browser-direct; keys are held in sessionStorage in the web version. If packaged as an APK, use Android secure storage for saved keys.

## Native rendering status
Capacitor config is present, but native FFmpeg is not wired into the current render graph. `src/lib/render.js` depends on FFmpeg.wasm's virtual FS, browser Canvas subtitle PNG generation, and `ffmpeg.exec()`. A native adapter must replace input/output file handling and execute the filter graph against app-local paths. Until this is implemented and tested on an Android device, treat this as a migration scaffold, not a completed APK.
