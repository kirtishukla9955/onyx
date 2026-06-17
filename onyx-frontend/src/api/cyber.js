import { API_BASE, postForm, getJSON } from './client';

const BASE = API_BASE.cyber;

// POST /embed-watermark — file + signature string -> watermarked image blob
export function embedWatermark(file, signature) {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('signature', signature);
  return postForm(BASE, '/embed-watermark', fd);
}

// POST /extract-watermark — file -> { watermark } or { message }
export function extractWatermark(file) {
  const fd = new FormData();
  fd.append('file', file);
  return postForm(BASE, '/extract-watermark', fd);
}

// POST /verify-integrity — original + suspect files -> status + tampered_regions
export function verifyIntegrity(originalFile, suspectFile) {
  const fd = new FormData();
  fd.append('original', originalFile);
  fd.append('suspect', suspectFile);
  return postForm(BASE, '/verify-integrity', fd);
}

// POST /generate-recipient-copy — file + recipient id -> uniquely watermarked copy
export function generateRecipientCopy(file, recipientId) {
  const fd = new FormData();
  fd.append('file', file);
  fd.append('recipient', recipientId);
  return postForm(BASE, '/generate-recipient-copy', fd);
}

// POST /trace-leak — leaked file -> { recipient } or { message }
export function traceLeak(file) {
  const fd = new FormData();
  fd.append('file', file);
  return postForm(BASE, '/trace-leak', fd);
}

// GET /recipients — list of all recipients + payload ids
export function listRecipients() {
  return getJSON(BASE, '/recipients');
}
