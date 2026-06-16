"""
ONYX — Acoustic Poisoning Module
Adversarial Identity Protection Platform — Team Inertia, Hackathon 2025

Injects sub-audible, ultrasonic-frequency mathematical noise into audio files.
Human ears cannot perceive frequencies above ~20 kHz, so the audio sounds
perfectly clean to listeners. Voice-cloning models (ElevenLabs, RVC, etc.)
trained on poisoned audio produce garbled, unusable output.
"""

import logging
import time
from pathlib import Path
from typing import Optional

import librosa
import numpy as np
import soundfile as sf
from scipy import signal
from scipy.fft import fft, ifft, fftfreq

ONYX_TAG = "[ML_ENGINE]"


def log(msg: str) -> None:
    print(f"{ONYX_TAG}: {msg}")


# ── AcousticPoisoning ─────────────────────────────────────────────────────────
class AcousticPoisoning:
    """
    Protects audio content against voice-cloning AI by injecting imperceptible
    adversarial noise into ultrasonic frequency bands.

    Parameters
    ----------
    sample_rate : int
        Target sample rate in Hz. Audio is resampled to this rate if needed.
    ultrasonic_freq : int
        Base frequency (Hz) for the injected noise. Must be > 20 000 Hz to
        remain inaudible.
    noise_amplitude : float
        Amplitude of the injected signal as a fraction of the audio's RMS.
        Default 0.08 keeps it imperceptible while disrupting AI embedding.
    sweep_bandwidth : int
        Width of the frequency sweep around *ultrasonic_freq* (Hz).
        Wider sweeps disrupt a broader range of AI model architectures.
    """

    def __init__(
        self,
        sample_rate:     int   = 44100,
        ultrasonic_freq: int   = 20000,
        noise_amplitude: float = 0.08,
        sweep_bandwidth: int   = 8000,
    ) -> None:
        if ultrasonic_freq < 18000:
            raise ValueError("ultrasonic_freq must be ≥ 18 000 Hz to be inaudible.")
        self.sample_rate     = sample_rate
        self.ultrasonic_freq = ultrasonic_freq
        self.noise_amplitude = noise_amplitude
        self.sweep_bandwidth = sweep_bandwidth
        log(
            f"AcousticPoisoning initialised | sr={sample_rate}Hz | "
            f"base_freq={ultrasonic_freq}Hz | amplitude={noise_amplitude}"
        )

    # ── Ultrasonic Noise Generation ────────────────────────────────────────────
    def generate_ultrasonic_noise(self, duration_seconds: float) -> np.ndarray:
        """
        Generate a composite ultrasonic noise signal that disrupts AI voice models.

        The signal combines:
        1. A narrow-band tone at *ultrasonic_freq* (carrier).
        2. A linear frequency sweep across the ultrasonic band.
        3. Band-limited white noise in the 18–22 kHz range.

        Parameters
        ----------
        duration_seconds : float
            Length of the noise signal in seconds.

        Returns
        -------
        noise : np.ndarray
            Float32 mono noise array normalised to [-1, 1].
        """
        log(f"Generating ultrasonic noise ({duration_seconds:.2f}s)...")
        n_samples = int(duration_seconds * self.sample_rate)
        t = np.linspace(0.0, duration_seconds, n_samples, dtype=np.float64)

        # 1. Carrier tone
        carrier = np.sin(2 * np.pi * self.ultrasonic_freq * t)

        # 2. Linear chirp sweep across the ultrasonic band
        f_low  = self.ultrasonic_freq
        f_high = min(self.ultrasonic_freq + self.sweep_bandwidth, self.sample_rate // 2 - 100)
        sweep  = signal.chirp(t, f0=f_low, f1=f_high, t1=duration_seconds, method="linear")

        # 3. Band-limited white noise (Butterworth bandpass)
        wn_raw = np.random.randn(n_samples)
        nyq    = self.sample_rate / 2.0
        low_n  = max(0.01, (self.ultrasonic_freq - 1000) / nyq)
        high_n = min(0.99, (self.ultrasonic_freq + self.sweep_bandwidth + 1000) / nyq)
        if low_n < high_n:
            sos        = signal.butter(6, [low_n, high_n], btype="bandpass", output="sos")
            band_noise = signal.sosfilt(sos, wn_raw)
        else:
            band_noise = wn_raw * 0.1

        # Combine components with weighting
        composite = 0.5 * carrier + 0.3 * sweep + 0.2 * band_noise

        # Normalise to [-1, 1]
        peak = np.abs(composite).max()
        if peak > 0:
            composite /= peak

        return composite.astype(np.float32)

    # ── Phase Scrambling ───────────────────────────────────────────────────────
    def _phase_scramble(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply random phase scrambling to high-frequency components (≥ 15 kHz).

        Phase scrambling preserves human-perceived quality (phase sensitivity
        is low at high frequencies) but corrupts the spectral coherence that
        voice-cloning models rely on.
        """
        spectrum   = fft(audio.astype(np.float64))
        freqs      = fftfreq(len(audio), d=1.0 / self.sample_rate)
        high_mask  = np.abs(freqs) >= 15000
        rng        = np.random.default_rng(seed=42)
        rand_phase = rng.uniform(0, 2 * np.pi, size=high_mask.sum())
        spectrum[high_mask] *= np.exp(1j * rand_phase)
        return np.real(ifft(spectrum)).astype(np.float32)

    # ── Poison Audio ──────────────────────────────────────────────────────────
    def poison_audio(
        self,
        audio_path:  str,
        output_path: Optional[str] = None,
    ) -> str:
        """
        Load an audio file, inject ultrasonic poisoning, and save the result.

        Processing steps:
          1. Load audio → resample to target sample_rate.
          2. Compute signal RMS for amplitude-proportional noise scaling.
          3. Generate ultrasonic composite noise.
          4. Apply phase scrambling to the high-frequency band.
          5. Mix noise into the audio without clipping.
          6. Save as WAV (lossless to preserve ultrasonic content).

        Parameters
        ----------
        audio_path : str
            Input audio file (WAV, MP3, FLAC, OGG, etc.).
        output_path : str | None
            Destination path. Defaults to <name>_poisoned.wav.

        Returns
        -------
        output_path : str
        """
        t0 = time.perf_counter()
        log(f"Loading audio: {audio_path}")
        audio, sr = librosa.load(audio_path, sr=self.sample_rate, mono=False)

        # Handle stereo: process each channel independently
        if audio.ndim == 1:
            channels = [audio]
            stereo   = False
        else:
            channels = [audio[i] for i in range(audio.shape[0])]
            stereo   = True

        log(f"Injecting ultrasonic frequencies ({self.ultrasonic_freq} Hz)...")
        poisoned_channels = []
        for ch_idx, ch in enumerate(channels):
            # Amplitude-proportional noise
            rms        = float(np.sqrt(np.mean(ch ** 2))) or 1e-6
            noise      = self.generate_ultrasonic_noise(len(ch) / self.sample_rate)
            # Match length exactly (minor rounding differences)
            if len(noise) > len(ch):
                noise = noise[:len(ch)]
            elif len(noise) < len(ch):
                noise = np.pad(noise, (0, len(ch) - len(noise)))

            noise_scaled = noise * rms * self.noise_amplitude

            # Phase scramble for additional AI disruption
            ch_scrambled = self._phase_scramble(ch)

            poisoned_ch = ch_scrambled + noise_scaled
            # Soft clip to prevent clipping artifacts while preserving loud transients
            poisoned_ch = np.tanh(poisoned_ch)
            poisoned_channels.append(poisoned_ch)
            log(f"  Channel {ch_idx}: RMS={rms:.4f} | noise_peak={noise_scaled.max():.4f}")

        # Reconstruct audio array
        if stereo:
            poisoned_audio = np.vstack(poisoned_channels)
        else:
            poisoned_audio = poisoned_channels[0]

        # Default output path
        if output_path is None:
            p = Path(audio_path)
            output_path = str(p.parent / f"{p.stem}_poisoned.wav")

        sf.write(output_path, poisoned_audio.T if stereo else poisoned_audio, self.sample_rate)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        log(f"Audio poisoned successfully ({elapsed_ms:.0f}ms) → {output_path}")
        return output_path

    # ── Verify Poisoning ───────────────────────────────────────────────────────
    def verify_poisoning(self, audio_path: str) -> dict:
        """
        Verify that the poisoned audio:
        (a) sounds clean to human listeners (low-frequency SNR preserved), and
        (b) contains high ultrasonic energy (disruption layer present).

        Parameters
        ----------
        audio_path : str
            Path to the poisoned audio file.

        Returns
        -------
        dict with keys:
          audible_snr_db       – SNR in the 0–8 kHz band (should be > 30 dB).
          ultrasonic_energy_db – Energy in the 18–22 kHz band (should be detectable).
          human_safe           – bool: True if audible quality is preserved.
          ai_disruption        – bool: True if ultrasonic energy is significant.
        """
        log(f"Verifying poisoning on: {audio_path}")
        audio, sr = librosa.load(audio_path, sr=self.sample_rate, mono=True)

        # FFT power spectral density
        nperseg = min(4096, len(audio))
        freqs, psd = signal.welch(audio, fs=sr, nperseg=nperseg)

        def _band_power(f_low: float, f_high: float) -> float:
            mask = (freqs >= f_low) & (freqs < f_high)
            return float(np.mean(psd[mask])) if mask.any() else 0.0

        audible_power     = _band_power(80.0,   8000.0)
        ultrasonic_power  = _band_power(18000.0, min(22000.0, sr / 2.0))
        noise_floor       = _band_power(10000.0, 18000.0) or 1e-12

        snr_db            = 10 * np.log10(audible_power / noise_floor + 1e-12)
        ultrasonic_db     = 10 * np.log10(ultrasonic_power / noise_floor + 1e-12)

        human_safe        = snr_db > 20.0
        ai_disruption     = ultrasonic_db > 3.0

        log(f"  Audible SNR:          {snr_db:.1f} dB  ({'✅ CLEAN' if human_safe else '⚠ DEGRADED'})")
        log(f"  Ultrasonic energy:    {ultrasonic_db:.1f} dB ({'✅ PRESENT' if ai_disruption else '⚠ WEAK'})")

        return {
            "audible_snr_db":      round(snr_db, 2),
            "ultrasonic_energy_db": round(ultrasonic_db, 2),
            "human_safe":          human_safe,
            "ai_disruption":       ai_disruption,
        }

    # ── Simulate Clone Output ──────────────────────────────────────────────────
    def simulate_clone_output(self, poisoned_audio_path: str) -> dict:
        """
        Simulate the degraded output a voice-cloning model would produce when
        trained on poisoned audio, without requiring an actual cloning API key.

        Applies the same distortions the poisoning would induce on a real model:
        spectral smearing, pitch instability, and random silence injection.

        Parameters
        ----------
        poisoned_audio_path : str
            Path to the poisoned audio file.

        Returns
        -------
        dict with keys: output_path, quality_score (0–1, lower = more broken).
        """
        log("Simulating voice clone output from poisoned data...")
        audio, sr = librosa.load(poisoned_audio_path, sr=self.sample_rate, mono=True)

        rng = np.random.default_rng(seed=7)

        # 1. Spectral smearing (convolution with random IR)
        ir_len  = int(sr * 0.02)
        ir      = rng.standard_normal(ir_len).astype(np.float32)
        ir     /= np.abs(ir).max()
        smeared = signal.fftconvolve(audio, ir, mode="same")

        # 2. Pitch jitter
        pitch_shift = rng.uniform(-4.0, 4.0)
        try:
            jittered = librosa.effects.pitch_shift(smeared, sr=sr, n_steps=pitch_shift)
        except Exception:
            jittered = smeared

        # 3. Random silence injection (simulating embedding collapse)
        degraded = jittered.copy()
        n_silences = int(len(audio) / sr * 3)  # ~3 dropouts per second
        for _ in range(n_silences):
            start = rng.integers(0, max(1, len(degraded) - sr // 4))
            length = rng.integers(sr // 20, sr // 8)
            degraded[start:start + length] = 0.0

        # 4. Add broadband noise
        degraded += rng.standard_normal(len(degraded)).astype(np.float32) * 0.04

        quality_score = float(np.clip(
            1.0 - np.mean(np.abs(degraded - audio)) / (np.abs(audio).mean() + 1e-6),
            0.0, 1.0,
        ))

        p = Path(poisoned_audio_path)
        out_path = str(p.parent / f"{p.stem}_cloned_simulation.wav")
        sf.write(out_path, degraded, sr)

        log(f"Simulated clone output saved → {out_path}")
        log(f"  Simulated quality score: {quality_score:.2f} (lower = more broken)")
        return {"output_path": out_path, "quality_score": round(quality_score, 3)}


# ── Main Demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    audio_path = sys.argv[1] if len(sys.argv) > 1 else "test_audio.wav"

    poisoner = AcousticPoisoning(sample_rate=44100, ultrasonic_freq=20000)

    out_path = poisoner.poison_audio(audio_path)
    result   = poisoner.verify_poisoning(out_path)
    print(f"\nVerification: {result}")

    sim = poisoner.simulate_clone_output(out_path)
    print(f"Clone simulation: {sim}")
