import React, { useState, useEffect, useRef } from 'react';

const LOG_LINES = [
  { tag: 'ML_ENGINE', text: 'Generating adversarial noise mask...', color: 'cyan' },
  { tag: 'ML_ENGINE', text: 'PGD optimization — step 40/40 complete', color: 'cyan' },
  { tag: 'CYBER_CORE', text: 'Embedding cryptographic watermark...', color: 'violet' },
  { tag: 'CYBER_CORE', text: 'SHA-256 signature bound to asset', color: 'violet' },
  { tag: 'ACOUSTIC', text: 'Injecting ultrasonic poison layer...', color: 'cyan' },
  { tag: 'ACOUSTIC', text: 'Frequency band 19.2kHz — corrupted', color: 'cyan' },
  { tag: 'TRENDRADAR', text: 'Scanning 14 platforms for velocity spikes', color: 'violet' },
  { tag: 'STATUS', text: 'Identity Shield — 100% active', color: 'success' },
];

export default function TerminalFeed() {
  const [lines, setLines] = useState([]);
  const idxRef = useRef(0);
  const containerRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setLines((prev) => {
        const next = [...prev, { ...LOG_LINES[idxRef.current % LOG_LINES.length], id: Date.now() }];
        idxRef.current += 1;
        return next.slice(-7);
      });
    }, 1100);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [lines]);

  const colorMap = {
    cyan: 'text-cyan-glow',
    violet: 'text-violet-glow',
    success: 'text-cyan-glow'
  };

  return (
    <div className="rounded-xl border border-void-border bg-void-deep/80 overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-2.5 border-b border-void-border bg-white/[0.02]">
        <span className="w-2.5 h-2.5 rounded-full bg-alert-red/70" />
        <span className="w-2.5 h-2.5 rounded-full bg-cyan-glow/40" />
        <span className="w-2.5 h-2.5 rounded-full bg-violet-glow/50" />
        <span className="ml-2 mono-label text-[10px] text-ink-faint">onyx_diagnostic.feed</span>
      </div>
      <div ref={containerRef} className="h-44 overflow-hidden px-4 py-3 font-mono text-[12px] leading-relaxed">
        {lines.map((line) => (
          <div key={line.id} className="flex gap-2 animate-[fadeIn_0.3s_ease]">
            <span className={`${colorMap[line.color]} shrink-0`}>[{line.tag}]</span>
            <span className="text-ink-dim">{line.text}</span>
          </div>
        ))}
        <div className="flex gap-2 mt-1">
          <span className="text-cyan-glow animate-pulse">█</span>
        </div>
      </div>
    </div>
  );
}
