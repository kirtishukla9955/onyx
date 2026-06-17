import { API_BASE, postForm } from './client';

const BASE = API_BASE.ml;

// POST /cloak-image — image file -> adversarially perturbed image blob
export function cloakImage(file, strength = 'medium') {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('strength', strength);
  return postForm(BASE, '/cloak-image', fd);
}

// POST /cloak-video — video file -> frame-by-frame perturbed video blob
export function cloakVideo(file, strength = 'medium') {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('strength', strength);
  return postForm(BASE, '/cloak-video', fd);
}

// POST /poison-audio — audio file -> ultrasonic-poisoned audio blob
export function poisonAudio(file) {
  const fd = new FormData();
  fd.append('file', file);
  return postForm(BASE, '/poison-audio', fd);
}
