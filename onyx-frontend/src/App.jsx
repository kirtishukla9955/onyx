import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './lib/ProtectedRoute';

import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Login from './pages/Login';

import DashboardLayout from './dashboard/DashboardLayout';
import Overview from './dashboard/Overview';
import Camouflage from './dashboard/Camouflage';
import FingerprintPage from './dashboard/FingerprintPage';
import Acoustic from './dashboard/Acoustic';
import TrendRadar from './dashboard/TrendRadar';
import Settings from './dashboard/Settings';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="bg-void min-h-screen text-ink font-body">
          <div className="grain" />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Overview />} />
              <Route path="camouflage" element={<Camouflage />} />
              <Route path="fingerprint" element={<FingerprintPage />} />
              <Route path="acoustic" element={<Acoustic />} />
              <Route path="trendradar" element={<TrendRadar />} />
              <Route path="settings" element={<Settings />} />
            </Route>
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}
