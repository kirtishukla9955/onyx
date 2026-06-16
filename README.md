# ONYX
### Adversarial Identity Protection & Predictive Intelligence Platform
> Protect before you post. Predict before you publish.

---

## Overview

ONYX is a unified creator protection platform that defends digital creators against AI-powered identity theft — including deepfakes, voice clones, and unauthorized content scraping — while providing predictive trend intelligence to maximize content reach and timing.

ONYX operates on a Zero-Trust Media Processing Pipeline. Every asset uploaded is shielded at the visual layer, the audio layer, and the provenance layer before it is distributed.

---

## Core Features

- **TrendRadar** — Predictive trend intelligence engine that surfaces emerging audio tracks, hashtags, and content formats 48 hours before they peak, with niche-specific adaptation suggestions
- **Digital Camouflage** — Adversarial ML engine that injects invisible PGD-based perturbations into visual content, rendering it untrainable by deepfake and LoRA models while appearing completely normal to human viewers
- **Secret Fingerprint** — Steganographic watermarking system that embeds invisible ownership signatures into assets, verifies authenticity on demand, maps exact tamper coordinates on altered files, and traces the source of leaked drafts through per-recipient unique payloads
- **Acoustic Poisoning** — Audio adversarial engine that injects sub-audible ultrasonic noise into audio tracks, corrupting any voice-cloning model trained on the stolen content while remaining completely inaudible to human listeners

---

## Repository Structure

```
onyx/
├── onyx-cyber-backend/       — Steganographic watermarking, tamper detection, traitor tracing
├── onyx-ml-backend/          — Adversarial visual perturbation, acoustic poisoning
├── onyx-trend-engine/        — Trend forecasting, engagement velocity scoring, niche alerts
├── onyx-frontend/            — React dashboard, terminal diagnostic feed, verification UI
└── README.md
```

---

## Module Overview

### `onyx-cyber-backend`
Cybersecurity module handling steganographic watermark embedding and extraction, pixel-level tamper detection and coordinate mapping, and per-recipient traitor tracing.

**Stack:** Python, FastAPI, Pillow, OpenCV, PostgreSQL, SQLAlchemy, Uvicorn

| Method | Endpoint | Description |
|---|---|---|
| POST | `/embed-watermark` | Embeds invisible LSB ownership signature into image |
| POST | `/extract-watermark` | Extracts hidden watermark from image |
| POST | `/verify-integrity` | Compares original vs suspect file, returns tamper coordinates |
| POST | `/generate-recipient-copy` | Creates unique watermarked copy per recipient |
| POST | `/trace-leak` | Identifies which recipient copy was the source of a leak |
| GET | `/recipients` | Returns all recipients and their payload identifiers |

---

### `onyx-ml-backend`
AI/ML module handling adversarial facial perturbation using PGD optimization and sub-audible acoustic poisoning for voice clone protection.

**Stack:** Python, PyTorch, FaceNet, DeepFace, LibROSA, SciPy, OpenCV, FastAPI

| Method | Endpoint | Description |
|---|---|---|
| POST | `/cloak-image` | Applies adversarial perturbation to image |
| POST | `/cloak-video` | Applies adversarial perturbation frame by frame |
| POST | `/poison-audio` | Injects ultrasonic noise into audio track |

---

### `onyx-trend-engine`
Trend intelligence module handling social data ingestion, engagement velocity scoring, and time-series forecasting for 48-hour trend prediction.

**Stack:** Python, Prophet, FastAPI, BeautifulSoup, PostgreSQL

| Method | Endpoint | Description |
|---|---|---|
| GET | `/trending` | Returns current top predicted trends |
| GET | `/trending/{niche}` | Returns niche-specific trend predictions |
| GET | `/trend-expiry` | Returns trends predicted to decline within 24 hours |

---

### `onyx-frontend`
React-based dashboard with real-time terminal diagnostic feed, asset upload pipeline, trend radar panel, and verification result display.

**Stack:** React.js, TailwindCSS, Axios

---

## Full Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, TailwindCSS |
| Backend API | Python FastAPI |
| Adversarial ML | PyTorch, PGD Optimization, FaceNet, DeepFace |
| Audio Processing | LibROSA, SciPy |
| Steganography | Custom LSB Module, Pillow |
| Trend Forecasting | Python Prophet |
| Image Processing | OpenCV |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| File Storage | AWS S3 / MinIO |
| Server | Uvicorn |
| Deployment | Docker, Railway |

---

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Docker (optional)

---

### Cybersecurity Backend

```bash
cd onyx-cyber-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/onyx_db
```

```bash
uvicorn main:app --reload --port 8001
```

---

### ML Backend

```bash
cd onyx-ml-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

---

### Trend Engine

```bash
cd onyx-trend-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

---

### Frontend

```bash
cd onyx-frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`

---

### Database

```bash
psql -U postgres
CREATE DATABASE onyx_db;
\q
```

All tables auto-create on first server startup.

---

## API Documentation

| Module | URL |
|---|---|
| Cybersecurity Backend | `http://localhost:8001/docs` |
| ML Backend | `http://localhost:8002/docs` |
| Trend Engine | `http://localhost:8003/docs` |

---

## Docker

```bash
docker-compose up --build
```

Spins up all backends, frontend, and PostgreSQL together.

---

## License

MIT License — see `LICENSE` for details.

---

**ONYX. Protect before you post. Predict before you publish.**
