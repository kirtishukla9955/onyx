import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

const STORAGE_KEY = 'onyx_session';

/*
  This is a placeholder auth layer so the UI is fully wired and testable
  before a real backend exists. It stores a fake session in localStorage.

  TO CONNECT YOUR REAL BACKEND LATER:
  Replace the bodies of `signup` and `login` below with real calls, e.g.

    const res = await fetch('http://localhost:8001/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await res.json();
    setUser(data.user);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data.user));

  Nothing else in the app needs to change — every page reads the user
  only through useAuth().
*/

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch (_) {
        localStorage.removeItem(STORAGE_KEY);
      }
    }
    setLoading(false);
  }, []);

  async function signup({ name, email, password }) {
    await fakeNetworkDelay();
    if (!name || !email || !password) {
      throw new Error('All fields are required.');
    }
    if (password.length < 6) {
      throw new Error('Password must be at least 6 characters.');
    }
    const newUser = { id: crypto.randomUUID(), name, email };
    setUser(newUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newUser));
    return newUser;
  }

  async function login({ email, password }) {
    await fakeNetworkDelay();
    if (!email || !password) {
      throw new Error('Enter your email and password.');
    }
    // Mock: accept any well-formed credentials since there is no backend yet.
    const existingName = email.split('@')[0];
    const loggedInUser = { id: crypto.randomUUID(), name: existingName, email };
    setUser(loggedInUser);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(loggedInUser));
    return loggedInUser;
  }

  function logout() {
    setUser(null);
    localStorage.removeItem(STORAGE_KEY);
  }

  return (
    <AuthContext.Provider value={{ user, loading, signup, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}

function fakeNetworkDelay() {
  return new Promise((resolve) => setTimeout(resolve, 600));
}
