import React, { useState } from 'react';
import { Eye, Download, RotateCcw, ShieldCheck } from 'lucide-react';
import { Panel, StatusBanner, PrimaryButton, SecondaryButton } from '../components/DashboardUI';
import Dropzone from '../components/Dropzone';
import { cloakImage, cloakVideo } from '../api/ml';

const STRENGTHS = [
  { id: 'light', label: 'Light', desc: 'Fast, subtle perturbation' },
  { id: 'medium', label: 'Medium', desc: 'Balanced protection' },
  { id: 'maximum', label: 'Maximum', desc: 'Strongest defense, slower' },
];

export default function Camouflage() {
  const [file, setFile] = useState(null);
  const [strength, setStrength] = useState('medium');
  const [status, setStatus] = useState(null); // null | loading | success | error
  const [message, setMessage] = useState('');
  const [resultUrl, setResultUrl] = useState(null);

  function handleFile(f) {
    setFile(f);
    setStatus(null);
    setResultUrl(null);
  }

  async function handleCloak() {
    if (!file) return;
    setStatus('loading');
    setMessage('Computing adversarial perturbation...');
    try {
      const isVideo = file.type.startsWith('video');
      const blob = isVideo ? await cloakVideo(file, strength) : await cloakImage(file, strength);
      const url = URL.createObjectURL(blob);
      setResultUrl(url);
      setStatus('success');
      setMessage('Asset cloaked. Identical to the eye, unusable to a model.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the ML backend on localhost:8002. Is it running?');
    }
  }

  function reset() {
    setFile(null);
    setStatus(null);
    setResultUrl(null);
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-cyan-glow/30 bg-cyan-soft shrink-0">
          <Eye size={22} className="text-cyan-glow" />
        </div>
        <div>
          <h2 className="font-display font-semibold text-2xl">Digital Camouflage</h2>
          <p className="text-ink-dim mt-1">
            Upload a photo or video. ONYX injects an invisible adversarial perturbation across facial
            regions so deepfake and LoRA models can't train on it.
          </p>
        </div>
      </div>

      <Panel eyebrow="Step 1" title="Upload your asset">
        <Dropzone
          accept="image/*,video/*"
          file={file}
          onFileSelected={handleFile}
          label="Drop a photo or video, or click to browse"
          hint="PNG, JPG, or MP4"
        />
      </Panel>

      <Panel eyebrow="Step 2" title="Protection strength">
        <div className="grid sm:grid-cols-3 gap-3">
          {STRENGTHS.map((s) => (
            <button
              key={s.id}
              onClick={() => setStrength(s.id)}
              className={`text-left rounded-xl border px-4 py-3.5 transition-colors ${
                strength === s.id
                  ? 'border-cyan-glow/50 bg-cyan-soft'
                  : 'border-void-border hover:border-cyan-glow/30'
              }`}
            >
              <div className={`font-medium text-sm mb-1 ${strength === s.id ? 'text-cyan-glow' : 'text-ink'}`}>
                {s.label}
              </div>
              <div className="text-xs text-ink-faint">{s.desc}</div>
            </button>
          ))}
        </div>
      </Panel>

      <Panel eyebrow="Step 3" title="Run protection">
        <StatusBanner state={status} message={message} />

        {!resultUrl ? (
          <PrimaryButton onClick={handleCloak} disabled={!file || status === 'loading'} icon={ShieldCheck}>
            {status === 'loading' ? 'Cloaking asset...' : 'Cloak this asset'}
          </PrimaryButton>
        ) : (
          <div className="flex flex-wrap gap-3">
            <SecondaryButton href={resultUrl} icon={Download}>
              Download cloaked file
            </SecondaryButton>
            <SecondaryButton onClick={reset} icon={RotateCcw}>
              Cloak another asset
            </SecondaryButton>
          </div>
        )}

        <p className="text-xs text-ink-faint mt-4">
          This calls <code className="text-cyan-glow">POST /cloak-image</code> or{' '}
          <code className="text-cyan-glow">/cloak-video</code> on your ML backend at{' '}
          <code className="text-cyan-glow">localhost:8002</code>.
        </p>
      </Panel>
    </div>
  );
}
