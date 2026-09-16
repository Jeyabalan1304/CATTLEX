import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, ChevronRight, Activity, Plus, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export const CattleListPage: React.FC = () => {
  const [cattleList, setCattleList] = useState<any[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  const loadCattle = async () => {
    try {
      const data = await api.getCattleList();
      setCattleList(data);
    } catch (err) {
      console.error('Error fetching cattle:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCattle();
  }, []);

  const filtered = cattleList.filter((c) => {
    const matchesSearch =
      c.tag_id.toLowerCase().includes(search.toLowerCase()) ||
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.breed.toLowerCase().includes(search.toLowerCase());

    const matchesStatus = statusFilter === 'ALL' || c.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">Cattle Herd Directory</h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            {cattleList.length} Registered Heads &bull; Continuous Collar Tracking
          </p>
        </div>

        <button
          onClick={loadCattle}
          className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors flex items-center gap-1.5 text-xs font-medium self-start"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh Fleet
        </button>
      </div>

      {/* Filters Bar */}
      <div className="glass-panel p-4 rounded-xl flex flex-col sm:flex-row items-center gap-4 justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search by Tag ID, Name or Breed..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto">
          {['ALL', 'HEALTHY', 'AT_RISK', 'CRITICAL'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                statusFilter === st
                  ? 'bg-brand-600 text-slate-950 font-bold'
                  : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {st.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Cattle Fleet Table */}
      <div className="glass-panel rounded-2xl overflow-hidden border border-slate-800">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/60 text-[11px] font-mono uppercase text-slate-400 tracking-wider">
                <th className="p-4">Tag ID &amp; Name</th>
                <th className="p-4">Breed &amp; Age</th>
                <th className="p-4">Health Status</th>
                <th className="p-4">Vitals (Latest)</th>
                <th className="p-4">Health Risk Score</th>
                <th className="p-4 text-right">Profile</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80 text-xs">
              {filtered.map((c) => (
                <tr key={c.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="p-4">
                    <div className="font-bold text-slate-100 text-sm">{c.tag_id}</div>
                    <div className="text-slate-400">{c.name} &bull; {c.sex}</div>
                  </td>
                  <td className="p-4 text-slate-300">
                    <div>{c.breed}</div>
                    <div className="text-slate-400 text-[11px]">{c.age} months ({c.weight} kg)</div>
                  </td>
                  <td className="p-4">
                    <StatusBadge status={c.status} size="sm" />
                  </td>
                  <td className="p-4 font-mono text-slate-300">
                    {c.latest_temperature ? (
                      <div className="space-y-0.5 text-[11px]">
                        <div>Temp: <span className="font-bold text-slate-100">{c.latest_temperature.toFixed(1)}&deg;C</span></div>
                        <div>HR: <span className="font-bold text-slate-100">{c.latest_heart_rate ? c.latest_heart_rate.toFixed(0) : '--'} bpm</span></div>
                      </div>
                    ) : (
                      <span className="text-slate-400">Awaiting telemetry</span>
                    )}
                  </td>
                  <td className="p-4">
                    <div className="w-32">
                      <div className="flex justify-between text-[10px] font-mono text-slate-400 mb-1">
                        <span>Risk</span>
                        <span className="font-bold">{c.risk_score ? c.risk_score.toFixed(0) : 12}/100</span>
                      </div>
                      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            c.risk_score > 70 ? 'bg-rose-500' : c.risk_score > 35 ? 'bg-amber-500' : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(c.risk_score || 12, 100)}%` }}
                        />
                      </div>
                    </div>
                  </td>
                  <td className="p-4 text-right">
                    <Link
                      to={`/cattle/${c.id}`}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-medium transition-colors"
                    >
                      Inspect
                      <ChevronRight className="w-3.5 h-3.5" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
