import React from 'react';

const items = [
  'PGD ADVERSARIAL OPTIMIZATION', 'LSB STEGANOGRAPHY', 'SHA-256 PROVENANCE',
  'ULTRASONIC POISONING', 'FACE EMBEDDING DEFENSE', 'TREND VELOCITY SCORING',
];

export default function TrustStrip() {
  const loop = [...items, ...items];
  return (
    <div className="border-y border-void-border bg-void-panel/50 py-5 overflow-hidden">
      <div className="flex w-max animate-marquee">
        {loop.map((item, i) => (
          <div key={i} className="flex items-center gap-3 mx-8">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-glow/60" />
            <span className="mono-label text-[11px] text-ink-faint whitespace-nowrap">{item}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
