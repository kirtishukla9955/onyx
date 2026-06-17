// Central place for every backend base URL.
// We use VITE_API_URL for production (Render) and default to localhost:8000 for local dev
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_BASE = {
  cyber: BASE_URL,
  ml: BASE_URL,
  trend: BASE_URL,
};

// Generic POST helper for multipart/form-data (file uploads).
export async function postForm(baseUrl, path, formData) {
  const res = await fetch(`${baseUrl}${path}`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const errBody = await res.json();
      detail = errBody.detail || errBody.message || detail;
    } catch (_) {
      /* response wasn't JSON — keep generic message */
    }
    throw new Error(detail);
  }

  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return res.json();
  }
  // file response (e.g. a returned watermarked image) — hand back a blob
  return res.blob();
}

// Generic GET helper for JSON endpoints.
export async function getJSON(baseUrl, path) {
  const res = await fetch(`${baseUrl}${path}`);
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return res.json();
}
