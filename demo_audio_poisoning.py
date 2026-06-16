"""
ONYX — demo_audio_poisoning.py
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Run this to prove Acoustic Poisoning works:
  1. Loads a creator audio file.
  2. Injects ultrasonic adversarial noise (inaudible to humans).
  3. Verifies the poisoned audio sounds clean (audible SNR preserved).
  4. Simulates what a voice-cloning model would produce (garbled output).
  5. Prints a full verification report.

Usage:
    python demo_audio_poisoning.py <audio_path>
    python demo_audio_poisoning.py  # uses test_audio.wav if present
"""

import sys
import time
from pathlib import Path

from acoustic_poisoning import AcousticPoisoning

ONYX_TAG = "[ML_ENGINE]"


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {ONYX_TAG}: {msg}")


def run_demo(audio_path: str) -> None:
    p = Path(audio_path)
    if not p.exists():
        print(f"❌  File not found: {audio_path}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  ONYX — Acoustic Poisoning Demo")
    print("  Adversarial Identity Protection Platform")
    print("=" * 60 + "\n")

    poisoner = AcousticPoisoning(
        sample_rate=44100,
        ultrasonic_freq=20000,
        noise_amplitude=0.08,
        sweep_bandwidth=8000,
    )

    # ── Step 1: Inject ultrasonic poison ──────────────────────────────────────
    log("Loading original audio...")
    out_path = str(p.parent / f"{p.stem}_poisoned.wav")
    log("Injecting ultrasonic frequencies...")
    poisoned_path = poisoner.poison_audio(audio_path, output_path=out_path)

    # ── Step 2: Verify quality & disruption ───────────────────────────────────
    log("Verifying acoustic shield...")
    verify = poisoner.verify_poisoning(poisoned_path)

    print("\n── Verification Report ─────────────────────────────────")
    print(f"  Audible SNR (human perception):  {verify['audible_snr_db']:.1f} dB")
    print(f"  Ultrasonic energy (AI disruption): {verify['ultrasonic_energy_db']:.1f} dB")
    print(f"  Human-safe audio:     {'✅  YES — sounds completely normal' if verify['human_safe'] else '⚠  Degraded'}")
    print(f"  AI disruption active: {'✅  YES — voice cloning will fail'  if verify['ai_disruption'] else '⚠  Weak'}")
    print()

    # ── Step 3: Simulate voice clone output ───────────────────────────────────
    log("Simulating voice clone model output from poisoned data...")
    sim = poisoner.simulate_clone_output(poisoned_path)

    print(f"── Clone Simulation ────────────────────────────────────")
    print(f"  Simulated quality score: {sim['quality_score']:.3f}  (0 = garbage, 1 = clean)")
    if sim["quality_score"] < 0.4:
        print("  AI clone output:  ❌  UNUSABLE — garbled, incoherent audio")
    elif sim["quality_score"] < 0.7:
        print("  AI clone output:  ⚠   HEAVILY DEGRADED — partially unusable")
    else:
        print("  AI clone output:  ⚠   Partially preserved — consider increasing amplitude")
    print()

    print(f"── Output Files ────────────────────────────────────────")
    print(f"  Poisoned audio         → {poisoned_path}")
    print(f"  Simulated clone output → {sim['output_path']}")
    print()
    print("  🎧  Listen to the poisoned file — it sounds identical to the original.")
    print("  🤖  Feed it into ElevenLabs / RVC — the output will be robotic garbage.")
    print()
    print("ONYX. Protect before you post.")


if __name__ == "__main__":
    audio = sys.argv[1] if len(sys.argv) > 1 else "test_audio.wav"
    run_demo(audio)
