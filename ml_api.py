"""
ONYX — ML API Server
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

FastAPI server exposing the ML Engine over HTTP.
Handles file uploads, returns protected files, and streams processing logs.

Run:
    uvicorn ml_api:app --host 0.0.0.0 --port 8000 --reload
"""

import asyncio
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from onyx_ml_engine import ONYXMLEngine

# ── App Setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ONYX ML Engine API",
    description="Adversarial Identity Protection — Digital Camouflage & Acoustic Poisoning",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Singleton ML Engine ────────────────────────────────────────────────────────
engine = ONYXMLEngine()

# ── Temp directory for uploads and results ─────────────────────────────────────
UPLOAD_DIR = Path(tempfile.gettempdir()) / "onyx_uploads"
OUTPUT_DIR = Path(tempfile.gettempdir()) / "onyx_outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _save_upload(upload: UploadFile) -> Path:
    """Save an uploaded file to UPLOAD_DIR with a unique name."""
    suffix = Path(upload.filename or "file").suffix or ".bin"
    dest   = UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
    with dest.open("wb") as f:
        shutil.copyfileobj(upload.file, f)
    return dest


def _output_path(upload_path: Path) -> Path:
    """Derive an output path inside OUTPUT_DIR."""
    return OUTPUT_DIR / f"{upload_path.stem}_protected{upload_path.suffix}"


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "ONYX ML Engine online", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────────────────────────────────────
@app.post("/process", tags=["Protection"])
async def process_file(
    file:       UploadFile = File(...),
    frame_skip: int        = Query(default=1, ge=1, description="Video: process every Nth frame"),
    max_frames: Optional[int] = Query(default=None, ge=1, description="Video: cap frame count"),
):
    """
    **Upload any image, video, or audio file.**

    The ML Engine routes the file to the correct protection pipeline:
    - **Image** → Digital Camouflage (PGD adversarial perturbation)
    - **Video** → Digital Camouflage applied per-frame
    - **Audio** → Acoustic Poisoning (ultrasonic frequency injection)

    Returns the protected file as a downloadable response.
    """
    upload_path = _save_upload(file)
    out_path    = _output_path(upload_path)

    kwargs: dict = {"output_path": str(out_path)}
    if frame_skip > 1:
        kwargs["frame_skip"] = frame_skip
    if max_frames:
        kwargs["max_frames"] = max_frames

    result = engine.process_file(str(upload_path), **kwargs)

    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("error", "Processing failed"))

    return FileResponse(
        path=result["output_path"],
        filename=f"onyx_protected_{file.filename}",
        media_type="application/octet-stream",
    )


# ─────────────────────────────────────────────────────────────────────────────
@app.post("/process/info", tags=["Protection"])
async def process_file_info(
    file:       UploadFile = File(...),
    frame_skip: int        = Query(default=1, ge=1),
    max_frames: Optional[int] = Query(default=None, ge=1),
):
    """
    Same as `/process` but returns a **JSON status report** instead of the
    protected file binary. Useful for the dashboard to display processing metadata.
    """
    upload_path = _save_upload(file)
    out_path    = _output_path(upload_path)

    kwargs: dict = {"output_path": str(out_path)}
    if frame_skip > 1:
        kwargs["frame_skip"] = frame_skip
    if max_frames:
        kwargs["max_frames"] = max_frames

    result = engine.process_file(str(upload_path), **kwargs)

    if not result.get("success"):
        raise HTTPException(status_code=422, detail=result.get("error", "Processing failed"))

    return JSONResponse(content=result)


# ─────────────────────────────────────────────────────────────────────────────
@app.get("/logs", tags=["Monitoring"])
async def get_processing_logs(last_n: Optional[int] = Query(default=50, ge=1)):
    """
    Return the most recent **last_n** ML Engine log lines.

    These are the same messages shown in the ONYX dashboard terminal sidebar.
    """
    logs = engine.get_logs(last_n=last_n)
    return JSONResponse(content={"logs": logs, "count": len(logs)})


# ─────────────────────────────────────────────────────────────────────────────
@app.get("/logs/stream", tags=["Monitoring"])
async def stream_logs(poll_interval: float = Query(default=0.5, ge=0.1)):
    """
    **Server-Sent Events** stream of real-time log lines.

    Connect from the frontend with:
    ```javascript
    const es = new EventSource('/logs/stream');
    es.onmessage = e => console.log(e.data);
    ```
    """
    sent_count = [0]  # mutable counter in closure

    async def _event_generator():
        while True:
            logs = engine.get_logs()
            new_lines = logs[sent_count[0]:]
            for line in new_lines:
                yield f"data: {line}\n\n"
            sent_count[0] += len(new_lines)
            await asyncio.sleep(poll_interval)

    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ─────────────────────────────────────────────────────────────────────────────
@app.post("/verify/cloak", tags=["Verification"])
async def verify_cloak(file: UploadFile = File(...)):
    """
    Upload a cloaked image and verify that the digital camouflage is effective
    (i.e., face detection fails on the cloaked file).

    Returns: `{ faces_detected, cloak_effective }`.
    """
    upload_path = _save_upload(file)
    result = engine.digital_camouflage.verify_cloak(str(upload_path))
    return JSONResponse(content=result)


# ─────────────────────────────────────────────────────────────────────────────
@app.post("/verify/audio", tags=["Verification"])
async def verify_audio_poisoning(file: UploadFile = File(...)):
    """
    Upload a poisoned audio file and verify:
    - Human-audible quality is preserved (`human_safe`).
    - Ultrasonic disruption layer is present (`ai_disruption`).

    Returns full verification metrics.
    """
    upload_path = _save_upload(file)
    result = engine.acoustic_poisoning.verify_poisoning(str(upload_path))
    return JSONResponse(content=result)


# ─────────────────────────────────────────────────────────────────────────────
@app.post("/simulate/clone", tags=["Demo"])
async def simulate_voice_clone(file: UploadFile = File(...)):
    """
    Simulate what a voice-cloning model produces when trained on poisoned audio.

    Returns the simulated (garbled) audio file and a quality score
    (0 = completely broken, 1 = clean — poisoning aims for < 0.3).
    """
    upload_path = _save_upload(file)
    result = engine.acoustic_poisoning.simulate_clone_output(str(upload_path))
    return FileResponse(
        path=result["output_path"],
        filename="simulated_clone_output.wav",
        media_type="audio/wav",
        headers={"X-Quality-Score": str(result["quality_score"])},
    )


# ─────────────────────────────────────────────────────────────────────────────
@app.delete("/logs", tags=["Monitoring"])
async def clear_logs():
    """Clear the in-memory log buffer."""
    engine.clear_logs()
    return {"status": "logs cleared"}


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ml_api:app", host="0.0.0.0", port=8000, reload=False)
