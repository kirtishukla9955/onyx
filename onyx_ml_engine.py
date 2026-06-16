"""
ONYX — ML Engine Orchestrator
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Central orchestrator that routes files through the correct protection pipeline
(Digital Camouflage for images/video, Acoustic Poisoning for audio) and
exposes a real-time log stream for the ONYX dashboard terminal sidebar.
"""

import threading
import time
from collections import deque
from pathlib import Path
from typing import Optional

import cv2

from digital_camouflage import DigitalCamouflage
from acoustic_poisoning import AcousticPoisoning

ONYX_TAG = "[ML_ENGINE]"

# Supported file extensions per modality
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}
AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}


def _ts() -> str:
    return time.strftime("%H:%M:%S")


class ONYXMLEngine:
    """
    Orchestrates Digital Camouflage and Acoustic Poisoning pipelines.

    Usage
    -----
    engine = ONYXMLEngine()
    result = engine.process_file("creator_photo.jpg")
    logs   = engine.get_logs()
    """

    def __init__(
        self,
        pgd_eps:         float = 0.03,
        pgd_steps:       int   = 40,
        ultrasonic_freq: int   = 20000,
        max_log_lines:   int   = 500,
    ) -> None:
        self._log_buffer: deque[str] = deque(maxlen=max_log_lines)
        self._lock = threading.Lock()

        self._emit("Initialising ONYX ML Engine...")
        self.digital_camouflage = DigitalCamouflage(eps=pgd_eps, steps=pgd_steps)
        self.acoustic_poisoning = AcousticPoisoning(ultrasonic_freq=ultrasonic_freq)
        self._emit("ML Engine ready ✅")

    # ── Log Helpers ────────────────────────────────────────────────────────────
    def _emit(self, msg: str) -> None:
        line = f"[{_ts()}] {ONYX_TAG}: {msg}"
        with self._lock:
            self._log_buffer.append(line)
        print(line)

    def get_logs(self, last_n: Optional[int] = None) -> list[str]:
        """
        Return recent processing log lines for the ONYX dashboard terminal.

        Parameters
        ----------
        last_n : int | None
            Return only the most recent *last_n* lines. None = all.
        """
        with self._lock:
            logs = list(self._log_buffer)
        return logs[-last_n:] if last_n else logs

    def clear_logs(self) -> None:
        with self._lock:
            self._log_buffer.clear()

    # ── Image Processing ───────────────────────────────────────────────────────
    def process_image(
        self,
        image_path:  str,
        output_path: Optional[str] = None,
    ) -> dict:
        """
        Apply Digital Camouflage to a single image.

        Returns
        -------
        dict with keys: success, output_path, faces_detected, elapsed_ms.
        """
        self._emit(f"Processing IMAGE → {Path(image_path).name}")
        self._emit("Detecting facial regions...")
        t0 = time.perf_counter()
        try:
            cloaked, mask, out = self.digital_camouflage.apply_cloak(image_path, output_path)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            self._emit(f"Cloak applied successfully ({elapsed_ms:.0f}ms)")

            verify = self.digital_camouflage.verify_cloak(out)
            status = "✅ PROTECTED" if verify["cloak_effective"] else "⚠ PARTIAL"
            self._emit(f"Shield status: {status}")

            return {
                "success":        True,
                "output_path":    out,
                "faces_detected": verify["faces_detected"],
                "cloak_effective": verify["cloak_effective"],
                "elapsed_ms":     round(elapsed_ms, 1),
            }
        except Exception as exc:
            self._emit(f"❌ Image processing failed: {exc}")
            return {"success": False, "error": str(exc)}

    # ── Video Processing ───────────────────────────────────────────────────────
    def process_video(
        self,
        video_path:    str,
        output_path:   Optional[str] = None,
        max_frames:    Optional[int] = None,
        frame_skip:    int           = 1,
    ) -> dict:
        """
        Apply Digital Camouflage to every (or every *frame_skip*-th) frame.

        Parameters
        ----------
        video_path : str
            Input video file path.
        output_path : str | None
            Output video path. Defaults to <name>_cloaked.<ext>.
        max_frames : int | None
            Cap the number of processed frames (useful for demos).
        frame_skip : int
            Process every Nth frame (1 = all frames, 2 = every other, etc.)

        Returns
        -------
        dict with keys: success, output_path, total_frames, elapsed_ms.
        """
        self._emit(f"Processing VIDEO → {Path(video_path).name}")
        t0  = time.perf_counter()
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self._emit(f"❌ Cannot open video: {video_path}")
            return {"success": False, "error": f"Cannot open {video_path}"}

        fps    = cap.get(cv2.CAP_PROP_FPS) or 25.0
        w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total  = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._emit(f"Video info: {w}×{h} @ {fps:.1f}fps | {total} frames")

        if output_path is None:
            p = Path(video_path)
            output_path = str(p.parent / f"{p.stem}_cloaked.mp4")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        frame_idx     = 0
        processed     = 0
        cloaked_cache = None   # Re-use last cloaked frame for skipped frames

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if max_frames and processed >= max_frames:
                break

            if frame_idx % frame_skip == 0:
                self._emit(f"Generating Adversarial Noise Mask... (frame {frame_idx})")
                import tempfile, os
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp_path = tmp.name
                try:
                    cv2.imwrite(tmp_path, frame)
                    cloaked_frame, _, _ = self.digital_camouflage.apply_cloak(tmp_path)
                    cloaked_cache = cloaked_frame
                finally:
                    os.unlink(tmp_path)
                processed += 1
            else:
                cloaked_cache = frame if cloaked_cache is None else cloaked_cache

            writer.write(cloaked_cache)
            frame_idx += 1

        cap.release()
        writer.release()

        elapsed_ms = (time.perf_counter() - t0) * 1000
        self._emit(f"Video cloaked ({processed} frames, {elapsed_ms:.0f}ms) → {output_path}")
        return {
            "success":       True,
            "output_path":   output_path,
            "total_frames":  frame_idx,
            "processed_frames": processed,
            "elapsed_ms":    round(elapsed_ms, 1),
        }

    # ── Audio Processing ───────────────────────────────────────────────────────
    def process_audio(
        self,
        audio_path:  str,
        output_path: Optional[str] = None,
    ) -> dict:
        """
        Apply Acoustic Poisoning to an audio file.

        Returns
        -------
        dict with keys: success, output_path, verification, elapsed_ms.
        """
        self._emit(f"Processing AUDIO → {Path(audio_path).name}")
        self._emit("Injecting ultrasonic frequencies...")
        t0 = time.perf_counter()
        try:
            out = self.acoustic_poisoning.poison_audio(audio_path, output_path)
            self._emit("Verifying acoustic shield...")
            verify     = self.acoustic_poisoning.verify_poisoning(out)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            status     = "✅ PROTECTED" if verify["ai_disruption"] and verify["human_safe"] else "⚠ PARTIAL"
            self._emit(f"Audio shield status: {status} ({elapsed_ms:.0f}ms)")
            return {
                "success":      True,
                "output_path":  out,
                "verification": verify,
                "elapsed_ms":   round(elapsed_ms, 1),
            }
        except Exception as exc:
            self._emit(f"❌ Audio processing failed: {exc}")
            return {"success": False, "error": str(exc)}

    # ── Universal Router ───────────────────────────────────────────────────────
    def process_file(self, file_path: str, **kwargs) -> dict:
        """
        Inspect *file_path* extension and route to the appropriate pipeline.

        Parameters
        ----------
        file_path : str
            Any supported image, video, or audio file.
        **kwargs
            Forwarded to the specific processor (e.g., output_path, frame_skip).

        Returns
        -------
        dict from the specific processor, plus a 'file_type' key.
        """
        ext = Path(file_path).suffix.lower()
        self._emit(f"Received file: {Path(file_path).name} (ext={ext})")

        if ext in IMAGE_EXTS:
            result = self.process_image(file_path, **kwargs)
            result["file_type"] = "image"
        elif ext in VIDEO_EXTS:
            result = self.process_video(file_path, **kwargs)
            result["file_type"] = "video"
        elif ext in AUDIO_EXTS:
            result = self.process_audio(file_path, **kwargs)
            result["file_type"] = "audio"
        else:
            msg = f"Unsupported file type: {ext}"
            self._emit(f"❌ {msg}")
            result = {"success": False, "error": msg, "file_type": "unknown"}

        return result


# ── Main Demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python onyx_ml_engine.py <file_path>")
        sys.exit(1)

    engine = ONYXMLEngine()
    result = engine.process_file(sys.argv[1])

    print("\n── Result ──────────────────────────────────")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print("\n── Last 10 log lines ───────────────────────")
    for line in engine.get_logs(last_n=10):
        print(line)
