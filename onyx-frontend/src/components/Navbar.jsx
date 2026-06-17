import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { label: 'Shield', href: '#features' },
    { label: 'Pipeline', href: '#pipeline' },
    { label: 'Proof', href: '#proof' },
    { label: 'Pricing', href: '#pricing' },
  ];

  return (
    <motion.header
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-void/80 backdrop-blur-xl border-b border-void-border' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 lg:px-10 h-[72px] flex items-center justify-between">
        <a href="#top" className="flex items-center gap-2.5 group">
          <div className="relative w-8 h-8">
            <div className="absolute inset-0 rounded-md bg-cyan-glow/20 blur-md group-hover:bg-cyan-glow/40 transition-all" />
            <svg viewBox="0 0 32 32" className="relative w-8 h-8">
              <polygon points="16,2 30,9 30,23 16,30 2,23 2,9" fill="none" stroke="#00F0FF" strokeWidth="1.5" />
              <polygon points="16,9 23,12.5 23,19.5 16,23 9,19.5 9,12.5" fill="#00F0FF" opacity="0.15" stroke="#00F0FF" strokeWidth="1" />
            </svg>
          </div>
          <span className="font-display font-semibold text-xl tracking-wide text-ink">ONYX</span>
        </a>

        <nav className="hidden lg:flex items-center gap-9">
          {links.map((l) => (
            <a
              key={l.label}
              href={l.href}
              className="mono-label text-[11px] text-ink-dim hover:text-cyan-glow transition-colors"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="hidden lg:flex items-center gap-4">
          <Link to="/login" className="mono-label text-[11px] text-ink-dim hover:text-ink transition-colors">
            Sign in
          </Link>
          <Link
            to="/signup"
            className="shine relative px-5 py-2.5 rounded-full bg-cyan-glow text-void-deep font-semibold text-sm hover:shadow-[0_0_24px_rgba(0,240,255,0.5)] transition-shadow"
          >
            Get Protected
          </Link>
        </div>

        <button onClick={() => setOpen(!open)} className="lg:hidden text-ink">
          {open ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {open && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="lg:hidden bg-void-panel border-t border-void-border px-6 py-6 flex flex-col gap-5"
        >
          {links.map((l) => (
            <a key={l.label} href={l.href} onClick={() => setOpen(false)} className="mono-label text-sm text-ink-dim">
              {l.label}
            </a>
          ))}
          <Link to="/signup" onClick={() => setOpen(false)} className="px-5 py-3 rounded-full bg-cyan-glow text-void-deep font-semibold text-sm text-center">
            Get Protected
          </Link>
        </motion.div>
      )}
    </motion.header>
  );
}
