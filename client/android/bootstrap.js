'use strict';
// Included only in the Android package, before shared state initialization.
window.NATIVE_MODE = true;
window.ANDROID_MODE = true;
try {
  const initial = JSON.parse(window.StepwiseAndroid.load());
  window.NATIVE_STATE = initial.state;
  window.STATE_ERROR = initial.error;
} catch (_) {
  window.NATIVE_STATE = null;
  window.STATE_ERROR = true;
}
