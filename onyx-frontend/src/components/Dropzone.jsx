import React, { useState, useRef } from 'react';
import { UploadCloud, FileCheck2, X } from 'lucide-react';

export default function Dropzone({ accept, file, onFileSelected, label = 'Drop a file or click to browse', hint }) {
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) onFileSelected(dropped);
  }

  function handleChange(e) {
    const picked = e.target.files?.[0];
    if (picked) onFileSelected(picked);
  }

  if (file) {
    return (
      <div className="flex items-center justify-between gap-3 rounded-xl border border-cyan-glow/30 bg-cyan-soft px-5 py-4">
        <div className="flex items-center gap-3 overflow-hidden">
          <FileCheck2 size={20} className="text-cyan-glow shrink-0" />
          <div className="overflow-hidden">
            <div className="text-sm font-medium truncate">{file.name}</div>
            <div className="text-xs text-ink-faint">{(file.size / 1024).toFixed(1)} KB</div>
          </div>
        </div>
        <button
          onClick={() => onFileSelected(null)}
          className="text-ink-faint hover:text-alert-red transition-colors shrink-0"
          aria-label="Remove file"
        >
          <X size={18} />
        </button>
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`cursor-pointer rounded-xl border-2 border-dashed px-6 py-10 flex flex-col items-center justify-center text-center transition-colors ${
        dragOver ? 'border-cyan-glow bg-cyan-soft' : 'border-void-border hover:border-cyan-glow/40'
      }`}
    >
      <UploadCloud size={28} className={`mb-3 ${dragOver ? 'text-cyan-glow' : 'text-ink-faint'}`} />
      <p className="text-sm text-ink-dim">{label}</p>
      {hint && <p className="text-xs text-ink-faint mt-1">{hint}</p>}
      <input ref={inputRef} type="file" accept={accept} onChange={handleChange} className="hidden" />
    </div>
  );
}
