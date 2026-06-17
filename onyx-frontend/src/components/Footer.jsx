import React from 'react';

export default function Footer() {
  return (
    <footer className="relative border-t border-void-border px-6 lg:px-10 py-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-8 mb-10">
          <div className="flex items-center gap-2.5">
            <svg viewBox="0 0 32 32" className="w-7 h-7">
              <polygon points="16,2 30,9 30,23 16,30 2,23 2,9" fill="none" stroke="#00F0FF" strokeWidth="1.5" />
              <polygon points="16,9 23,12.5 23,19.5 16,23 9,19.5 9,12.5" fill="#00F0FF" opacity="0.15" stroke="#00F0FF" strokeWidth="1" />
            </svg>
            <span className="font-display font-semibold text-lg">ONYX</span>
          </div>
          <div className="flex flex-wrap gap-8">
            {['Shield', 'Pipeline', 'Proof', 'Pricing', 'Docs'].map((l) => (
              <a key={l} href="#" className="mono-label text-[11px] text-ink-faint hover:text-cyan-glow transition-colors">
                {l}
              </a>
            ))}
          </div>
        </div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-8 border-t border-void-border">
          <p className="text-ink-faint text-sm">
            ONYX. Protect before you post. Predict before you publish.
          </p>
          <p className="mono-label text-[10px] text-ink-faint">© 2025 ONYX. All assets cloaked.</p>
        </div>
      </div>
    </footer>
  );
}
