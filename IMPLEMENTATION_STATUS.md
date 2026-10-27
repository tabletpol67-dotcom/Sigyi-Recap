# Si Gyi Recap Studio — Neon Workflow Update

## Included in this source update

- Neon multi-colour studio theme with higher-contrast, larger touch controls.
- Renamed workflow steps to Upload video → Style & Script → Render MP4.
- Added a route from upload to the full style editor before Gemini analysis.
- The style editor now offers “Confirm Style → Generate Script + Voice” when no script exists; once the script and voice are ready, the action becomes Render MP4.
- Added a real Gemini API connectivity test using a small `generateContent` request. It reports invalid/unauthorized key, quota/rate limit, model, network, and success states separately.
- Added direct touch/mouse dragging for the Burmese caption overlay and original-subtitle blur area's vertical position; corresponding sliders stay synchronized.
- Updated Gemini fallback model order to prefer current stable Flash model IDs.

## Important current limitations (do not mistake this package for a finished APK)

- This remains the existing Vite browser app. It is **not yet a compiled Android APK**, and the render path is still browser-side FFmpeg.wasm / experimental WebCodecs. Native Android FFmpeg needs a separate Android wrapper/plugin and must be benchmarked on real devices.
- The existing TTS endpoint is `api/tts.js`, a Node serverless handler that spawns Python `edge_tts` and an `ffmpeg` executable. That deployment assumption must be validated/reworked before using Streamlit Community Cloud; Streamlit is a Python app host, not a drop-in Vercel/Node serverless host.
- Gemini API calls are browser-direct. The key is stored in `sessionStorage` (cleared when the browser session ends) and is not sent to this project's server by the Gemini code. The external Google API receives the key as an HTTP header for the new key test; existing analysis calls are still in the current Gemini module and should be migrated to headers in a security hardening pass.
- Edge TTS is an online service, not a guaranteed unlimited production API. TTS availability, host limits, and Gemini quota can change.
- Dragging adjusts vertical position only. Resize handles for blur rectangles and free X/Y positioning are not implemented yet.

## Validation performed

- JavaScript syntax checks with `node --check` passed for `src/main.js` and `src/lib/gemini.js`.
- Full Vite production build could not be run in this environment because dependency installation timed out. Run `npm install` and `npm run build` on a machine with package-registry access before deployment.

## Recommended next engineering phase

1. Finish direct Gemini request hardening (use `x-goog-api-key` headers consistently, add an explicit model/permission probe, and ensure no key is logged).
2. Decide and implement the hosting split: static Vite front end + a compatible TTS backend, or a real Streamlit Python backend with an API contract.
3. Add a Capacitor Android project and select a maintained native FFmpeg integration with a verified license/build setup.
4. Benchmark native software encoding vs Android MediaCodec hardware encoding on low-end and mid-range phones; expose Auto / Low / Balanced / High profiles based on tested limits.
5. Add drag handles for blur rectangle size and full X/Y placement, then compare preview coordinates with exported output.
6. Build/sign the APK and test upload, API-key probe, Edge TTS, cancel/retry, long renders, screen-off behavior, and output saving on actual Android devices.

## Follow-up preparation (2026-10-27)
- Added GitHub Actions frontend build check, `.gitignore`, and Termux-to-GitHub deployment guide.
- The native FFmpeg Android bridge and Streamlit-compatible TTS request bridge remain unfinished; do not treat this scaffold as a working APK or claim that Streamlit deployment alone enables `/api/tts`.
