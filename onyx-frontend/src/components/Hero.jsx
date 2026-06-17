import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import FaceScrambleCanvas from './FaceScrambleCanvas';
import TerminalFeed from './TerminalFeed';

export default function Hero() {
  return (
    <section id="top" className="relative pt-40 pb-24 px-6 lg:px-10 overflow-hidden">
      {/* ambient backdrop */}
      <div className="absolute inset-0 grid-bg opacity-60" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[500px] spotlight" />
      <div className="absolute -top-40 -right-40 w-[500px] h-[500px] bg-violet-glow/10 rounded-full blur-[120px]" />

      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex items-center gap-2 w-fit mx-auto mb-8 px-4 py-1.5 rounded-full border border-cyan-glow/25 bg-cyan-soft"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-glow opacity-60" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-glow" />
          </span>
          <span className="mono-label text-[11px] text-cyan-glow">Adversarial ML &amp; Provenance Engine</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="font-display font-semibold text-center text-[42px] sm:text-[58px] lg:text-[72px] leading-[1.05] tracking-tight max-w-4xl mx-auto"
        >
          Your face is data.
          <br />
          <span className="text-cyan-glow text-glow-cyan">Stop feeding it</span> to the wrong models.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="text-center text-ink-dim text-lg max-w-2xl mx-auto mt-6 leading-relaxed"
        >
          ONYX poisons your photos and audio against deepfake and voice-clone training before you post —
          then proves what's real after you do. Built for creators who refuse to be cloned.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10"
        >
          <Link
            id="cta"
            to="/signup"
            className="shine group flex items-center gap-2 px-7 py-3.5 rounded-full bg-cyan-glow text-void-deep font-semibold hover:shadow-[0_0_32px_rgba(0,240,255,0.55)] transition-shadow"
          >
            Shield Your Identity
            <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
          </Link>
          <a
            href="#proof"
            className="flex items-center gap-2 px-7 py-3.5 rounded-full border border-void-border text-ink hover:border-cyan-glow/40 hover:text-cyan-glow transition-colors"
          >
            <ShieldCheck size={18} />
            See the proof
          </a>
        </motion.div>

        {/* Centerpiece visual panel */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="relative mt-20 gradient-border rounded-2xl overflow-hidden"
        >
          <div className="grid lg:grid-cols-[1.3fr_1fr] bg-void-panel">
            {/* Face scramble visual */}
            <div className="relative h-[420px] lg:h-[480px] border-b lg:border-b-0 lg:border-r border-void-border overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-soft via-transparent to-violet-soft" />
              <FaceScrambleCanvas />
              <div className="absolute top-5 left-5 flex items-center gap-2">
                <span className="mono-label text-[10px] text-cyan-glow px-2.5 py-1 rounded-full border border-cyan-glow/30 bg-void-deep/60">
                  DIGITAL_CAMOUFLAGE.exe
                </span>
              </div>
              <div className="absolute bottom-5 left-5 right-5 flex items-center justify-between">
                <span className="mono-label text-[10px] text-ink-faint">FACE_EMBEDDING_SCRAMBLE</span>
                <span className="mono-label text-[10px] text-cyan-glow">ACTIVE</span>
              </div>
            </div>

            {/* Right panel: status + terminal */}
            <div className="p-6 flex flex-col gap-5 justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="mono-label text-[10px] text-ink-faint">SHIELD STATUS</span>
                  <span className="flex items-center gap-1.5 text-cyan-glow text-xs font-medium">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-glow animate-pulse" />
                    100% ACTIVE
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    ['Visual Shield', '98.4%'],
                    ['Voice Shield', '96.1%'],
                    ['Watermark', 'SIGNED'],
                    ['Trend Scan', 'LIVE'],
                  ].map(([label, val]) => (
                    <div key={label} className="rounded-lg border border-void-border bg-void-deep/60 p-3">
                      <div className="mono-label text-[9px] text-ink-faint mb-1">{label}</div>
                      <div className="text-cyan-glow font-mono text-sm">{val}</div>
                    </div>
                  ))}
                </div>
              </div>
              <TerminalFeed />
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
