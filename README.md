# ONYX: Adversarial Identity Protection & Predictive Intelligence Platform

ONYX is a security platform designed to protect personal media assets (images, videos, audio) from adversarial AI scraping, facial recognition models, and unauthorized deepfake generation. It integrates **Digital Camouflage** (adversarial noise overlays), **Acoustic Poisoning** (frequency disruption), and **Watermark Embedding** (steganographic verification) coupled with a time-series forecasting engine called **TrendRadar** to predict engagement dynamics.

---

## 🏗️ Project Architecture

```
onyx-backend/
├── db/
│   └── database.py          # PostgreSQL DB session & SQLAlchemy models
├── models/
│   └── schemas.py           # Pydantic schemas (Request/Response validation)
├── routers/
│   ├── upload.py            # File upload handlers (multipart form)
│   ├── status.py            # Protection trigger & real-time SSE log stream
│   ├── results.py           # Completed asset retrieval & verification
│   └── trendradar.py        # Prophet time-series trend forecasting
├── services/
│   ├── log_service.py       # Persistence of pipeline logs & SSE logic
│   ├── trend_service.py     # Python Prophet mock-forecasting engine
│   └── pipeline_service.py  # Background worker orchestration
├── storage/
│   └── s3_client.py         # S3/MinIO upload wrapper
├── .env.example             # Config template
├── Dockerfile               # Build configuration
├── docker-compose.yml       # App + DB + MinIO local stack
├── requirements.txt         # Dependencies
└── README.md                # This manual
```

---

## ⚡ Setup & Execution

### Option A: Run with Docker Compose (Recommended)
This method spins up the FastAPI app, a PostgreSQL database, MinIO S3-compatible storage, and provisions the default bucket (`onyx-assets`) automatically.

1. **Start the containers:**
   ```bash
   docker-compose up --build
   ```
2. **Access services:**
   - **FastAPI Backend:** [http://localhost:8000](http://localhost:8000)
   - **Interactive API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **MinIO Dashboard:** [http://localhost:9001](http://localhost:9001) (User: `minioadmin` / Pass: `minioadmin`)

---

### Option B: Run Locally (Without Docker)
1. **Prerequisites:**
   - Python 3.10+
   - A running PostgreSQL database instance (with a database named `onyx` created).
   - A running MinIO instance (or AWS account) with a bucket named `onyx-assets` created and set to allow public/download access.

2. **Clone and setup virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   *Note: Installing `prophet` compiles C++ code using C++ compilers (like `gcc`, `g++`, or Visual Studio Build Tools). Ensure these are installed on your host system.*
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Copy `.env.example` to `.env` and adjust database/S3 credentials:
   ```bash
   cp .env.example .env
   ```

5. **Start Uvicorn server:**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

---

## 🔌 API Endpoints & Example Curl Commands

### 1. Health Check
Returns system status and API version.
* **Endpoint:** `GET /api/health`
* **Curl Command:**
  ```bash
  curl -X GET http://localhost:8000/api/health
  ```
* **Expected Response:**
  ```json
  {"status":"ok","version":"1.0.0"}
  ```

### 2. File Upload
Uploads a media asset (images, videos, audio) to the storage bucket and records metadata in the database.
* **Endpoint:** `POST /api/upload`
* **Content-Type:** `multipart/form-data`
* **Curl Command:**
  ```bash
  # Upload a dummy image to test
  curl -X POST http://localhost:8000/api/upload \
    -F "file=@/path/to/your/image.png" \
    -F "niche=fitness" \
    -F "platform=tiktok"
  ```
* **Expected Response:**
  ```json
  {
    "asset_id": "79c61d56-78e7-497b-83c3-d922bc968c92",
    "status": "uploaded",
    "file_url": "http://localhost:9000/onyx-assets/79c61d56-78e7-497b-83c3-d922bc968c92.png"
  }
  ```

### 3. Protection Pipeline Trigger
Queues the asset and starts the asynchronous protection steps (Digital Camouflage → Acoustic Poisoning → Watermark Embedding).
* **Endpoint:** `POST /api/protect/{asset_id}`
* **Curl Command:**
  ```bash
  curl -X POST http://localhost:8000/api/protect/79c61d56-78e7-497b-83c3-d922bc968c92
  ```
* **Expected Response:**
  ```json
  {
    "asset_id": "79c61d56-78e7-497b-83c3-d922bc968c92",
    "status": "queued",
    "message": "Protection pipeline triggered."
  }
  ```

### 4. Real-Time Log Stream (SSE)
Establishes a Server-Sent Events connection to stream raw processing logs to the console sidebar in real-time.
* **Endpoint:** `GET /api/logs/{asset_id}`
* **Curl Command:**
  ```bash
  curl -N -H "Accept: text/event-stream" http://localhost:8000/api/logs/79c61d56-78e7-497b-83c3-d922bc968c92
  ```
* **Expected Stream Output:**
  ```
  data: {"log_line": "[ONYX]: Protection pipeline triggered. Asset queued.", "emitted_at": "2026-06-16T17:55:00.123"}
  data: {"log_line": "[ML_ENGINE]: Analyzing facial embedding space...", "emitted_at": "2026-06-16T17:55:01.456"}
  data: {"log_line": "[ML_ENGINE]: Generating Adversarial Noise Mask...", "emitted_at": "2026-06-16T17:55:02.890"}
  data: {"log_line": "[ML_ENGINE]: Injecting PGD perturbation layer...", "emitted_at": "2026-06-16T17:55:03.999"}
  data: {"log_line": "[AUDIO_ENGINE]: Scanning audio frequency bands...", "emitted_at": "2026-06-16T17:55:05.111"}
  data: {"log_line": "[AUDIO_ENGINE]: Injecting ultrasonic poison layer...", "emitted_at": "2026-06-16T17:55:06.321"}
  ...
  data: {"log_line": "[ONYX]: Protection complete. Asset secured.", "emitted_at": "2026-06-16T17:55:08.450"}
  ```

### 5. TrendRadar Module
Generates time-series trend forecasts using Prophet, based on the specified social media niche and target platform. Returns 5 mock trending topics with peak times and customized strategic suggestions.
* **Endpoint:** `GET /api/trends?niche={niche}&platform={platform}`
* **Curl Command:**
  ```bash
  curl -X GET "http://localhost:8000/api/trends?niche=fitness&platform=instagram"
  ```
* **Expected Response:**
  ```json
  {
    "niche": "fitness",
    "platform": "instagram",
    "trends": [
      {
        "trend_name": "Zone 2 Cardio Secrets",
        "predicted_peak_in_hours": 14,
        "engagement_velocity_score": 88.5,
        "niche_prompt": "Record a reel explaining Zone 2 cardio benefits while jogging at sunset. Keep it under 30s."
      },
      ...
    ]
  }
  ```

### 6. Results & Verification
Returns the complete database record of the protected asset, matching the original file, protected file, generated watermark, and complete audit trail log.
* **Endpoint:** `GET /api/results/{asset_id}`
* **Curl Command:**
  ```bash
  curl -X GET http://localhost:8000/api/results/79c61d56-78e7-497b-83c3-d922bc968c92
  ```
* **Expected Response:**
  ```json
  {
    "id": "79c61d56-78e7-497b-83c3-d922bc968c92",
    "filename": "79c61d56-78e7-497b-83c3-d922bc968c92.png",
    "file_type": "image/png",
    "file_size": 1048576,
    "original_url": "http://localhost:9000/onyx-assets/79c61d56-78e7-497b-83c3-d922bc968c92.png",
    "protected_url": "http://localhost:9000/onyx-assets/protected_a1b2c3d4_79c61d56-78e7-497b-83c3-d922bc968c92.png",
    "watermark_id": "ONYX-WM-4E9A2C10",
    "status": "protected",
    "niche": "fitness",
    "platform": "tiktok",
    "created_at": "2026-06-16T17:55:00",
    "updated_at": "2026-06-16T17:55:08",
    "logs": [
      {
        "id": 1,
        "asset_id": "79c61d56-78e7-497b-83c3-d922bc968c92",
        "log_line": "[ONYX]: Protection pipeline triggered. Asset queued.",
        "emitted_at": "2026-06-16T17:55:00"
      },
      ...
    ]
  }
  ```
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

**ONYX. Protect before you post. Predict before you publish.**
