import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Check } from 'lucide-react';

const PLANS = [
  {
    name: 'Creator',
    price: '0',
    desc: 'For individuals getting started with protection.',
    features: ['Watermarking only', '10 assets / month', 'Basic authenticity check', 'Community support'],
    cta: 'Start free',
    highlight: false,
  },
  {
    name: 'Shield Pro',
    price: '29',
    desc: 'Full protection for working creators.',
    features: [
      'Digital Camouflage + Acoustic Poisoning',
      'Unlimited asset processing',
      'Traitor tracing for drafts',
      'TrendRadar alerts (your niche)',
      'Priority support',
    ],
    cta: 'Get Shield Pro',
    highlight: true,
  },
  {
    name: 'Agency',
    price: 'Custom',
    desc: 'White-labeled infrastructure for talent networks.',
    features: [
      'Everything in Shield Pro',
      'Verification API access',
      'Multi-seat team management',
      'Custom watermark policy',
      'Dedicated integration support',
    ],
    cta: 'Talk to us',
    highlight: false,
  },
];

export default function Pricing() {
  return (
    <section id="pricing" className="relative py-28 px-6 lg:px-10 bg-void-deep/40">
      <div className="absolute inset-0 grid-bg opacity-30" />
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-2xl mx-auto mb-16"
        >
          <span className="mono-label text-[11px] text-cyan-glow">Pricing</span>
          <h2 className="font-display font-semibold text-4xl lg:text-5xl mt-3 leading-tight">
            Protection scales with you.
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 items-stretch">
          {PLANS.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className={`relative rounded-2xl p-8 flex flex-col ${
                plan.highlight
                  ? 'gradient-border bg-void-card scale-[1.02] shadow-[0_0_60px_rgba(0,240,255,0.12)]'
                  : 'border border-void-border bg-void-panel'
              }`}
            >
              {plan.highlight && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 mono-label text-[10px] px-3 py-1 rounded-full bg-cyan-glow text-void-deep font-semibold">
                  MOST PROTECTED
                </span>
              )}
              <h3 className="font-display font-semibold text-2xl">{plan.name}</h3>
              <p className="text-ink-dim text-sm mt-2 mb-6">{plan.desc}</p>
              <div className="flex items-baseline gap-1 mb-6">
                {plan.price !== 'Custom' && <span className="text-2xl text-ink-dim">$</span>}
                <span className="font-display font-semibold text-5xl">{plan.price}</span>
                {plan.price !== 'Custom' && <span className="text-ink-dim text-sm">/mo</span>}
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-ink-dim">
                    <Check size={16} className="text-cyan-glow shrink-0 mt-0.5" />
                    {f}
                  </li>
                ))}
              </ul>
              <Link
                to="/signup"
                className={`shine text-center py-3 rounded-full font-semibold text-sm transition-shadow ${
                  plan.highlight
                    ? 'bg-cyan-glow text-void-deep hover:shadow-[0_0_28px_rgba(0,240,255,0.5)]'
                    : 'border border-void-border text-ink hover:border-cyan-glow/40 hover:text-cyan-glow'
                }`}
              >
                {plan.cta}
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
