"""
ONYX — Face Detection Demo
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Demonstrates side-by-side face detection:
  • Original  → detection succeeds (green bounding box)
  • Cloaked   → detection fails   (red "NO FACE DETECTED" overlay)
"""

import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

ONYX_TAG = "[ML_ENGINE]"


def log(msg: str) -> None:
    print(f"{ONYX_TAG}: {msg}")


# ── Visual Style ───────────────────────────────────────────────────────────────
CYAN    = (255, 210, 0)    # BGR — electric cyan accent
GREEN   = (0, 255, 100)
RED     = (60, 60, 255)
WHITE   = (255, 255, 255)
DARK_BG = (20, 20, 20)

FONT       = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.65
THICKNESS  = 2


def _draw_label(img: np.ndarray, text: str, pos: tuple[int, int], color: tuple) -> None:
    cv2.putText(img, text, pos, FONT, FONT_SCALE, (0, 0, 0), THICKNESS + 2, cv2.LINE_AA)
    cv2.putText(img, text, pos, FONT, FONT_SCALE, color,     THICKNESS,     cv2.LINE_AA)


# ── FaceDetectionDemo ─────────────────────────────────────────────────────────
class FaceDetectionDemo:
    """
    Side-by-side ONYX demo: proves digital camouflage defeats face detection.

    Prefers MediaPipe → face_recognition → OpenCV Haar cascade (in that order)
    so the demo always runs regardless of installed packages.
    """

    def __init__(self) -> None:
        log("Initialising Face Detection Demo...")
        self._init_detector()

    # ── Detector Initialisation ────────────────────────────────────────────────
    def _init_detector(self) -> None:
        if MEDIAPIPE_AVAILABLE:
            self._backend = "mediapipe"
            log("Backend: MediaPipe FaceDetection")
        elif FACE_RECOGNITION_AVAILABLE:
            self._backend = "face_recognition"
            log("Backend: face_recognition (dlib HOG)")
        else:
            self._backend = "haar"
            self._haar = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            log("Backend: OpenCV Haar Cascade (fallback)")

    # ── Face Detection ─────────────────────────────────────────────────────────
    def detect_faces(self, image: np.ndarray) -> list[tuple[int, int, int, int]]:
        """
        Return list of bounding boxes (top, right, bottom, left) for detected faces.

        Parameters
        ----------
        image : np.ndarray
            BGR image.
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self._backend == "mediapipe":
            return self._mediapipe_detect(rgb, image.shape[:2])

        if self._backend == "face_recognition":
            return face_recognition.face_locations(rgb, model="hog")

        # Haar fallback
        gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self._haar.detectMultiScale(gray, 1.1, 5)
        return [(y, x + w, y + h, x) for (x, y, w, h) in faces]

    def _mediapipe_detect(
        self, rgb: np.ndarray, hw: tuple[int, int]
    ) -> list[tuple[int, int, int, int]]:
        h, w   = hw
        mp_fd  = mp.solutions.face_detection
        boxes: list[tuple[int, int, int, int]] = []
        with mp_fd.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
            res = fd.process(rgb)
            if res.detections:
                for det in res.detections:
                    bb  = det.location_data.relative_bounding_box
                    l   = max(0, int(bb.xmin * w))
                    t   = max(0, int(bb.ymin * h))
                    r   = min(w, int((bb.xmin + bb.width) * w))
                    b   = min(h, int((bb.ymin + bb.height) * h))
                    boxes.append((t, r, b, l))
        return boxes

    # ── Annotate Helper ────────────────────────────────────────────────────────
    def _annotate(
        self,
        image:      np.ndarray,
        faces:      list[tuple[int, int, int, int]],
        label:      str,
        detected:   bool,
    ) -> np.ndarray:
        """Draw bounding boxes and status banner on a copy of *image*."""
        out = image.copy()

        if detected and faces:
            for (top, right, bottom, left) in faces:
                cv2.rectangle(out, (left, top), (right, bottom), GREEN, 2)
                _draw_label(out, "FACE DETECTED", (left, top - 10), GREEN)
        else:
            # Full-image red overlay when detection fails
            overlay = out.copy()
            cv2.rectangle(overlay, (0, 0), (out.shape[1], out.shape[0]), (0, 0, 180), -1)
            out = cv2.addWeighted(overlay, 0.15, out, 0.85, 0)
            cx  = out.shape[1] // 2
            cy  = out.shape[0] // 2
            _draw_label(out, "NO FACE DETECTED", (cx - 130, cy), RED)
            _draw_label(out, "CLOAK ACTIVE",      (cx - 90,  cy + 30), CYAN)

        # Top banner
        banner_h = 36
        cv2.rectangle(out, (0, 0), (out.shape[1], banner_h), DARK_BG, -1)
        _draw_label(out, label, (10, 25), CYAN)

        return out

    # ── Side-by-Side Comparison ────────────────────────────────────────────────
    def run_comparison(
        self,
        original_path: str,
        cloaked_path:  str,
        output_path:   Optional[str] = None,
        show_window:   bool = True,
    ) -> np.ndarray:
        """
        Load original and cloaked images, run detection on both, and display/save
        a side-by-side comparison panel.

        Parameters
        ----------
        original_path : str
            Path to the unprotected image.
        cloaked_path : str
            Path to the ONYX-cloaked image.
        output_path : str | None
            If given, saves the comparison panel as an image file.
        show_window : bool
            If True, opens an OpenCV window (requires a display).

        Returns
        -------
        comparison : np.ndarray
            The rendered comparison panel (BGR).
        """
        log(f"Loading original  → {original_path}")
        original = cv2.imread(original_path)
        log(f"Loading cloaked   → {cloaked_path}")
        cloaked  = cv2.imread(cloaked_path)

        if original is None:
            raise FileNotFoundError(f"Cannot read: {original_path}")
        if cloaked is None:
            raise FileNotFoundError(f"Cannot read: {cloaked_path}")

        # Resize both to the same height for panel layout
        target_h = 480
        def _resize_h(img: np.ndarray, h: int) -> np.ndarray:
            ratio = h / img.shape[0]
            return cv2.resize(img, (int(img.shape[1] * ratio), h))

        original = _resize_h(original, target_h)
        cloaked  = _resize_h(cloaked,  target_h)

        # Run detection
        log("Running detection on ORIGINAL image...")
        t0    = time.perf_counter()
        orig_faces = self.detect_faces(original)
        orig_ms    = (time.perf_counter() - t0) * 1000

        log("Running detection on CLOAKED image...")
        t0    = time.perf_counter()
        clk_faces  = self.detect_faces(cloaked)
        clk_ms     = (time.perf_counter() - t0) * 1000

        log(f"Original: {len(orig_faces)} face(s) in {orig_ms:.1f}ms")
        log(f"Cloaked:  {len(clk_faces)} face(s) in {clk_ms:.1f}ms")

        # Annotate panels
        orig_panel = self._annotate(
            original, orig_faces,
            f"ORIGINAL  [{len(orig_faces)} face(s) — {orig_ms:.0f}ms]",
            detected=len(orig_faces) > 0,
        )
        clk_panel = self._annotate(
            cloaked, clk_faces,
            f"CLOAKED   [{len(clk_faces)} face(s) — SHIELD ACTIVE]",
            detected=len(clk_faces) > 0,
        )

        # Divider
        divider = np.full((target_h, 4, 3), list(CYAN), dtype=np.uint8)
        comparison = np.hstack([orig_panel, divider, clk_panel])

        # Footer bar
        footer_h = 40
        footer   = np.full((footer_h, comparison.shape[1], 3), list(DARK_BG), dtype=np.uint8)
        _draw_label(footer, "ONYX — Adversarial Identity Protection Platform", (10, 28), CYAN)
        comparison = np.vstack([comparison, footer])

        if output_path:
            cv2.imwrite(output_path, comparison)
            log(f"Comparison saved → {output_path}")

        if show_window:
            cv2.imshow("ONYX — Face Detection Comparison", comparison)
            log("Press any key to close the window...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return comparison

    # ── Live Webcam Demo ───────────────────────────────────────────────────────
    def run_live_demo(self, camouflage_fn=None) -> None:
        """
        Optional real-time webcam demo.

        Captures from the default webcam and applies face detection each frame.
        If *camouflage_fn* is provided (a callable accepting and returning BGR
        np.ndarray), it is applied to the right panel in near-real-time.

        Press 'q' to quit.
        """
        log("Starting live webcam demo (press 'q' to quit)...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            log("⚠ No webcam found — aborting live demo")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            faces = self.detect_faces(frame)
            left_panel = self._annotate(frame, faces, "LIVE — ORIGINAL", len(faces) > 0)

            if camouflage_fn:
                cloaked_frame  = camouflage_fn(frame)
                clk_faces      = self.detect_faces(cloaked_frame)
                right_panel    = self._annotate(cloaked_frame, clk_faces, "LIVE — CLOAKED", len(clk_faces) > 0)
            else:
                right_panel = left_panel.copy()
                _draw_label(right_panel, "Cloak not applied", (10, 60), WHITE)

            divider  = np.full((frame.shape[0], 4, 3), list(CYAN), dtype=np.uint8)
            combined = np.hstack([left_panel, divider, right_panel])
            cv2.imshow("ONYX — Live Demo", combined)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        log("Live demo ended.")


# ── Main Demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python face_detection_demo.py <original_image> <cloaked_image>")
        sys.exit(1)

    demo = FaceDetectionDemo()
    demo.run_comparison(
        original_path=sys.argv[1],
        cloaked_path=sys.argv[2],
        output_path="onyx_comparison.jpg",
        show_window=True,
    )
