# Android Native FFmpeg integration

This repository includes Capacitor configuration, but is not yet a signed APK. After installing dependencies, generate the Android shell:

```bash
npm install
npx cap add android
npx cap sync android
npx cap open android
```

## Native FFmpeg dependency

In `android/app/build.gradle`, add Maven Central and a maintained FFmpegKit dependency. Check the current version and license at https://github.com/ffmpegkit-maintained/ffmpeg. Example:

```gradle
dependencies { implementation 'dev.ffmpegkit-maintained:ffmpeg:8.1.9' }
```

A Capacitor native plugin is still required to pass real file paths and FFmpeg arguments to Android. Do not pass large video files as base64 through the JS bridge. Use Android content URIs/app cache files and return the output URI. Current `src/lib/render.js` is browser-WASM-specific and has not yet been ported to the native plugin.

Licensing: the `ffmpeg` artifact is LGPL by default; GPL variants have different obligations. Review the selected artifact's exact codec list and license before release.
