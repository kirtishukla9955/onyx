import React, { useState } from 'react';
import { Radar, TrendingUp, TrendingDown, RefreshCw } from 'lucide-react';
import { Panel, StatusBanner, PrimaryButton } from '../components/DashboardUI';
import { getTrending, getTrendingByNiche, getTrendExpiry } from '../api/trend';

const NICHES = ['All', 'Fitness', 'Food', 'Beauty', 'Tech', 'Music', 'Comedy'];

export default function TrendRadar() {
  const [niche, setNiche] = useState('All');
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');
  const [trending, setTrending] = useState(null);
  const [expiring, setExpiring] = useState(null);

  async function loadTrends() {
    setStatus('loading');
    setMessage('Scanning platforms for velocity spikes...');
    try {
      const data = niche === 'All' ? await getTrending() : await getTrendingByNiche(niche.toLowerCase());
      const expiry = await getTrendExpiry();
      setTrending(Array.isArray(data) ? data : data.trends || []);
      setExpiring(Array.isArray(expiry) ? expiry : expiry.trends || []);
      setStatus('success');
      setMessage('TrendRadar updated.');
    } catch (err) {
      setStatus('error');
      setMessage(err.message || 'Could not reach the Trend Engine on localhost:8003. Is it running?');
      setTrending(null);
      setExpiring(null);
    }
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-violet-glow/30 bg-violet-soft shrink-0">
          <Radar size={22} className="text-violet-glow" />
        </div>
        <div>
          <h2 className="font-display font-semibold text-2xl">TrendRadar</h2>
          <p className="text-ink-dim mt-1">
            Predicted trends 48 hours before they peak, with a heads-up on what's about to die so you
            don't post into a dead wave.
          </p>
        </div>
      </div>

      <Panel eyebrow="Filter" title="Choose your niche">
        <div className="flex flex-wrap gap-2 mb-6">
          {NICHES.map((n) => (
            <button
              key={n}
              onClick={() => setNiche(n)}
              className={`mono-label text-[10px] px-3.5 py-2 rounded-full border transition-colors ${
                niche === n ? 'border-violet-glow/40 bg-violet-soft text-violet-glow' : 'border-void-border text-ink-faint'
              }`}
            >
              {n}
            </button>
          ))}
        </div>

        <StatusBanner state={status} message={message} />

        <PrimaryButton onClick={loadTrends} disabled={status === 'loading'} icon={RefreshCw}>
          {status === 'loading' ? 'Scanning...' : 'Scan for trends'}
        </PrimaryButton>

        <p className="text-xs text-ink-faint mt-4">
          Calls <code className="text-violet-glow">GET /trending</code> and{' '}
          <code className="text-violet-glow">/trend-expiry</code> on localhost:8003.
        </p>
      </Panel>

      {trending && (
        <Panel eyebrow="Rising" title="About to peak">
          {trending.length === 0 ? (
            <EmptyState text="No rising trends returned for this niche yet." />
          ) : (
            <div className="space-y-3">
              {trending.map((t, i) => (
                <TrendRow key={i} trend={t} direction="up" />
              ))}
            </div>
          )}
        </Panel>
      )}

      {expiring && (
        <Panel eyebrow="Expiring" title="About to die">
          {expiring.length === 0 ? (
            <EmptyState text="Nothing flagged as expiring right now." />
          ) : (
            <div className="space-y-3">
              {expiring.map((t, i) => (
                <TrendRow key={i} trend={t} direction="down" />
              ))}
            </div>
          )}
        </Panel>
      )}
    </div>
  );
}

function TrendRow({ trend, direction }) {
  const isUp = direction === 'up';
  const label = trend.name || trend.hashtag || trend.title || JSON.stringify(trend);
  return (
    <div className="flex items-center justify-between rounded-lg border border-void-border bg-void-deep/60 px-4 py-3">
      <div className="flex items-center gap-3">
        {isUp ? <TrendingUp size={16} className="text-cyan-glow" /> : <TrendingDown size={16} className="text-alert-red" />}
        <span className="text-sm">{label}</span>
      </div>
      {trend.score && (
        <span className="font-mono text-xs text-ink-faint">{trend.score}</span>
      )}
    </div>
  );
}

function EmptyState({ text }) {
  return (
    <div className="text-center py-8">
      <p className="text-ink-dim text-sm">{text}</p>
    </div>
  );
}
