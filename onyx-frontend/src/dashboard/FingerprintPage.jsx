import React, { useState } from 'react';
import { Fingerprint, Download, RotateCcw, KeyRound, ScanSearch, Users, CheckCircle2, AlertTriangle } from 'lucide-react';
import { Panel, StatusBanner, PrimaryButton, SecondaryButton } from '../components/DashboardUI';
import Dropzone from '../components/Dropzone';
import { embedWatermark, extractWatermark, verifyIntegrity, generateRecipientCopy, traceLeak } from '../api/cyber';

const TABS = [
  { id: 'embed', label: 'Embed Watermark', icon: KeyRound },
  { id: 'verify', label: 'Verify Integrity', icon: ScanSearch },
  { id: 'trace', label: 'Traitor Trace', icon: Users },
];

export default function FingerprintPage() {
  const [tab, setTab] = useState('embed');

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-violet-glow/30 bg-violet-soft shrink-0">
          <Fingerprint size={22} className="text-violet-glow" />
        </div>
        <div>
          <h2 className="font-display font-semibold text-2xl">Secret Fingerprint</h2>
          <p className="text-ink-dim mt-1">
            Burn a steganographic watermark into your asset, verify whether a file has been tampered
            with, or trace a leaked draft back to the recipient who leaked it.
          </p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {TABS.map((t) => {
          const Icon = t.icon;
          return (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex items-center gap-2 mono-label text-[11px] px-4 py-2.5 rounded-full border transition-colors ${
                tab === t.id
                  ? 'border-violet-glow/40 bg-violet-soft text-violet-glow'
                  : 'border-void-border text-ink-faint hover:text-ink-dim'
              }`}
            >
              <Icon size={14} />
              {t.label}
            </button>
          );
        })}
      </div>

      {tab === 'embed' && <EmbedTab />}
      {tab === 'verify' && <VerifyTab />}
      {tab === 'trace' && <TraceTab />}
    </div>
  );
}

function EmbedTab() {
  const [file, setFile] = useState(null);
  const [signature, setSignature] = useState('');
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');
  const [resultUrl, setResultUrl] = useState(null);

  async function handleEmbed() {
    if (!file || !signature) return;
    setStatus('loading');
    setMessage('Embedding LSB watermark...');
    try {
      const blob = await embedWatermark(file, signature);
      setResultUrl(URL.createObjectURL(blob));
      setStatus('success');
      setMessage('Watermark embedded. Visually identical, cryptographically signed.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the Cybersecurity backend on localhost:8001.');
    }
  }

  function reset() {
    setFile(null);
    setSignature('');
    setStatus(null);
    setResultUrl(null);
  }

  return (
    <Panel eyebrow="Embed" title="Sign an asset with your ownership watermark">
      <div className="space-y-5">
        <Dropzone accept="image/*" file={file} onFileSelected={(f) => { setFile(f); setStatus(null); setResultUrl(null); }} label="Drop a PNG or JPG to watermark" />

        <div>
          <label className="block mono-label text-[10px] text-ink-faint mb-2">Ownership signature</label>
          <input
            type="text"
            value={signature}
            onChange={(e) => setSignature(e.target.value)}
            placeholder="e.g. ONYX_OWNER_001"
            className="w-full px-4 py-3 rounded-lg bg-void-deep border border-void-border text-ink placeholder:text-ink-faint focus:outline-none focus:border-violet-glow/50 focus:ring-1 focus:ring-violet-glow/30 transition-colors"
          />
        </div>

        <StatusBanner state={status} message={message} />

        {!resultUrl ? (
          <PrimaryButton onClick={handleEmbed} disabled={!file || !signature || status === 'loading'} icon={KeyRound}>
            {status === 'loading' ? 'Embedding...' : 'Embed watermark'}
          </PrimaryButton>
        ) : (
          <div className="flex flex-wrap gap-3">
            <SecondaryButton href={resultUrl} icon={Download}>Download watermarked file</SecondaryButton>
            <SecondaryButton onClick={reset} icon={RotateCcw}>Start over</SecondaryButton>
          </div>
        )}

        <p className="text-xs text-ink-faint">
          Calls <code className="text-violet-glow">POST /embed-watermark</code> on localhost:8001.
        </p>
      </div>
    </Panel>
  );
}

function VerifyTab() {
  const [original, setOriginal] = useState(null);
  const [suspect, setSuspect] = useState(null);
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);

  async function handleVerify() {
    if (!original || !suspect) return;
    setStatus('loading');
    setMessage('Comparing watermark integrity...');
    setResult(null);
    try {
      const data = await verifyIntegrity(original, suspect);
      setResult(data);
      setStatus('success');
      setMessage('Scan complete.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the Cybersecurity backend on localhost:8001.');
    }
  }

  function reset() {
    setOriginal(null);
    setSuspect(null);
    setStatus(null);
    setResult(null);
  }

  return (
    <Panel eyebrow="Verify" title="Check whether a file has been altered">
      <div className="space-y-5">
        <div className="grid sm:grid-cols-2 gap-4">
          <div>
            <label className="block mono-label text-[10px] text-ink-faint mb-2">Original watermarked file</label>
            <Dropzone accept="image/*" file={original} onFileSelected={(f) => { setOriginal(f); setStatus(null); setResult(null); }} label="Drop the original" />
          </div>
          <div>
            <label className="block mono-label text-[10px] text-ink-faint mb-2">File to check</label>
            <Dropzone accept="image/*" file={suspect} onFileSelected={(f) => { setSuspect(f); setStatus(null); setResult(null); }} label="Drop the suspect file" />
          </div>
        </div>

        <StatusBanner state={status} message={message} />

        {result && (
          <div className={`rounded-xl border px-5 py-4 ${result.status === 'AUTHENTIC' ? 'border-cyan-glow/30 bg-cyan-soft' : 'border-alert-red/30 bg-alert-soft'}`}>
            <div className={`flex items-center gap-2 font-semibold text-sm mb-2 ${result.status === 'AUTHENTIC' ? 'text-cyan-glow' : 'text-alert-red'}`}>
              {result.status === 'AUTHENTIC' ? <CheckCircle2 size={16} /> : <AlertTriangle size={16} />}
              {result.status}
            </div>
            <p className="text-sm text-ink-dim">{result.message}</p>
            {result.tampered_regions?.length > 0 && (
              <div className="mt-3 font-mono text-xs text-alert-red space-y-1">
                {result.tampered_regions.map((r, i) => (
                  <div key={i}>region {i + 1}: x:{r.x} y:{r.y}, {r.width}×{r.height}px</div>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          {!result ? (
            <PrimaryButton onClick={handleVerify} disabled={!original || !suspect || status === 'loading'} icon={ScanSearch}>
              {status === 'loading' ? 'Scanning...' : 'Verify integrity'}
            </PrimaryButton>
          ) : (
            <SecondaryButton onClick={reset} icon={RotateCcw}>Check another pair</SecondaryButton>
          )}
        </div>

        <p className="text-xs text-ink-faint">
          Calls <code className="text-violet-glow">POST /verify-integrity</code> on localhost:8001.
        </p>
      </div>
    </Panel>
  );
}

function TraceTab() {
  const [mode, setMode] = useState('generate');
  const [file, setFile] = useState(null);
  const [recipient, setRecipient] = useState('');
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');
  const [resultUrl, setResultUrl] = useState(null);
  const [traceResult, setTraceResult] = useState(null);

  async function handleGenerate() {
    if (!file || !recipient) return;
    setStatus('loading');
    setMessage('Generating per-recipient watermarked copy...');
    try {
      const blob = await generateRecipientCopy(file, recipient);
      setResultUrl(URL.createObjectURL(blob));
      setStatus('success');
      setMessage(`Unique copy generated for ${recipient}.`);
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the Cybersecurity backend on localhost:8001.');
    }
  }

  async function handleTrace() {
    if (!file) return;
    setStatus('loading');
    setMessage('Decoding leaked payload...');
    setTraceResult(null);
    try {
      const data = await traceLeak(file);
      setTraceResult(data);
      setStatus('success');
      setMessage('Trace complete.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the Cybersecurity backend on localhost:8001.');
    }
  }

  function reset() {
    setFile(null);
    setRecipient('');
    setStatus(null);
    setResultUrl(null);
    setTraceResult(null);
  }

  return (
    <Panel eyebrow="Traitor Trace" title="Share safely, find leaks instantly">
      <div className="flex gap-2 mb-6">
        {[
          { id: 'generate', label: 'Generate recipient copy' },
          { id: 'trace', label: 'Trace a leaked file' },
        ].map((m) => (
          <button
            key={m.id}
            onClick={() => { setMode(m.id); reset(); }}
            className={`mono-label text-[10px] px-3.5 py-2 rounded-full border transition-colors ${
              mode === m.id ? 'border-violet-glow/40 bg-violet-soft text-violet-glow' : 'border-void-border text-ink-faint'
            }`}
          >
            {m.label}
          </button>
        ))}
      </div>

      {mode === 'generate' ? (
        <div className="space-y-5">
          <Dropzone accept="image/*" file={file} onFileSelected={(f) => { setFile(f); setStatus(null); setResultUrl(null); }} label="Drop the draft to share" />
          <div>
            <label className="block mono-label text-[10px] text-ink-faint mb-2">Recipient name or ID</label>
            <input
              type="text"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              placeholder="e.g. Agency_A"
              className="w-full px-4 py-3 rounded-lg bg-void-deep border border-void-border text-ink placeholder:text-ink-faint focus:outline-none focus:border-violet-glow/50 focus:ring-1 focus:ring-violet-glow/30 transition-colors"
            />
          </div>

          <StatusBanner state={status} message={message} />

          {!resultUrl ? (
            <PrimaryButton onClick={handleGenerate} disabled={!file || !recipient || status === 'loading'} icon={Users}>
              {status === 'loading' ? 'Generating...' : 'Generate recipient copy'}
            </PrimaryButton>
          ) : (
            <div className="flex flex-wrap gap-3">
              <SecondaryButton href={resultUrl} icon={Download}>Download copy for {recipient}</SecondaryButton>
              <SecondaryButton onClick={reset} icon={RotateCcw}>Generate another</SecondaryButton>
            </div>
          )}
          <p className="text-xs text-ink-faint">
            Calls <code className="text-violet-glow">POST /generate-recipient-copy</code> on localhost:8001.
          </p>
        </div>
      ) : (
        <div className="space-y-5">
          <Dropzone accept="image/*" file={file} onFileSelected={(f) => { setFile(f); setStatus(null); setTraceResult(null); }} label="Drop the leaked file" />

          <StatusBanner state={status} message={message} />

          {traceResult && (
            <div className="rounded-xl border border-violet-glow/30 bg-violet-soft px-5 py-4">
              {traceResult.recipient ? (
                <p className="text-sm">
                  Source identified: <span className="font-mono text-violet-glow">{traceResult.recipient}</span>
                </p>
              ) : (
                <p className="text-sm text-ink-dim">{traceResult.message || 'Payload unrecognised.'}</p>
              )}
            </div>
          )}

          <div className="flex flex-wrap gap-3">
            {!traceResult ? (
              <PrimaryButton onClick={handleTrace} disabled={!file || status === 'loading'} icon={ScanSearch}>
                {status === 'loading' ? 'Tracing...' : 'Trace leak source'}
              </PrimaryButton>
            ) : (
              <SecondaryButton onClick={reset} icon={RotateCcw}>Trace another file</SecondaryButton>
            )}
          </div>
          <p className="text-xs text-ink-faint">
            Calls <code className="text-violet-glow">POST /trace-leak</code> on localhost:8001.
          </p>
        </div>
      )}
    </Panel>
  );
}
