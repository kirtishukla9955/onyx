import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';

const TITLES = {
  '/dashboard': 'Overview',
  '/dashboard/camouflage': 'Digital Camouflage',
  '/dashboard/fingerprint': 'Secret Fingerprint',
  '/dashboard/acoustic': 'Acoustic Poisoning',
  '/dashboard/trendradar': 'TrendRadar',
  '/dashboard/settings': 'Settings',
};

export default function DashboardLayout() {
  const location = useLocation();
  const title = TITLES[location.pathname] || 'Dashboard';

  return (
    <div className="min-h-screen bg-void text-ink">
      <Sidebar />
      <div className="pl-[76px] lg:pl-64">
        <header className="h-[72px] border-b border-void-border flex items-center justify-between px-6 lg:px-10 bg-void/80 backdrop-blur-xl sticky top-0 z-30">
          <div>
            <span className="mono-label text-[10px] text-ink-faint">ONYX / DASHBOARD</span>
            <h1 className="font-display font-semibold text-lg leading-tight">{title}</h1>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-cyan-glow/25 bg-cyan-soft">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-glow animate-pulse" />
            <span className="mono-label text-[10px] text-cyan-glow">Shield Active</span>
          </div>
        </header>
        <main className="p-6 lg:p-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
