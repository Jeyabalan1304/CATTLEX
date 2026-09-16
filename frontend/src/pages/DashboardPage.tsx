import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Users,
  ShieldCheck,
  AlertTriangle,
  Flame,
  Radio,
  Thermometer,
  Heart,
  Wind,
  Zap,
  TrendingUp,
  ArrowRight,
  RefreshCw,
  Stethoscope
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';
import { api } from '../services/api';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [sumRes, trendsRes] = await Promise.all([
        api.getDashboardSummary(),
        api.getHerdTrends()
      ]);
      setSummary(sumRes);
      setTrends(trendsRes);
    } catch (err) {
      console.error('Error fetching dashboard summary:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000); // 5s auto-refresh
    return () => clearInterval(interval);
  }, []);

  const handleResolveAlert = async (id: number) => {
    try {
      await api.resolveAlert(id);
      loadData();
    } catch (err) {
      console.error('Failed to resolve alert:', err);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-sans">
            Herd Health Operations Dashboard
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 font-mono">
            Autonomous Solar IoT Collar Ingestion &bull; Multi-Disease AI Inference
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadData}
            className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:bg-slate-800 transition-colors flex items-center gap-1.5 text-xs font-medium"
            title="Refresh"
          >
            <RefreshCw className="w-4 h-4" />
            Sync
          </button>
          <Link
            to="/live"
            className="px-4 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs transition-all shadow-md shadow-brand-600/20 flex items-center gap-2"
          >
            <Radio className="w-4 h-4" />
            Live IoT Telemetry
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          title="Total Cattle"
          value={summary?.kpis?.total_cattle || 5}
          subtitle="Monitored Herd"
          icon={Users}
          color="blue"
        />
        <MetricCard
          title="Healthy"
          value={summary?.kpis?.healthy || 3}
          subtitle="Normal Baseline"
          icon={ShieldCheck}
          color="brand"
        />
        <MetricCard
          title="At Risk"
          value={summary?.kpis?.at_risk || 1}
          subtitle="Elevated Vitals"
          icon={AlertTriangle}
          color="amber"
        />
        <MetricCard
          title="Critical"
          value={summary?.kpis?.critical || 1}
          subtitle="Pyrexia / Lethargy"
          icon={Flame}
          color="rose"
        />
        <MetricCard
          title="Active Alerts"
          value={summary?.kpis?.active_alerts || 2}
          subtitle="Triage Required"
          icon={AlertTriangle}
          color="purple"
        />
      </div>

      {/* Average Herd Vitals Strip */}
      <div className="glass-panel p-5 rounded-xl">
        <h3 className="text-xs uppercase font-mono tracking-wider text-slate-400 mb-4">
          Herd Average Physiological Parameters (Collar & Pasture Stations)
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <Thermometer className="w-3.5 h-3.5 text-rose-400" /> Body Temp
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.temperature || 38.8} &deg;C
            </p>
            <span className="text-[10px] text-slate-400">MLX90614</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <Heart className="w-3.5 h-3.5 text-rose-500" /> Heart Rate
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.heart_rate || 72} bpm
            </p>
            <span className="text-[10px] text-slate-400">MAX30102</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <Wind className="w-3.5 h-3.5 text-sky-400" /> Respiration
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.respiratory_rate || 28} bpm
            </p>
            <span className="text-[10px] text-slate-400">Acoustic / IMU</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <Zap className="w-3.5 h-3.5 text-amber-400" /> Activity Index
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.activity_level || 0.76}
            </p>
            <span className="text-[10px] text-slate-400">MPU6050 (0-1)</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-400" /> Feed Intake
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.feed_intake || 17.5} kg
            </p>
            <span className="text-[10px] text-slate-400">RFID + Scale</span>
          </div>

          <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800">
            <span className="text-[11px] text-slate-400 flex items-center gap-1">
              <Radio className="w-3.5 h-3.5 text-blue-400" /> Water Intake
            </span>
            <p className="text-lg font-bold font-mono text-slate-100 mt-1">
              {summary?.average_vitals?.water_intake || 60.5} L
            </p>
            <span className="text-[10px] text-slate-400">YF-S201 Flow</span>
          </div>
        </div>
      </div>

      {/* Historical Telemetry Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-panel p-6 rounded-2xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Temperature Telemetry Dynamics</h3>
              <p className="text-xs text-slate-400 font-mono">Bovine thermal curve (°C)</p>
            </div>
            <span className="text-xs font-mono text-slate-400">Threshold: 39.4°C</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="timestamp" stroke="#64748b" fontSize={11} />
                <YAxis domain={[37.5, 41.5]} stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="temperature"
                  name="Temp (°C)"
                  stroke="#ef4444"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Heart Rate & Activity Correlation</h3>
              <p className="text-xs text-slate-400 font-mono">Pulse (bpm) vs Mobility Index</p>
            </div>
            <span className="text-xs font-mono text-slate-400">Normal HR: 48-84 bpm</span>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="timestamp" stroke="#64748b" fontSize={11} />
                <YAxis yAxisId="left" domain={[40, 120]} stroke="#64748b" fontSize={11} />
                <YAxis yAxisId="right" orientation="right" domain={[0, 1.0]} stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="heart_rate"
                  name="Heart Rate (bpm)"
                  stroke="#38bdf8"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="activity_level"
                  name="Activity Index"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Alerts & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Alerts Table */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-2xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Active Health & Triage Alerts</h3>
              <p className="text-xs text-slate-400 font-mono">Automated safety threshold events</p>
            </div>
            <Link to="/alerts" className="text-xs text-brand-400 hover:underline font-mono">
              View All Alerts &rarr;
            </Link>
          </div>

          <div className="space-y-3">
            {summary?.recent_alerts?.length === 0 ? (
              <p className="text-xs text-slate-500 py-6 text-center">No active alerts recorded.</p>
            ) : (
              summary?.recent_alerts?.map((alert: any) => (
                <div
                  key={alert.id}
                  className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 flex items-start justify-between gap-4"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <StatusBadge status={alert.severity} size="sm" />
                      <span className="text-xs font-mono text-slate-400">{alert.type}</span>
                    </div>
                    <p className="text-xs text-slate-200 mt-1">{alert.message}</p>
                  </div>
                  {alert.status === 'ACTIVE' && (
                    <button
                      onClick={() => handleResolveAlert(alert.id)}
                      className="shrink-0 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors border border-slate-700"
                    >
                      Acknowledge
                    </button>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Quick Launchpad */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-100 mb-2">Decision-Support Tools</h3>
            <p className="text-xs text-slate-400 mb-6">
              Access the clinical symptom inference model or inspect individual cattle telemetry.
            </p>

            <div className="space-y-3">
              <Link
                to="/prediction"
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 flex items-center justify-between text-xs text-slate-200 font-medium group transition-colors"
              >
                <span className="flex items-center gap-2.5">
                  <Stethoscope className="w-4 h-4 text-brand-400" />
                  Multi-Disease Prediction Form
                </span>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
              </Link>

              <Link
                to="/cattle"
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 flex items-center justify-between text-xs text-slate-200 font-medium group transition-colors"
              >
                <span className="flex items-center gap-2.5">
                  <Users className="w-4 h-4 text-sky-400" />
                  View All Cattle Records
                </span>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
              </Link>

              <Link
                to="/models"
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 flex items-center justify-between text-xs text-slate-200 font-medium group transition-colors"
              >
                <span className="flex items-center gap-2.5">
                  <Zap className="w-4 h-4 text-amber-400" />
                  ML Algorithms &amp; Benchmark
                </span>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-800/80">
            <span className="text-[11px] font-mono text-slate-500">
              System: CATTLEX Autonomous Pasture Node
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
