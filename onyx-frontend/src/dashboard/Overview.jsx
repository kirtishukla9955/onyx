import React from 'react';
import { Link } from 'react-router-dom';
import { Eye, Fingerprint, Volume2, Radar, ArrowRight } from 'lucide-react';
import { Panel } from '../components/DashboardUI';
import TerminalFeed from '../components/TerminalFeed';
import { useAuth } from '../context/AuthContext';

const FEATURE_CARDS = [
  {
    to: '/dashboard/camouflage',
    icon: Eye,
    title: 'Digital Camouflage',
    desc: 'Cloak a photo or video against deepfake training.',
    color: 'cyan',
  },
  {
    to: '/dashboard/fingerprint',
    icon: Fingerprint,
    title: 'Secret Fingerprint',
    desc: 'Watermark, verify, and trace leaked drafts.',
    color: 'violet',
  },
  {
    to: '/dashboard/acoustic',
    icon: Volume2,
    title: 'Acoustic Poisoning',
    desc: 'Poison an audio track against voice cloning.',
    color: 'cyan',
  },
  {
    to: '/dashboard/trendradar',
    icon: Radar,
    title: 'TrendRadar',
    desc: 'See what is about to peak in your niche.',
    color: 'violet',
  },
];

export default function Overview() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      <div>
        <h2 className="font-display font-semibold text-2xl">
          Welcome back, {user?.name?.split(' ')[0] || 'Creator'}.
        </h2>
        <p className="text-ink-dim mt-1">Here's the state of your identity shield.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          ['Assets Protected', '0'],
          ['Visual Shield', 'Ready'],
          ['Voice Shield', 'Ready'],
          ['Watermarks Issued', '0'],
        ].map(([label, val]) => (
          <Panel key={label} className="p-5">
            <div className="mono-label text-[10px] text-ink-faint mb-2">{label}</div>
            <div className="text-2xl font-display font-semibold text-cyan-glow">{val}</div>
          </Panel>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        {FEATURE_CARDS.map((f) => {
          const Icon = f.icon;
          const isCyan = f.color === 'cyan';
          return (
            <Link
              key={f.to}
              to={f.to}
              className="group gradient-border rounded-2xl bg-void-panel p-6 flex items-center justify-between hover:bg-void-card transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center border ${isCyan ? 'border-cyan-glow/30 bg-cyan-soft' : 'border-violet-glow/30 bg-violet-soft'}`}>
                  <Icon size={22} className={isCyan ? 'text-cyan-glow' : 'text-violet-glow'} />
                </div>
                <div>
                  <h3 className="font-display font-semibold">{f.title}</h3>
                  <p className="text-ink-dim text-sm">{f.desc}</p>
                </div>
              </div>
              <ArrowRight size={18} className="text-ink-faint group-hover:text-cyan-glow group-hover:translate-x-1 transition-all shrink-0" />
            </Link>
          );
        })}
      </div>

      <Panel eyebrow="Live" title="Diagnostic Feed">
        <TerminalFeed />
      </Panel>
    </div>
  );
}
