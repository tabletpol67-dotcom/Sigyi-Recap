# Si Gyi Recap Studio — Error/Performance Fix Report

မူရင်း `SiGyi_Recap_Studio_v1_FIXED.zip` ကို မထိခိုက်စေဘဲ copy တစ်ခုထဲမှာသာ အောက်ပါ defensive fixes တွေ ထည့်ထားပါတယ်။ UI layout/style ကို ပြောင်းလဲထားခြင်း မရှိပါ။

## ပြင်ဆင်ထားသော ဖိုင်များ

- `src/main.js`
- `src/lib/gemini.js`
- `src/lib/tts.js`
- `src/lib/render.js`
- `api/tts.js`
- `pnpm-lock.yaml` — `package.json` ထဲမှာရှိပေမယ့် မူရင်း lockfile ထဲ မပါသေးသော `@ffmpeg/core` နှင့် `mediabunny` dependencies ကို sync လုပ်ထားသည်။

## Error ဖြစ်နိုင်သောနေရာများ ပြင်ထားချက်

### `src/main.js`

- Browser private mode / storage ပိတ်ထားသော device များတွင် `sessionStorage` error ကြောင့် app မတက်တော့သည့်ပြဿနာကို safe wrapper ဖြင့် ကာကွယ်ထားသည်။
- Video file ကို 250 MB ထက် မကျော်စေရန် upload အစမှာ validation ထည့်ထားသည်။ Mobile memory မလောက်ခြင်းနှင့် FFmpeg WASM crash ဖြစ်နိုင်ခြေ လျှော့ချထားသည်။
- Direct video URL download တွင် 60-second timeout နှင့် `content-length`/downloaded blob size စစ်ဆေးမှု ထည့်ထားသည်။ Link request တစ်ခု hang ဖြစ်ပြီး UI အမြဲစောင့်နေခြင်းကို ကာကွယ်ထားသည်။
- Action button async error များကို global catch ဖြင့် user-friendly toast ပြနိုင်အောင် ပြင်ထားသည်။ Unhandled Promise rejection လျှော့ချထားသည်။
- Gemini key test တွင် 30-second request timeout ထည့်ထားသည်။

### `src/lib/gemini.js`

- Gemini API key ကို URL query string ထဲ ထည့်ပို့ခြင်းမပြုတော့ဘဲ `x-goog-api-key` header သုံးထားသည်။ Browser history/proxy log တွင် key ပါသွားနိုင်ခြေ လျှော့ချထားသည်။
- Abort signal အရင်ကတည်းက aborted ဖြစ်နေပါက polling sleep ချက်ချင်းရပ်စေထားသည်။
- Gemini မှ ပြန်လာသော `start/end` timestamp မမှန်ခြင်း၊ အနုတ်တန်ဖိုး၊ `Infinity/NaN`၊ duration ကျော်သွားခြင်းများကို normalize/clamp လုပ်ထားသည်။
- Malformed timestamp ကြောင့် render graph ထဲ `NaN`, `Infinity`, negative duration ဝင်ပြီး FFmpeg fail ဖြစ်နိုင်ခြေ ကာကွယ်ထားသည်။

### `src/lib/tts.js`

- TTS segment pool ထဲတွင် cancellation signal ကို worker တစ်ခုချင်းစီ စစ်ဆေးထားသည်။ User က cancel လုပ်ပြီးနောက် queued segment အသစ်များ မစတော့ပါ။
- Segment order ကို မူရင်းအတိုင်း ထိန်းထားပြီး concurrent synthesis ပြီးဆုံးမှုကြောင့် timeline လွဲသွားခြင်းကို မဖြစ်စေပါ။

### `api/tts.js`

- Python executable ကို Linux environment တွင် `python3` ရှိလျှင် အရင်သုံးပြီး မရှိမှ `python` fallback သုံးထားသည်။ Local Linux/Termux နှင့် deployment environment compatibility ပိုကောင်းစေသည်။
- Child process spawn တွင် `windowsHide` ထည့်ထားပြီး timeout/error ဖြစ်သော process များ မကျန်ရစ်စေရန် existing kill/cleanup flow နှင့် တွဲဖက်ထားသည်။

### `src/lib/render.js`

- Style/timeline value မမှန်သည့်အခါ `Number.isFinite` ဖြင့် clamp လုပ်ထားသည်။
- Narration duration သည် 0/NaN/Infinity ဖြစ်ပါက source duration သို့ fallback လုပ်ပြီး duration လုံးဝမမှန်လျှင် render မစဘဲ actionable error ပြသည်။
- Invalid duration ကြောင့် `toFixed()`၊ FFmpeg `-t`၊ filter graph timing များ fail ဖြစ်နိုင်ခြေ လျှော့ချထားသည်။

## မူရင်းအပိုင်းများ မထိထားသောအရာများ

- `src/styles.css` UI design/layout ကို မပြောင်းထားပါ။
- UI labels, workflow design, render engine choice, Burmese subtitle canvas rendering, logo controls, existing FFmpeg graph design များကို မဖျက်မပြင်ထားပါ။
- မူရင်း ZIP ကို overwrite မလုပ်ပါ။ Fixed output သည် သီးခြား ZIP ဖြစ်သည်။

## Validation

- Modified JavaScript files အားလုံးကို `node --check` ဖြင့် syntax စစ်ပြီး အောင်မြင်သည်။
- `pnpm install --no-frozen-lockfile` ဖြင့် dependency install အောင်မြင်သည်။ မူရင်း lockfile သည် `package.json` နှင့် မကိုက်သောကြောင့် fixed copy ထဲတွင် lockfile ကို sync ပြန်လုပ်ထားသည်။
- `pnpm run build` ဖြင့် Vite production build အောင်မြင်သည်။
- Build output ကို source ZIP မကြီးအောင် `dist/` နှင့် `node_modules/` မထည့်ပါ။ မူရင်း package ၏ source-only ပုံစံအတိုင်းထားထားသည်။

## သတိပြုရန်

`api/tts.js` သည် server-side Python `edge_tts` နှင့် system `ffmpeg` ကို ဆက်လက်လိုအပ်သည်။ Vercel/serverless deployment တွင် Python/FFmpeg runtime မရပါက TTS endpoint သီးခြား compatible backend သို့ ရွှေ့ရမည်။ ဒီအချက်ကို source behavior မဖျက်ဘဲ report ထဲတွင်သာ ထိန်းသိမ်းဖော်ပြထားသည်။
