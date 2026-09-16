import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Activity,
  Stethoscope,
  Radio,
  AlertTriangle,
  CalendarCheck,
  Cpu,
  FileText,
  Settings,
  HelpCircle,
  Home
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Cattle Fleet', path: '/cattle', icon: Activity },
    { label: 'Disease Prediction', path: '/prediction', icon: Stethoscope },
    { label: 'Live IoT Telemetry', path: '/live', icon: Radio },
    { label: 'Alerts & Triage', path: '/alerts', icon: AlertTriangle },
    { label: 'Veterinary RPA', path: '/veterinary', icon: CalendarCheck },
    { label: 'ML Benchmark', path: '/models', icon: Cpu },
    { label: 'Reports & Export', path: '/reports', icon: FileText },
    { label: 'System Settings', path: '/settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col justify-between shrink-0 h-screen sticky top-0">
      <div>
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center gap-3 border-b border-slate-800">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
            <Radio className="w-4 h-4 text-slate-950 font-bold" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white font-sans">
              CATTLEX <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-400 border border-brand-500/30">AIoT</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-mono">Livestock Health Platform</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-4 space-y-1.5">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-slate-800/80 text-brand-400'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`
            }
          >
            <Home className="w-4 h-4" />
            Landing Page
          </NavLink>

          <div className="pt-2 pb-1 px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500 font-mono">
            Platform Modules
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-brand-600/15 text-brand-400 border border-brand-500/30 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer / System Status */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="p-3 rounded-lg bg-slate-850 border border-slate-800">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400">IoT Edge Status</span>
            <span className="flex items-center gap-1 text-emerald-400 font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              ONLINE
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1 font-mono">MQTT: cattlex/cattle/#</p>
        </div>
      </div>
    </aside>
  );
};
