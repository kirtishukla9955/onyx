"""
ONYX — demo_face_detection.py
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Run this to prove Digital Camouflage works:
  1. Loads a creator photo.
  2. Detects face on original → success (green box).
  3. Applies ONYX cloak.
  4. Detects face on cloaked → fails completely.
  5. Saves a side-by-side comparison image.

Usage:
    python demo_face_detection.py <image_path>
    python demo_face_detection.py  # uses test_face.jpg if present
"""

import sys
import time
from pathlib import Path

import cv2

from digital_camouflage import DigitalCamouflage
from face_detection_demo import FaceDetectionDemo

ONYX_TAG = "[ML_ENGINE]"


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {ONYX_TAG}: {msg}")


def run_demo(image_path: str) -> None:
    p = Path(image_path)
    if not p.exists():
        print(f"❌  File not found: {image_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  ONYX — Digital Camouflage Demo")
    print("  Adversarial Identity Protection Platform")
    print("=" * 60 + "\n")

    # ── Step 1: Verify detection on original ──────────────────────────────────
    log("Loading original image...")
    orig_image = cv2.imread(image_path)
    if orig_image is None:
        print(f"❌  Cannot read image: {image_path}")
        sys.exit(1)

    cam = DigitalCamouflage(eps=0.03, alpha=0.005, steps=40)

    log("Running face detection on ORIGINAL image...")
    orig_faces = cam.detect_faces(orig_image)
    log(f"Original → {len(orig_faces)} face(s) detected  ✅")

    if not orig_faces:
        log("⚠  No faces found in original. Demo will still apply global cloak.")

    # ── Step 2: Apply ONYX cloak ──────────────────────────────────────────────
    log("Applying ONYX Digital Camouflage...")
    cloaked_path = str(p.parent / f"{p.stem}_cloaked{p.suffix}")
    cloaked, mask, cloaked_out = cam.apply_cloak(image_path, output_path=cloaked_path)

    # ── Step 3: Verify cloak defeated detection ───────────────────────────────
    log("Verifying cloak effectiveness...")
    result = cam.verify_cloak(cloaked_out)

    print("\n── Detection Results ───────────────────────────────────")
    print(f"  Original image  → {len(orig_faces)} face(s) detected")
    print(f"  Cloaked image   → {result['faces_detected']} face(s) detected")
    if result["cloak_effective"]:
        print("  Shield status   → ✅  CLOAK EFFECTIVE — AI detection DEFEATED")
    else:
        print("  Shield status   → ⚠   Detection partially survived — try higher eps/steps")
    print()

    # ── Step 4: Render side-by-side comparison ────────────────────────────────
    log("Rendering comparison panel...")
    demo = FaceDetectionDemo()
    comp_path = str(p.parent / f"{p.stem}_comparison.jpg")
    comparison = demo.run_comparison(
        original_path=image_path,
        cloaked_path=cloaked_out,
        output_path=comp_path,
        show_window=True,   # set False in headless environments
    )

    print(f"\n── Output Files ────────────────────────────────────────")
    print(f"  Cloaked image   → {cloaked_out}")
    print(f"  Comparison      → {comp_path}")
    print()
    print("ONYX. Protect before you post.")


if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else "test_face.jpg"
    run_demo(img)
