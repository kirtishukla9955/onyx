import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

export function TextField({ label, type = 'text', value, onChange, placeholder, ...rest }) {
  return (
    <div className="mb-4">
      <label className="block mono-label text-[10px] text-ink-faint mb-2">{label}</label>
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full px-4 py-3 rounded-lg bg-void-deep border border-void-border text-ink placeholder:text-ink-faint focus:outline-none focus:border-cyan-glow/50 focus:ring-1 focus:ring-cyan-glow/30 transition-colors"
        {...rest}
      />
    </div>
  );
}

export function PasswordField({ label, value, onChange, placeholder }) {
  const [show, setShow] = useState(false);
  return (
    <div className="mb-4">
      <label className="block mono-label text-[10px] text-ink-faint mb-2">{label}</label>
      <div className="relative">
        <input
          type={show ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="w-full px-4 py-3 pr-11 rounded-lg bg-void-deep border border-void-border text-ink placeholder:text-ink-faint focus:outline-none focus:border-cyan-glow/50 focus:ring-1 focus:ring-cyan-glow/30 transition-colors"
        />
        <button
          type="button"
          onClick={() => setShow((s) => !s)}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint hover:text-cyan-glow transition-colors"
          aria-label={show ? 'Hide password' : 'Show password'}
        >
          {show ? <EyeOff size={17} /> : <Eye size={17} />}
        </button>
      </div>
    </div>
  );
}
