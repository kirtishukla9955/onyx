import React, { useState, useRef } from 'react';
import { Volume2, Download, RotateCcw, Play, Pause, ShieldCheck } from 'lucide-react';
import { Panel, StatusBanner, PrimaryButton, SecondaryButton } from '../components/DashboardUI';
import Dropzone from '../components/Dropzone';
import { poisonAudio } from '../api/ml';

export default function Acoustic() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');
  const [resultUrl, setResultUrl] = useState(null);
  const [playing, setPlaying] = useState(false);
  const audioRef = useRef(null);

  function handleFile(f) {
    setFile(f);
    setStatus(null);
    setResultUrl(null);
  }

  async function handlePoison() {
    if (!file) return;
    setStatus('loading');
    setMessage('Injecting ultrasonic poison layer...');
    try {
      const blob = await poisonAudio(file);
      setResultUrl(URL.createObjectURL(blob));
      setStatus('success');
      setMessage('Audio poisoned. Sounds identical, breaks voice-clone training.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the ML backend on localhost:8002. Is it running?');
    }
  }

  function reset() {
    setFile(null);
    setStatus(null);
    setResultUrl(null);
    setPlaying(false);
  }

  function togglePlay() {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setPlaying(!playing);
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-cyan-glow/30 bg-cyan-soft shrink-0">
          <Volume2 size={22} className="text-cyan-glow" />
        </div>
        <div>
          <h2 className="font-display font-semibold text-2xl">Acoustic Poisoning</h2>
          <p className="text-ink-dim mt-1">
            Upload an audio track. ONYX injects sub-audible, ultrasonic noise that's inaudible to people
            but corrupts any voice-cloning model trained on it.
          </p>
        </div>
      </div>

      <Panel eyebrow="Step 1" title="Upload your audio">
        <Dropzone
          accept="audio/*"
          file={file}
          onFileSelected={handleFile}
          label="Drop an audio file, or click to browse"
          hint="MP3, WAV, or M4A"
        />
      </Panel>

      <Panel eyebrow="Step 2" title="Run protection">
        <StatusBanner state={status} message={message} />

        {!resultUrl ? (
          <PrimaryButton onClick={handlePoison} disabled={!file || status === 'loading'} icon={ShieldCheck}>
            {status === 'loading' ? 'Poisoning audio...' : 'Poison this audio'}
          </PrimaryButton>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center gap-4 rounded-xl border border-void-border bg-void-deep/60 px-5 py-4">
              <button
                onClick={togglePlay}
                className="w-10 h-10 rounded-full bg-cyan-glow text-void-deep flex items-center justify-center shrink-0 hover:shadow-[0_0_20px_rgba(0,240,255,0.5)] transition-shadow"
              >
                {playing ? <Pause size={16} /> : <Play size={16} />}
              </button>
              <div className="flex-1">
                <div className="text-sm font-medium">Poisoned preview</div>
                <div className="text-xs text-ink-faint">Sounds clean. The poison lives above 19kHz.</div>
              </div>
              <audio ref={audioRef} src={resultUrl} onEnded={() => setPlaying(false)} className="hidden" />
            </div>
            <div className="flex flex-wrap gap-3">
              <SecondaryButton href={resultUrl} icon={Download}>Download poisoned file</SecondaryButton>
              <SecondaryButton onClick={reset} icon={RotateCcw}>Poison another file</SecondaryButton>
            </div>
          </div>
        )}

        <p className="text-xs text-ink-faint mt-4">
          This calls <code className="text-cyan-glow">POST /poison-audio</code> on your ML backend at{' '}
          <code className="text-cyan-glow">localhost:8002</code>.
        </p>
      </Panel>
    </div>
  );
}
