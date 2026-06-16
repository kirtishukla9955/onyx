"""
ONYX — Digital Camouflage Module
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Member 1: AI/ML Engineer
Implements PGD (Projected Gradient Descent) adversarial perturbation pipeline
targeting facial regions to defeat AI-based face recognition and deepfake training.
"""

import logging
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image

# Optional imports — graceful fallback if not installed
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

# ── Logging Setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [ML_ENGINE]: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ONYX.DigitalCamouflage")

ONYX_TAG = "[ML_ENGINE]"


def log(msg: str) -> None:
    """Emit a styled ONYX terminal log line."""
    print(f"{ONYX_TAG}: {msg}")


# ── Surrogate Model ────────────────────────────────────────────────────────────
def _build_surrogate_model(device: torch.device) -> nn.Module:
    """
    Build a lightweight surrogate face-embedding model.

    We use the first few layers of a pretrained ResNet-50 as a differentiable
    proxy for commercial face recognizers (FaceNet, ArcFace, etc.).
    Gradients from this surrogate drive the PGD attack.
    """
    backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    # Strip the classifier — we only need the embedding space
    surrogate = nn.Sequential(*list(backbone.children())[:-1])
    surrogate.eval()
    surrogate.to(device)
    for param in surrogate.parameters():
        param.requires_grad = False
    return surrogate


# ── Transforms ────────────────────────────────────────────────────────────────
_IMAGENET_MEAN = torch.tensor([0.485, 0.456, 0.406])
_IMAGENET_STD  = torch.tensor([0.229, 0.224, 0.225])

_to_tensor = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=_IMAGENET_MEAN.tolist(), std=_IMAGENET_STD.tolist()),
])


def _tensor_to_np_uint8(tensor: torch.Tensor) -> np.ndarray:
    """Convert a normalised [C, H, W] tensor back to a uint8 HWC numpy array."""
    mean = _IMAGENET_MEAN.view(3, 1, 1)
    std  = _IMAGENET_STD.view(3, 1, 1)
    img  = tensor.detach().cpu() * std + mean
    img  = img.clamp(0.0, 1.0).permute(1, 2, 0).numpy()
    return (img * 255).astype(np.uint8)


# ── DigitalCamouflage ─────────────────────────────────────────────────────────
class DigitalCamouflage:
    """
    Applies an invisible PGD adversarial cloak to facial regions in an image.

    The perturbation is constrained within ±eps in L∞ norm so that it remains
    imperceptible to human viewers while corrupting the face-embedding space
    used by AI models.

    Parameters
    ----------
    eps : float
        Maximum per-pixel perturbation magnitude (L∞, default 0.03 ≈ 8/255).
    alpha : float
        PGD step size per iteration.
    steps : int
        Number of PGD optimisation iterations.
    device : str | None
        Torch device string. Auto-detects CUDA/MPS/CPU if None.
    """

    def __init__(
        self,
        eps:    float = 0.03,
        alpha:  float = 0.01,
        steps:  int   = 40,
        device: Optional[str] = None,
    ) -> None:
        self.eps   = eps
        self.alpha = alpha
        self.steps = steps

        if device is None:
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
        self.device = torch.device(device)
        log(f"DigitalCamouflage initialised | device={self.device} | eps={eps} | steps={steps}")

        self.surrogate = _build_surrogate_model(self.device)

    # ── Face Detection ─────────────────────────────────────────────────────────
    def detect_faces(self, image: np.ndarray) -> list[tuple[int, int, int, int]]:
        """
        Detect faces and return bounding boxes as (top, right, bottom, left).

        Tries face_recognition library first; falls back to MediaPipe,
        then to OpenCV Haar cascades if neither is available.

        Parameters
        ----------
        image : np.ndarray
            BGR image as loaded by OpenCV.

        Returns
        -------
        list of (top, right, bottom, left) tuples in pixel coordinates.
        """
        log("Detecting facial regions...")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if FACE_RECOGNITION_AVAILABLE:
            boxes = face_recognition.face_locations(rgb, model="hog")
            log(f"face_recognition found {len(boxes)} face(s)")
            return boxes

        if MEDIAPIPE_AVAILABLE:
            boxes = self._detect_with_mediapipe(rgb)
            log(f"MediaPipe found {len(boxes)} face(s)")
            return boxes

        # Fallback: OpenCV Haar cascade
        boxes = self._detect_with_haar(image)
        log(f"Haar cascade found {len(boxes)} face(s)")
        return boxes

    def _detect_with_mediapipe(self, rgb: np.ndarray) -> list[tuple[int, int, int, int]]:
        """Run MediaPipe short-range face detection."""
        mp_fd = mp.solutions.face_detection
        h, w  = rgb.shape[:2]
        boxes: list[tuple[int, int, int, int]] = []
        with mp_fd.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
            results = fd.process(rgb)
            if results.detections:
                for det in results.detections:
                    bb   = det.location_data.relative_bounding_box
                    left = max(0, int(bb.xmin * w))
                    top  = max(0, int(bb.ymin * h))
                    right  = min(w, int((bb.xmin + bb.width) * w))
                    bottom = min(h, int((bb.ymin + bb.height) * h))
                    boxes.append((top, right, bottom, left))
        return boxes

    def _detect_with_haar(self, image: np.ndarray) -> list[tuple[int, int, int, int]]:
        """Fallback: OpenCV Haar cascade face detector."""
        gray    = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        boxes: list[tuple[int, int, int, int]] = []
        for (x, y, w, h) in faces:
            boxes.append((y, x + w, y + h, x))  # → (top, right, bottom, left)
        return boxes

    # ── PGD Perturbation ───────────────────────────────────────────────────────
    def generate_perturbation(
        self,
        image:      np.ndarray,
        face_boxes: list[tuple[int, int, int, int]],
    ) -> np.ndarray:
        """
        Run PGD to generate an adversarial perturbation over all detected faces.

        The attack maximises the distance between the original embedding and the
        perturbed embedding (feature-space disruption), keeping delta within L∞(eps).

        Parameters
        ----------
        image : np.ndarray
            Original BGR image.
        face_boxes : list of (top, right, bottom, left)
            Bounding boxes from detect_faces().

        Returns
        -------
        perturbation : np.ndarray
            Float32 array of shape (H, W, 3) with values in [-eps·255, eps·255].
        """
        log("Generating Adversarial Noise Mask...")
        rgb_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        x_orig  = _to_tensor(rgb_pil).unsqueeze(0).to(self.device)

        # Build binary mask (in 224×224 tensor space) for face regions
        h_orig, w_orig = image.shape[:2]
        mask = torch.zeros(1, 1, 224, 224, device=self.device)
        for (top, right, bottom, left) in face_boxes:
            # Map original pixel coords → 224×224
            t = int(top    / h_orig * 224)
            b = int(bottom / h_orig * 224)
            l = int(left   / w_orig * 224)      # noqa: E741
            r = int(right  / w_orig * 224)
            mask[:, :, t:b, l:r] = 1.0

        if mask.sum() == 0:
            log("⚠ No face region found in tensor space — applying global perturbation")
            mask = torch.ones(1, 1, 224, 224, device=self.device)

        # Compute original embedding (target to move away from)
        with torch.no_grad():
            emb_orig = self.surrogate(x_orig)

        # Initialise delta with small random noise inside the epsilon ball
        delta = (torch.rand_like(x_orig) * 2 - 1) * self.eps
        delta = delta * mask  # apply only to face region
        delta.requires_grad_(True)

        optimizer = torch.optim.Adam([delta], lr=self.alpha)

        for step in range(self.steps):
            optimizer.zero_grad()
            x_adv    = x_orig + delta * mask
            emb_adv  = self.surrogate(x_adv)
            # Maximise feature-space distance (negative loss = gradient ascent)
            loss = -nn.functional.mse_loss(emb_adv, emb_orig)
            loss.backward()
            optimizer.step()

            # Project back into L∞ epsilon ball
            with torch.no_grad():
                delta.clamp_(-self.eps, self.eps)

            if (step + 1) % 10 == 0:
                log(f"  PGD step {step+1}/{self.steps} | loss={-loss.item():.4f}")

        # Convert delta back to original image pixel space (0–255)
        with torch.no_grad():
            delta_np = delta.squeeze(0).cpu().permute(1, 2, 0).numpy()
            # Un-normalize to pixel space
            delta_np = delta_np * _IMAGENET_STD.numpy()
            delta_np = (delta_np * 255).astype(np.float32)

        # Upscale 224×224 perturbation back to original resolution
        perturbation = cv2.resize(delta_np, (w_orig, h_orig), interpolation=cv2.INTER_LINEAR)
        return perturbation  # float32, shape (H, W, 3)

    # ── Apply Cloak ────────────────────────────────────────────────────────────
    def apply_cloak(
        self,
        image_path:  str,
        output_path: Optional[str] = None,
    ) -> tuple[np.ndarray, np.ndarray, str]:
        """
        Full pipeline: load image → detect faces → generate perturbation → save.

        Parameters
        ----------
        image_path : str
            Path to the original image file.
        output_path : str | None
            Destination path. Defaults to <name>_cloaked.<ext> beside the original.

        Returns
        -------
        (cloaked_image, perturbation_mask, output_path)
        """
        t0 = time.perf_counter()
        log(f"Loading image: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")

        face_boxes = self.detect_faces(image)
        if not face_boxes:
            log("⚠ No faces detected — cloak applied globally as fallback")

        perturbation = self.generate_perturbation(image, face_boxes)

        # Add perturbation and clip to valid uint8 range
        cloaked = image.astype(np.float32) + perturbation
        cloaked = np.clip(cloaked, 0, 255).astype(np.uint8)

        # Derive output path
        if output_path is None:
            p = Path(image_path)
            output_path = str(p.parent / f"{p.stem}_cloaked{p.suffix}")

        cv2.imwrite(output_path, cloaked)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        log(f"Cloak applied successfully ({elapsed_ms:.0f}ms) → {output_path}")

        # Build a visualisable mask (absolute perturbation, normalised 0–255)
        mask_vis = np.abs(perturbation)
        mask_vis = (mask_vis / mask_vis.max() * 255).astype(np.uint8) if mask_vis.max() > 0 else mask_vis.astype(np.uint8)

        return cloaked, mask_vis, output_path

    # ── Verify Cloak ───────────────────────────────────────────────────────────
    def verify_cloak(self, cloaked_image_path: str) -> dict:
        """
        Verify that the cloaked image defeats face detection.

        Parameters
        ----------
        cloaked_image_path : str
            Path to the cloaked image.

        Returns
        -------
        dict with keys: faces_detected (int), cloak_effective (bool).
        """
        log(f"Verifying cloak on: {cloaked_image_path}")
        image     = cv2.imread(cloaked_image_path)
        if image is None:
            raise FileNotFoundError(f"Could not read: {cloaked_image_path}")
        faces     = self.detect_faces(image)
        effective = len(faces) == 0
        status    = "✅ CLOAK EFFECTIVE — Face detection FAILED" if effective else f"⚠ Detection still found {len(faces)} face(s)"
        log(status)
        return {"faces_detected": len(faces), "cloak_effective": effective}


# ── Main Demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    image_path = sys.argv[1] if len(sys.argv) > 1 else "test_face.jpg"

    cam = DigitalCamouflage(eps=0.03, alpha=0.005, steps=40)

    # Step 1: verify detection on original
    orig = cv2.imread(image_path)
    if orig is None:
        print(f"Please provide a valid image path. Got: {image_path}")
        sys.exit(1)

    original_faces = cam.detect_faces(orig)
    print(f"\nOriginal image  → {len(original_faces)} face(s) detected")

    # Step 2: apply cloak
    cloaked, mask, out_path = cam.apply_cloak(image_path)
    print(f"Cloaked image saved → {out_path}")

    # Step 3: verify cloak
    result = cam.verify_cloak(out_path)
    print(f"Verification    → cloak_effective={result['cloak_effective']}")
