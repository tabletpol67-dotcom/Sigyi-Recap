# SiGyi Recap Studio — Streamlit + Android migration

This branch preserves the existing Vite UI source, adds a Streamlit custom-component Edge TTS bridge, and adds Android build scaffolding. It is **not yet a production-ready APK** because native Android FFmpeg rendering remains unfinished and device testing is required.

## What is currently included

- Original Vite UI and existing styles retained.
- Streamlit Community Cloud entry point (`streamlit_app.py`).
- Static asset hosting config (`.streamlit/config.toml`) and `npm run build:streamlit`.
- Capacitor Android app-shell config (`capacitor.config.ts`).
- Streamlit custom-component Edge TTS bridge (`streamlit_component/frontend/` + Python `edge-tts`).
- Native-render migration notes (`ANDROID_NATIVE_FFMPEG.md`).

## Streamlit deploy from GitHub

1. In Termux, install Git and Node.js if needed:

   ```sh
   pkg update
   pkg install git nodejs-lts
   ```

2. Extract this ZIP, enter the project directory, and create a GitHub repository. Then:

   ```sh
   git init
   git add .
   git commit -m "Prepare SiGyi Recap Studio Streamlit Android scaffold"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

3. On Termux or a desktop with npm access, generate the static build and commit it:

   ```sh
   npm install
   npm run build:streamlit
   git add static package.json package-lock.json pnpm-lock.yaml
   git commit -m "Build frontend assets for Streamlit static hosting"
   git push
   ```

   If `npm install` creates `package-lock.json`, commit it. Do not commit `node_modules/`.

4. In Streamlit Community Cloud, create an app from the GitHub repository and select `streamlit_app.py` as the entrypoint.

## Important functional blockers

### Streamlit Edge TTS bridge

The hosted UI now relays Edge TTS requests through a Streamlit custom component to Python `edge-tts`; the returned MP3 is decoded in the browser and placed on the existing voiceover timeline. This needs a live Streamlit Community Cloud test for network access, Burmese voices, and Android WebView MP3 decoding. The local Vite/Node `/api/tts` endpoint remains available for ordinary browser development.

### Native FFmpeg

The current `src/lib/render.js` still imports `@ffmpeg/ffmpeg` and uses its in-memory virtual filesystem. Capacitor configuration alone does not turn this into native FFmpeg. A native Android plugin must import/copy the selected video into app cache, write the WAV and subtitle sprite inputs, execute a licensed Android FFmpeg binary/library, and return an output URI. That plugin and device-tested render adapter are not yet complete.

### API keys

The current Gemini key is held in browser `sessionStorage`. Do not put user API keys in GitHub, Streamlit shared secrets, logs, or persistent shared files. A packaged APK should use Android secure storage if key persistence is needed.

## Termux is only for source/build upload

Once a standalone APK is built and installed, the user should not need Termux to run the app. Termux may still be used by the developer to push source code to GitHub; that does not mean the published app depends on Termux.
