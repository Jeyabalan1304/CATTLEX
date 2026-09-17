import React from 'react';
import { Bell, ShieldCheck, User, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

interface NavbarProps {
  activeAlertCount?: number;
}

export const Navbar: React.FC<NavbarProps> = ({ activeAlertCount = 0 }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-3">
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-300">
          Farm Node: <strong className="text-slate-100">FARM-01</strong>
        </span>
        <span className="hidden md:inline-flex items-center gap-1.5 text-xs text-slate-400">
          <ShieldCheck className="w-3.5 h-3.5 text-brand-400" />
          Predictive Health Monitoring Active
        </span>
      </div>

      <div className="flex items-center gap-4">
        {/* Quick Alert Bell */}
        <Link
          to="/alerts"
          className="relative p-2 rounded-lg bg-slate-800/80 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors border border-slate-700/60"
        >
          <Bell className="w-4 h-4" />
          {activeAlertCount > 0 && (
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-white text-[10px] font-bold flex items-center justify-center animate-pulse">
              {activeAlertCount}
            </span>
          )}
        </Link>

        {/* User Indicator */}
        <div className="flex items-center gap-2.5 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-sky-600 flex items-center justify-center text-white text-xs font-bold shadow-sm">
            JB
          </div>
          <div className="hidden sm:block text-left">
            <p className="text-xs font-semibold text-slate-200">Jeyabalan</p>
            <p className="text-[10px] text-slate-400">System Administrator</p>
          </div>
        </div>
      </div>
    </header>
  );
};
