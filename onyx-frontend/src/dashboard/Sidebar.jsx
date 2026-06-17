import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Eye, Fingerprint, Volume2, Radar, Settings, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const NAV_ITEMS = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Overview', end: true },
  { to: '/dashboard/camouflage', icon: Eye, label: 'Digital Camouflage' },
  { to: '/dashboard/fingerprint', icon: Fingerprint, label: 'Secret Fingerprint' },
  { to: '/dashboard/acoustic', icon: Volume2, label: 'Acoustic Poisoning' },
  { to: '/dashboard/trendradar', icon: Radar, label: 'TrendRadar' },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  const initials = (user?.name || 'U')
    .split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  return (
    <aside className="fixed left-0 top-0 h-screen w-[76px] lg:w-64 bg-void-panel border-r border-void-border flex flex-col z-40">
      {/* Logo */}
      <div className="h-[72px] flex items-center justify-center lg:justify-start lg:px-6 border-b border-void-border">
        <svg viewBox="0 0 32 32" className="w-8 h-8 shrink-0">
          <polygon points="16,2 30,9 30,23 16,30 2,23 2,9" fill="none" stroke="#00F0FF" strokeWidth="1.5" />
          <polygon points="16,9 23,12.5 23,19.5 16,23 9,19.5 9,12.5" fill="#00F0FF" opacity="0.15" stroke="#00F0FF" strokeWidth="1" />
        </svg>
        <span className="hidden lg:inline font-display font-semibold text-lg ml-2.5">ONYX</span>
      </div>

      {/* Profile */}
      <div className="px-3 lg:px-6 py-5 border-b border-void-border flex items-center gap-3 justify-center lg:justify-start">
        <div className="w-10 h-10 rounded-full bg-cyan-soft border border-cyan-glow/30 flex items-center justify-center font-mono text-sm text-cyan-glow shrink-0">
          {initials}
        </div>
        <div className="hidden lg:block overflow-hidden">
          <div className="text-sm font-medium truncate">{user?.name || 'Creator'}</div>
          <div className="text-xs text-ink-faint truncate">{user?.email || ''}</div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 lg:px-4 py-5 flex flex-col gap-1.5 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `relative flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors group justify-center lg:justify-start ${
                  isActive
                    ? 'bg-cyan-soft text-cyan-glow'
                    : 'text-ink-dim hover:text-ink hover:bg-white/[0.03]'
                }`
              }
              title={item.label}
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <span className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-cyan-glow rounded-full hidden lg:block" />
                  )}
                  <Icon size={19} className="shrink-0" />
                  <span className="hidden lg:inline text-sm font-medium truncate">{item.label}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Settings + logout */}
      <div className="px-3 lg:px-4 py-4 border-t border-void-border flex flex-col gap-1.5">
        <NavLink
          to="/dashboard/settings"
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors justify-center lg:justify-start ${
              isActive ? 'bg-cyan-soft text-cyan-glow' : 'text-ink-dim hover:text-ink hover:bg-white/[0.03]'
            }`
          }
          title="Settings"
        >
          <Settings size={19} className="shrink-0" />
          <span className="hidden lg:inline text-sm font-medium">Settings</span>
        </NavLink>
        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-ink-dim hover:text-alert-red hover:bg-alert-soft transition-colors justify-center lg:justify-start"
          title="Log out"
        >
          <LogOut size={19} className="shrink-0" />
          <span className="hidden lg:inline text-sm font-medium">Log out</span>
        </button>
      </div>
    </aside>
  );
}
