import { API_BASE, getJSON } from './client';

const BASE = API_BASE.trend;

// GET /trending — current top predicted trends
export function getTrending() {
  return getJSON(BASE, '/trending');
}

// GET /trending/{niche} — niche-specific predictions
export function getTrendingByNiche(niche) {
  return getJSON(BASE, `/trending/${encodeURIComponent(niche)}`);
}

// GET /trend-expiry — trends predicted to decline soon
export function getTrendExpiry() {
  return getJSON(BASE, '/trend-expiry');
}
