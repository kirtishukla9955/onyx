import React, { useState } from 'react';
import { Settings as SettingsIcon, Save, LogOut } from 'lucide-react';
import { Panel, PrimaryButton, SecondaryButton, StatusBanner } from '../components/DashboardUI';
import { TextField } from '../components/FormField';
import { useAuth } from '../context/AuthContext';

export default function Settings() {
  const { user, logout } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [saved, setSaved] = useState(false);

  function handleSave(e) {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center border border-cyan-glow/30 bg-cyan-soft shrink-0">
          <SettingsIcon size={22} className="text-cyan-glow" />
        </div>
        <div>
          <h2 className="font-display font-semibold text-2xl">Settings</h2>
          <p className="text-ink-dim mt-1">Manage your account and shield preferences.</p>
        </div>
      </div>

      <Panel eyebrow="Account" title="Profile">
        <form onSubmit={handleSave} className="space-y-1">
          <TextField label="Full name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" />
          <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" />

          {saved && <StatusBanner state="success" message="Profile updated." />}

          <PrimaryButton type="submit" icon={Save}>Save changes</PrimaryButton>
        </form>
      </Panel>

      <Panel eyebrow="Backend" title="Connected services">
        <div className="space-y-3">
          {[
            ['Cybersecurity Backend', 'localhost:8001'],
            ['ML Backend', 'localhost:8002'],
            ['Trend Engine', 'localhost:8003'],
          ].map(([label, url]) => (
            <div key={label} className="flex items-center justify-between rounded-lg border border-void-border bg-void-deep/60 px-4 py-3">
              <span className="text-sm">{label}</span>
              <span className="font-mono text-xs text-ink-faint">{url}</span>
            </div>
          ))}
        </div>
        <p className="text-xs text-ink-faint mt-4">
          Edit <code className="text-cyan-glow">src/api/client.js</code> to change these if your backend
          runs elsewhere.
        </p>
      </Panel>

      <Panel eyebrow="Session" title="Sign out">
        <p className="text-ink-dim text-sm mb-4">End your current session on this device.</p>
        <SecondaryButton onClick={logout} icon={LogOut}>Log out</SecondaryButton>
      </Panel>
    </div>
  );
}
