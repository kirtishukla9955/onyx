import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Check, AlertTriangle, ScanLine } from 'lucide-react';

export default function Proof() {
  const [tab, setTab] = useState('watermark');

  return (
    <section id="proof" className="relative py-28 px-6 lg:px-10">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-2xl mb-12"
        >
          <span className="mono-label text-[11px] text-cyan-glow">The Proof</span>
          <h2 className="font-display font-semibold text-4xl lg:text-5xl mt-3 leading-tight">
            It doesn't just claim to work.
          </h2>
          <p className="text-ink-dim text-lg mt-4 leading-relaxed">
            Run the same file through detection before and after ONYX. The difference is the product.
          </p>
        </motion.div>

        <div className="flex gap-2 mb-8">
          {[
            { id: 'watermark', label: 'Tamper Detection' },
            { id: 'face', label: 'Face Detection' },
          ].map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`mono-label text-[11px] px-4 py-2 rounded-full border transition-colors ${
                tab === t.id
                  ? 'border-cyan-glow/40 bg-cyan-soft text-cyan-glow'
                  : 'border-void-border text-ink-faint hover:text-ink-dim'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === 'watermark' ? (
          <div className="grid md:grid-cols-2 gap-5">
            <ProofCard
              status="authentic"
              title="Original File"
              subtitle="watermark_check.scan"
              lines={[
                'Reading steganographic payload...',
                'Signature hash matched: 9f3a...e21c',
                'Cross-referencing frame integrity...',
                'No deviation across 1,920 frames',
              ]}
            />
            <ProofCard
              status="tampered"
              title="Edited File"
              subtitle="watermark_check.scan"
              lines={[
                'Reading steganographic payload...',
                'Signature hash mismatch detected',
                'Locating divergent region...',
                'Tamper isolated: x:412 y:188, 64×64px',
              ]}
            />
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-5">
            <ProofCard
              status="tracked"
              title="Raw Upload"
              subtitle="face_detect.scan"
              lines={[
                'Loading detection model...',
                'Face located: confidence 0.99',
                'Landmark mesh: 468 points mapped',
                'Embedding extracted successfully',
              ]}
            />
            <ProofCard
              status="blind"
              title="Cloaked Upload"
              subtitle="face_detect.scan"
              lines={[
                'Loading detection model...',
                'Face located: confidence 0.11',
                'Landmark mesh: failed to converge',
                'Embedding extraction aborted',
              ]}
            />
          </div>
        )}
      </div>
    </section>
  );
}

function ProofCard({ status, title, subtitle, lines }) {
  const isGood = status === 'authentic' || status === 'tracked';
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className="gradient-border rounded-2xl bg-void-panel overflow-hidden"
    >
      <div className="flex items-center justify-between px-6 py-4 border-b border-void-border">
        <div>
          <h4 className="font-display font-semibold text-lg">{title}</h4>
          <span className="mono-label text-[10px] text-ink-faint">{subtitle}</span>
        </div>
        <div
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[11px] font-semibold ${
            isGood ? 'bg-cyan-soft text-cyan-glow' : 'bg-alert-soft text-alert-red'
          }`}
        >
          {isGood ? <Check size={13} /> : <AlertTriangle size={13} />}
          {status.toUpperCase()}
        </div>
      </div>
      <div className="p-6 font-mono text-[13px] space-y-2.5">
        {lines.map((line, i) => (
          <div key={i} className="flex items-start gap-2.5">
            <ScanLine size={14} className={`mt-0.5 shrink-0 ${isGood ? 'text-cyan-glow/60' : 'text-alert-red/70'}`} />
            <span className="text-ink-dim">{line}</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
