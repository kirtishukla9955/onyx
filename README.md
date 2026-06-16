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
