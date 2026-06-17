// Central place for every backend base URL.
// Change these three lines if your ports/hosts ever differ —
// nothing else in the app needs to know about it.
export const API_BASE = {
  cyber: 'http://localhost:8001',
  ml: 'http://localhost:8002',
  trend: 'http://localhost:8003',
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
