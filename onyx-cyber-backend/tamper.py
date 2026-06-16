import cv2
import numpy as np

def verify_integrity(original_bytes: bytes, suspect_bytes: bytes) -> dict:
    # Decode images from bytes
    nparr_original = np.frombuffer(original_bytes, np.uint8)
    img_original = cv2.imdecode(nparr_original, cv2.IMREAD_COLOR)

    nparr_suspect = np.frombuffer(suspect_bytes, np.uint8)
    img_suspect = cv2.imdecode(nparr_suspect, cv2.IMREAD_COLOR)

    if img_original is None or img_suspect is None:
        raise ValueError("Invalid image file(s) provided. Ensure they are valid image formats.")

    if img_original.shape != img_suspect.shape:
        raise ValueError("Image dimensions do not match. Cannot perform pixel-level comparison.")

    # Compute absolute difference
    diff = cv2.absdiff(img_original, img_suspect)

    # Convert difference to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Threshold the difference (any non-zero difference is a tamper)
    # LSB changes might be very small (e.g., 1), so any difference > 0 becomes 255
    _, thresh = cv2.threshold(gray_diff, 0, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {
            "status": "AUTHENTIC",
            "flag": "green",
            "message": "Watermark is intact and matches original."
        }

    # Extract bounding boxes for tampered regions
    tampered_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        tampered_regions.append({
            "x": int(x),
            "y": int(y),
            "w": int(w),
            "h": int(h)
        })

    return {
        "status": "TAMPERED",
        "flag": "red",
        "message": "Watermark is broken or missing. Image has been altered.",
        "tampered_regions": tampered_regions
    }
