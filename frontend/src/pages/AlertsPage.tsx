import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AlertTriangle, ShieldCheck, Check, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>('ACTIVE');
  const [loading, setLoading] = useState(true);

  const loadAlerts = async () => {
    try {
      const data = await api.getAlerts(statusFilter === 'ALL' ? undefined : statusFilter);
      setAlerts(data);
    } catch (err) {
      console.error('Failed to load alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, [statusFilter]);

  const handleResolve = async (id: number) => {
    try {
      await api.resolveAlert(id);
      loadAlerts();
    } catch (err) {
      console.error('Failed to resolve alert:', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
            Safety &amp; Triage Alerts
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Automated Physiological Threshold Rule Engine &bull; Incident Logs
          </p>
        </div>

        <button
          onClick={loadAlerts}
          className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors flex items-center gap-1.5 text-xs font-medium self-start"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
        {['ACTIVE', 'RESOLVED', 'ALL'].map((tab) => (
          <button
            key={tab}
            onClick={() => setStatusFilter(tab)}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              statusFilter === tab
                ? 'bg-brand-600 text-slate-950 font-bold'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            {tab} Alerts
          </button>
        ))}
      </div>

      {/* Alerts Table */}
      <div className="space-y-3">
        {alerts.length === 0 ? (
          <div className="glass-panel p-12 text-center rounded-2xl">
            <ShieldCheck className="w-10 h-10 text-emerald-400 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-slate-200">No {statusFilter} Alerts</h3>
            <p className="text-xs text-slate-400 mt-1">All cattle parameters currently within safety thresholds.</p>
          </div>
        ) : (
          alerts.map((a) => (
            <div
              key={a.id}
              className="glass-panel p-5 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1.5">
                <div className="flex items-center gap-3">
                  <StatusBadge status={a.severity} size="sm" />
                  <span className="text-xs font-mono text-brand-400 font-bold">Cattle #{a.cattle_id}</span>
                  <span className="text-slate-400 text-xs font-mono">&bull; {a.type}</span>
                  <span className="text-slate-500 text-[11px]">
                    {new Date(a.created_at).toLocaleString()}
                  </span>
                </div>
                <p className="text-xs text-slate-200 leading-relaxed font-sans">{a.message}</p>
              </div>

              <div className="flex items-center gap-3 shrink-0">
                <Link
                  to={`/cattle/${a.cattle_id}`}
                  className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs font-medium"
                >
                  View Vitals
                </Link>
                {a.status === 'ACTIVE' && (
                  <button
                    onClick={() => handleResolve(a.id)}
                    className="px-3.5 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 text-xs font-bold transition-colors flex items-center gap-1"
                  >
                    <Check className="w-3.5 h-3.5" />
                    Resolve Alert
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
