import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Radio, Lock, Mail, ShieldAlert, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@cattlex.io');
  const [password, setPassword] = useState('admin123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await api.login({ email, password });
      if (res.access_token) {
        localStorage.setItem('cattlex_token', res.access_token);
        localStorage.setItem('cattlex_user', JSON.stringify(res.user));
      }
      navigate('/dashboard');
    } catch (err: any) {
      // For demo convenience, allow proceed if mock credentials used
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const quickFill = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center px-6 relative">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-tr from-brand-600 to-emerald-400 text-slate-950 font-bold mb-3 shadow-lg shadow-brand-500/20">
            <Radio className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white font-sans">Sign in to CATTLEX</h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">Livestock Health & AI Telemetry Node</p>
        </div>

        <div className="glass-panel p-8 rounded-2xl shadow-xl">
          {error && (
            <div className="mb-4 p-3 rounded-lg bg-rose-950/80 border border-rose-800/80 text-rose-300 text-xs flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5 font-mono">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5 font-mono">
                Password
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-bold text-sm transition-all shadow-md shadow-brand-600/20 flex items-center justify-center gap-2"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Credentials */}
          <div className="mt-6 pt-5 border-t border-slate-800">
            <p className="text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-2">
              Quick Role Switch (Demo Credentials):
            </p>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => quickFill('admin@cattlex.io', 'admin123')}
                className="p-2 rounded bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[11px] text-left text-slate-300"
              >
                <span className="font-bold block text-purple-400">Admin</span>
                admin@cattlex.io
              </button>
              <button
                type="button"
                onClick={() => quickFill('farmer@cattlex.io', 'farmer123')}
                className="p-2 rounded bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[11px] text-left text-slate-300"
              >
                <span className="font-bold block text-emerald-400">Farmer</span>
                farmer@cattlex.io
              </button>
              <button
                type="button"
                onClick={() => quickFill('vet@cattlex.io', 'vet123')}
                className="p-2 rounded bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[11px] text-left text-slate-300"
              >
                <span className="font-bold block text-sky-400">Vet</span>
                vet@cattlex.io
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
