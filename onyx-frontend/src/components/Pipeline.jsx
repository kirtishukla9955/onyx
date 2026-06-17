import React from 'react';
import { motion } from 'framer-motion';
import { Upload, ScanFace, KeyRound, MonitorCheck } from 'lucide-react';

const STEPS = [
  { icon: Upload, title: 'Raw Asset In', desc: 'A photo, video, or audio file enters the pipeline untouched.' },
  { icon: ScanFace, title: 'Adversarial Noise', desc: 'PGD optimization scrambles the facial and vocal embedding space.' },
  { icon: KeyRound, title: 'Watermark Burned', desc: 'A steganographic signature is signed into pixels and frequencies.' },
  { icon: MonitorCheck, title: 'Cloaked Asset Out', desc: 'Identical to the eye and ear. Unusable to any model that steals it.' },
];

export default function Pipeline() {
  return (
    <section id="pipeline" className="relative py-28 px-6 lg:px-10 bg-void-deep/40">
      <div className="absolute inset-0 grid-bg opacity-30" />
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mb-16"
        >
          <span className="mono-label text-[11px] text-cyan-glow">The Pipeline</span>
          <h2 className="font-display font-semibold text-4xl lg:text-5xl mt-3 leading-tight">
            Zero-Trust Media Processing
          </h2>
          <p className="text-ink-dim text-lg mt-4 leading-relaxed">
            Every asset moves through the same four-stage gauntlet before it's cleared to post.
          </p>
        </motion.div>

        <div className="relative grid md:grid-cols-4 gap-6">
          {/* connecting line */}
          <div className="hidden md:block absolute top-8 left-[12%] right-[12%] h-px bg-gradient-to-r from-cyan-glow/0 via-cyan-glow/40 to-cyan-glow/0" />

          {STEPS.map((step, i) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 24 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.12 }}
                className="relative flex flex-col items-center text-center"
              >
                <div className="relative mb-5">
                  <div className="absolute inset-0 rounded-full bg-cyan-glow/15 blur-xl" />
                  <div className="relative w-16 h-16 rounded-full border border-cyan-glow/30 bg-void-panel flex items-center justify-center">
                    <Icon size={24} className="text-cyan-glow" />
                  </div>
                  <span className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-void-deep border border-void-border flex items-center justify-center mono-label text-[10px] text-ink-dim">
                    {i + 1}
                  </span>
                </div>
                <h3 className="font-display font-semibold text-lg mb-2">{step.title}</h3>
                <p className="text-ink-dim text-sm leading-relaxed">{step.desc}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
