import React from 'react';
import { motion } from 'framer-motion';
import { Radar, Eye, Fingerprint, Volume2 } from 'lucide-react';

const FEATURES = [
  {
    icon: Radar,
    eyebrow: 'PREDICT',
    title: 'TrendRadar',
    desc: "Scans emerging audio, hashtags, and formats across platforms and surfaces what's about to peak — 48 hours before it does. Every alert comes with a niche-specific way to adapt it.",
    color: 'violet',
    stat: '48HRS',
    statLabel: 'early warning',
  },
  {
    icon: Eye,
    eyebrow: 'SHIELD',
    title: 'Digital Camouflage',
    desc: 'Injects an invisible adversarial perturbation across facial regions before you post. Looks completely normal to a viewer. Scrambles the embedding space for any AI trying to clone it.',
    color: 'cyan',
    stat: '0%',
    statLabel: 'visible change',
  },
  {
    icon: Fingerprint,
    eyebrow: 'PROVE',
    title: 'Secret Fingerprint',
    desc: 'Burns a steganographic watermark into pixels and audio frames. Verify authenticity on demand, trace exactly which frame was altered, and identify which recipient leaked a draft.',
    color: 'violet',
    stat: '256-BIT',
    statLabel: 'signature strength',
  },
  {
    icon: Volume2,
    eyebrow: 'SHIELD',
    title: 'Acoustic Poisoning',
    desc: 'Sub-audible, ultrasonic noise rides inside your audio track — inaudible to people, toxic to voice-cloning models. Rip it for training data and the clone comes out broken.',
    color: 'cyan',
    stat: '19kHz+',
    statLabel: 'poison frequency',
  },
];

export default function Features() {
  return (
    <section id="features" className="relative py-28 px-6 lg:px-10">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mb-16"
        >
          <span className="mono-label text-[11px] text-cyan-glow">The Shield</span>
          <h2 className="font-display font-semibold text-4xl lg:text-5xl mt-3 leading-tight">
            Four engines. One pipeline.
          </h2>
          <p className="text-ink-dim text-lg mt-4 leading-relaxed">
            ONYX runs every asset through adversarial ML and cryptographic provenance before it
            ever reaches a platform — protecting the face, the voice, and the proof of ownership.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-5">
          {FEATURES.map((f, i) => {
            const Icon = f.icon;
            const isCyan = f.color === 'cyan';
            return (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.55, delay: i * 0.08 }}
                className="group relative gradient-border rounded-2xl bg-void-panel p-8 overflow-hidden hover:bg-void-card transition-colors"
              >
                <div
                  className={`absolute -top-20 -right-20 w-56 h-56 rounded-full blur-[80px] opacity-0 group-hover:opacity-100 transition-opacity duration-500 ${
                    isCyan ? 'bg-cyan-glow/20' : 'bg-violet-glow/20'
                  }`}
                />
                <div className="relative flex items-start justify-between mb-6">
                  <div
                    className={`w-12 h-12 rounded-xl flex items-center justify-center border ${
                      isCyan ? 'border-cyan-glow/30 bg-cyan-soft' : 'border-violet-glow/30 bg-violet-soft'
                    }`}
                  >
                    <Icon size={22} className={isCyan ? 'text-cyan-glow' : 'text-violet-glow'} />
                  </div>
                  <div className="text-right">
                    <div className={`font-mono text-xl font-semibold ${isCyan ? 'text-cyan-glow' : 'text-violet-glow'}`}>
                      {f.stat}
                    </div>
                    <div className="mono-label text-[9px] text-ink-faint">{f.statLabel}</div>
                  </div>
                </div>

                <span className="mono-label text-[10px] text-ink-faint">{f.eyebrow}</span>
                <h3 className="font-display font-semibold text-2xl mt-1.5 mb-3">{f.title}</h3>
                <p className="text-ink-dim leading-relaxed">{f.desc}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
