import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, AlertCircle } from 'lucide-react';
import AuthLayout from './AuthLayout';
import { TextField, PasswordField } from '../components/FormField';
import { useAuth } from '../context/AuthContext';

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await signup(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Something went wrong. Try again.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <AuthLayout
      title="Create your shield"
      subtitle="Set up your ONYX account to start protecting your content."
      footer={
        <>
          Already protected?{' '}
          <Link to="/login" className="text-cyan-glow hover:underline">
            Sign in
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit}>
        <TextField label="Full name" value={form.name} onChange={update('name')} placeholder="Avery Chen" autoComplete="name" />
        <TextField label="Email" type="email" value={form.email} onChange={update('email')} placeholder="you@example.com" autoComplete="email" />
        <PasswordField label="Password" value={form.password} onChange={update('password')} placeholder="At least 6 characters" />

        {error && (
          <div className="flex items-center gap-2 text-alert-red text-sm mb-4">
            <AlertCircle size={15} />
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="shine group w-full flex items-center justify-center gap-2 py-3.5 rounded-full bg-cyan-glow text-void-deep font-semibold hover:shadow-[0_0_28px_rgba(0,240,255,0.5)] transition-shadow disabled:opacity-60"
        >
          {submitting ? 'Creating account...' : 'Create account'}
          {!submitting && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
        </button>
      </form>
    </AuthLayout>
  );
}
