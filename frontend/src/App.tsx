import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './layouts/DashboardLayout';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { CattleListPage } from './pages/CattleListPage';
import { CattleProfilePage } from './pages/CattleProfilePage';
import { DiseasePredictionPage } from './pages/DiseasePredictionPage';
import { LiveMonitoringPage } from './pages/LiveMonitoringPage';
import { AlertsPage } from './pages/AlertsPage';
import { VeterinaryPage } from './pages/VeterinaryPage';
import { ModelsPage } from './pages/ModelsPage';
import { ReportsPage } from './pages/ReportsPage';
import { SettingsPage } from './pages/SettingsPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Landing & Login */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* Protected Dashboard Shell */}
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/cattle" element={<CattleListPage />} />
          <Route path="/cattle/:id" element={<CattleProfilePage />} />
          <Route path="/prediction" element={<DiseasePredictionPage />} />
          <Route path="/live" element={<LiveMonitoringPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/veterinary" element={<VeterinaryPage />} />
          <Route path="/models" element={<ModelsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};
