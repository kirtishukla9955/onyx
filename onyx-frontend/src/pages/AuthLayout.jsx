import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import FaceScrambleCanvas from '../components/FaceScrambleCanvas';

export default function AuthLayout({ title, subtitle, children, footer }) {
  return (
    <div className="min-h-screen bg-void grid lg:grid-cols-2">
      {/* Left: form */}
      <div className="flex flex-col justify-center px-6 sm:px-12 lg:px-20 py-12 relative">
        <div className="absolute inset-0 grid-bg opacity-30" />
        <Link to="/" className="relative flex items-center gap-2.5 mb-12 w-fit">
          <svg viewBox="0 0 32 32" className="w-8 h-8">
            <polygon points="16,2 30,9 30,23 16,30 2,23 2,9" fill="none" stroke="#00F0FF" strokeWidth="1.5" />
            <polygon points="16,9 23,12.5 23,19.5 16,23 9,19.5 9,12.5" fill="#00F0FF" opacity="0.15" stroke="#00F0FF" strokeWidth="1" />
          </svg>
          <span className="font-display font-semibold text-xl">ONYX</span>
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="relative max-w-sm w-full mx-auto"
        >
          <h1 className="font-display font-semibold text-3xl mb-2">{title}</h1>
          <p className="text-ink-dim text-sm mb-8">{subtitle}</p>
          {children}
          {footer && <div className="mt-8 text-center text-sm text-ink-dim">{footer}</div>}
        </motion.div>
      </div>

      {/* Right: visual */}
      <div className="hidden lg:block relative border-l border-void-border overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-soft via-void-panel to-violet-soft" />
        <FaceScrambleCanvas />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-12">
          <span className="mono-label text-[11px] text-cyan-glow mb-4 px-3 py-1.5 rounded-full border border-cyan-glow/30 bg-void-deep/60">
            IDENTITY SHIELD ACTIVE
          </span>
          <h2 className="font-display font-semibold text-3xl max-w-sm leading-tight">
            Protect before you post.
            <br />
            Predict before you publish.
          </h2>
        </div>
      </div>
    </div>
  );
}
