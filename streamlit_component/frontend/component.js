(() => {
  const iframe = document.getElementById('sigyi-app');
  let latestResponseId = null;
  let args = {};

  function send(type, payload) {
    iframe.contentWindow?.postMessage({ type, payload }, '*');
  }
  function postToStreamlit(message) { window.parent.postMessage(message, '*'); }
  function ready() {
    postToStreamlit({ isStreamlitMessage: true, type: 'streamlit:componentReady', apiVersion: 1 });
    postToStreamlit({ isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: 980 });
  }

  window.addEventListener('message', (event) => {
    const data = event.data || {};
    if (data.type === 'streamlit:render') {
      args = data.args || {};
      const response = args.tts_response;
      if (response && response.requestId && response.requestId !== latestResponseId) {
        latestResponseId = response.requestId;
        send('sigyi-tts-response', response);
      }
    }
    // The app iframe is a child of this component. Relay only the known TTS
    // request shape to Python; no secrets or other messages are forwarded.
    if (data.type === 'sigyi-tts-request' && data.payload && data.payload.requestId) {
      postToStreamlit({
        isStreamlitMessage: true,
        type: 'streamlit:setComponentValue',
        dataType: 'json',
        value: { kind: 'tts', ...data.payload }
      });
    }
  });

  iframe.addEventListener('load', () => {
    if (args.tts_response) send('sigyi-tts-response', args.tts_response);
  });
  ready();
})();
