# ONYX — Frontend

A full creator-protection web app: a marketing landing page, working sign up /
sign in, and a dashboard with four real feature pages wired to your backend.

---

## Tech Stack

- React 18 + Vite
- React Router v6 (routing, protected routes)
- TailwindCSS (custom design tokens — see `tailwind.config.js`)
- Framer Motion (scroll reveals, page-load animation)
- Lucide React (icons)
- HTML5 Canvas (the animated face-scramble hero visual)

---

## Setup

```bash
npm install
npm run dev
```

Runs at `http://localhost:5173`

```bash
npm run build      # production build
npm run preview    # preview the production build
```

---

## What's Built

### Public site (`/`)
The original marketing landing page — hero, four-pillar feature breakdown,
pipeline diagram, before/after proof section, pricing, closing CTA. Every CTA
button now routes to `/signup`.

### Auth (`/signup`, `/login`)
Full working signup and login forms with validation, loading states, and
error handling — currently backed by a **mock auth layer** (see below) since
no auth backend exists yet. On success, the user is redirected straight into
`/dashboard`.

### Dashboard (`/dashboard/*`)
Protected routes — visiting any dashboard URL while signed out redirects to
`/login`. Left sidebar has: profile (avatar + name/email), the four feature
pages, and Settings + Log out pinned at the bottom. Collapses to icon-only on
narrow screens.

| Route | Page | What it does |
|---|---|---|
| `/dashboard` | Overview | Stat cards, quick links to all 4 features, live terminal feed |
| `/dashboard/camouflage` | Digital Camouflage | Upload image/video, calls ML backend to cloak it, download result |
| `/dashboard/fingerprint` | Secret Fingerprint | 3 tabs: embed watermark, verify integrity (tamper detection), traitor trace (generate recipient copy + trace a leak) |
| `/dashboard/acoustic` | Acoustic Poisoning | Upload audio, calls ML backend to poison it, preview + download |
| `/dashboard/trendradar` | TrendRadar | Pick a niche, fetches trending + expiring trends from your trend engine |
| `/dashboard/settings` | Settings | Edit profile, see connected backend URLs, log out |

Every button on these pages makes a **real network call** to your backend.
Nothing is faked or simulated. If your backend isn't running, you'll see a
clear error banner telling you which port it expected to reach.

---

## Connecting Your Real Backend

### Auth
There is no auth backend yet, so `src/context/AuthContext.jsx` currently
fakes signup/login by storing a session in `localStorage`. The file has a
comment block showing exactly what to replace once your auth endpoints
exist. It's a single function body swap; nothing else in the app needs to
change since every page reads the user only through `useAuth()`.

### The three feature backends
Already wired for real. Base URLs live in one place:

```js
// src/api/client.js
export const API_BASE = {
  cyber: 'http://localhost:8001',
  ml: 'http://localhost:8002',
  trend: 'http://localhost:8003',
};
```

Change these three lines if your ports or hosts differ. Nothing else needs
to be touched.

The actual endpoint calls live in `src/api/cyber.js`, `src/api/ml.js`, and
`src/api/trend.js`, matching the routes from your backend spec:

**Cybersecurity backend (8001)**
- `POST /embed-watermark` — file + signature, returns watermarked file
- `POST /extract-watermark` — file, returns watermark text
- `POST /verify-integrity` — original + suspect, returns status + tampered regions
- `POST /generate-recipient-copy` — file + recipient, returns unique watermarked copy
- `POST /trace-leak` — leaked file, returns recipient match
- `GET /recipients` — list of recipients

**ML backend (8002)**
- `POST /cloak-image` — image, returns adversarially perturbed image
- `POST /cloak-video` — video, returns perturbed video
- `POST /poison-audio` — audio, returns ultrasonic-poisoned audio

**Trend engine (8003)**
- `GET /trending` — current top trends
- `GET /trending/{niche}` — niche-specific trends
- `GET /trend-expiry` — trends about to decline

If any of your real endpoints expect different field names than what's sent
(e.g. `signature` vs `owner_id`), open the matching function in `src/api/`
and adjust the `FormData.append(...)` calls. That's the only place it's
hardcoded.

### CORS
Since the frontend runs on `localhost:5173` and your backends run on
`8001`/`8002`/`8003`, you'll need CORS enabled on each FastAPI app, e.g.:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Without this, the browser will block the requests even though the backend
is running.

---

## Project Structure

```
onyx-frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── public/
│   └── onyx-mark.svg
└── src/
    ├── main.jsx
    ├── App.jsx                  — router setup, all routes
    ├── index.css
    ├── api/
    │   ├── client.js            — base URLs + fetch helpers
    │   ├── cyber.js             — cybersecurity backend calls
    │   ├── ml.js                — ML backend calls
    │   └── trend.js             — trend engine calls
    ├── context/
    │   └── AuthContext.jsx      — auth state (mock — see comments)
    ├── lib/
    │   └── ProtectedRoute.jsx   — redirects to /login if signed out
    ├── pages/
    │   ├── Landing.jsx          — assembles the marketing page
    │   ├── AuthLayout.jsx       — shared split-screen layout for auth
    │   ├── Signup.jsx
    │   └── Login.jsx
    ├── dashboard/
    │   ├── DashboardLayout.jsx  — sidebar + topbar shell
    │   ├── Sidebar.jsx
    │   ├── Overview.jsx
    │   ├── Camouflage.jsx
    │   ├── FingerprintPage.jsx
    │   ├── Acoustic.jsx
    │   ├── TrendRadar.jsx
    │   └── Settings.jsx
    └── components/
        ├── Navbar.jsx
        ├── Hero.jsx
        ├── FaceScrambleCanvas.jsx
        ├── TerminalFeed.jsx
        ├── TrustStrip.jsx
        ├── Features.jsx
        ├── Pipeline.jsx
        ├── Proof.jsx
        ├── Pricing.jsx
        ├── CTABanner.jsx
        ├── Footer.jsx
        ├── FormField.jsx        — TextField, PasswordField
        ├── Dropzone.jsx         — drag-and-drop file upload
        └── DashboardUI.jsx      — Panel, StatusBanner, buttons
```

---

## Design Tokens

| Token | Value | Use |
|---|---|---|
| `void` | `#050608` | Page background |
| `void-panel` | `#0A0C10` | Card backgrounds |
| `cyan-glow` | `#00F0FF` | Primary accent — shields, CTAs |
| `violet-glow` | `#7B5CFF` | Secondary accent — prediction, provenance |
| `alert-red` | `#FF3B5C` | Tamper / failure states |

Fonts: **Chakra Petch** (display/headlines), **Inter** (body), **JetBrains Mono** (terminal, data labels, eyebrow labels).
