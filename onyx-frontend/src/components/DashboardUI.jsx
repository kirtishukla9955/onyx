import React from 'react';
import { AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';

export function Panel({ title, eyebrow, children, className = '' }) {
  return (
    <div className={`gradient-border rounded-2xl bg-void-panel p-6 lg:p-8 ${className}`}>
      {(title || eyebrow) && (
        <div className="mb-6">
          {eyebrow && <span className="mono-label text-[10px] text-cyan-glow">{eyebrow}</span>}
          {title && <h2 className="font-display font-semibold text-xl mt-1">{title}</h2>}
        </div>
      )}
      {children}
    </div>
  );
}

export function StatusBanner({ state, message }) {
  if (!state) return null;

  const config = {
    loading: { icon: Loader2, classes: 'text-cyan-glow bg-cyan-soft border-cyan-glow/30', spin: true },
    success: { icon: CheckCircle2, classes: 'text-cyan-glow bg-cyan-soft border-cyan-glow/30' },
    error: { icon: AlertCircle, classes: 'text-alert-red bg-alert-soft border-alert-red/30' },
  }[state];

  const Icon = config.icon;

  return (
    <div className={`flex items-center gap-2.5 rounded-lg border px-4 py-3 text-sm mb-5 ${config.classes}`}>
      <Icon size={16} className={config.spin ? 'animate-spin' : ''} />
      {message}
    </div>
  );
}

export function PrimaryButton({ children, onClick, disabled, type = 'button', icon: Icon }) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className="shine group flex items-center justify-center gap-2 px-6 py-3 rounded-full bg-cyan-glow text-void-deep font-semibold text-sm hover:shadow-[0_0_24px_rgba(0,240,255,0.5)] transition-shadow disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
    >
      {Icon && <Icon size={16} />}
      {children}
    </button>
  );
}

export function SecondaryButton({ children, onClick, disabled, icon: Icon, href }) {
  const classes = "flex items-center justify-center gap-2 px-6 py-3 rounded-full border border-void-border text-ink text-sm font-medium hover:border-cyan-glow/40 hover:text-cyan-glow transition-colors disabled:opacity-50 disabled:cursor-not-allowed";
  if (href) {
    return (
      <a href={href} download className={classes}>
        {Icon && <Icon size={16} />}
        {children}
      </a>
    );
  }
  return (
    <button onClick={onClick} disabled={disabled} className={classes}>
      {Icon && <Icon size={16} />}
      {children}
    </button>
  );
}
