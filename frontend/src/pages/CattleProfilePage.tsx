import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Thermometer,
  Heart,
  Wind,
  Zap,
  Clock,
  AlertTriangle,
  CalendarCheck,
  Stethoscope,
  ArrowLeft,
  RefreshCw,
  TrendingUp,
  Droplets
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
import { StatusBadge } from '../components/StatusBadge';
import { GaugeCard } from '../components/GaugeCard';

export const CattleProfilePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const cattleId = Number(id) || 1;

  const [profile, setProfile] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadProfileData = async () => {
    try {
      const [profData, histData, predData] = await Promise.all([
        api.getCattleProfile(cattleId),
        api.getSensorHistory(cattleId),
        api.getPredictionHistory(cattleId)
      ]);
      setProfile(profData);
      setHistory(histData.reverse());
      setPredictions(predData);
    } catch (err) {
      console.error('Error loading cattle profile:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfileData();
  }, [cattleId]);

  if (loading && !profile) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400 font-mono text-xs">
        Loading cattle profile and telemetry history...
      </div>
    );
  }

  const vitals = profile?.latest_vitals || {};

  return (
    <div className="space-y-8">
      {/* Top Breadcrumb & Actions */}
      <div className="flex items-center justify-between">
        <Link
          to="/cattle"
          className="inline-flex items-center gap-1 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Cattle Fleet
        </Link>
        <button
          onClick={loadProfileData}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white text-xs flex items-center gap-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Refresh
        </button>
      </div>

      {/* Cattle Identity Banner */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-sky-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-emerald-950/50">
            {profile?.tag_id?.substring(0, 3)}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-white font-sans">{profile?.tag_id} ({profile?.name})</h1>
              <StatusBadge status={profile?.status || 'HEALTHY'} size="md" />
            </div>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Breed: <span className="text-slate-200 font-semibold">{profile?.breed}</span> &bull; Age: {profile?.age} mo &bull; Weight: {profile?.weight} kg &bull; Location: {profile?.farm_id}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 p-4 rounded-xl">
          <div className="text-right">
            <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400 block">Health Risk Score</span>
            <span className="text-2xl font-extrabold font-mono text-slate-100">
              {profile?.latest_prediction?.risk_score || 12}/100
            </span>
          </div>
          <Link
            to="/prediction"
            className="px-3.5 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs transition-colors flex items-center gap-1.5"
          >
            <Stethoscope className="w-4 h-4" />
            Diagnose
          </Link>
        </div>
      </div>

      {/* Real-time Physiological Gauges */}
      <div>
        <h3 className="text-xs uppercase font-mono tracking-wider text-slate-400 mb-4">
          Current Vital Telemetry (Smart Collar &amp; Ingestion Stations)
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <GaugeCard
            title="Body Temperature"
            value={vitals.temperature || 38.6}
            unit="°C"
            min={36.0}
            max={42.0}
            normalMin={38.0}
            normalMax={39.3}
            icon={Thermometer}
            sensorModel="MLX90614 (Infrared)"
          />
          <GaugeCard
            title="Heart Rate"
            value={vitals.heart_rate || 64.0}
            unit="bpm"
            min={30.0}
            max={140.0}
            normalMin={48.0}
            normalMax={84.0}
            icon={Heart}
            sensorModel="MAX30102 (PPG)"
          />
          <GaugeCard
            title="Respiratory Rate"
            value={vitals.respiratory_rate || 26.0}
            unit="bpm"
            min={10.0}
            max={70.0}
            normalMin={24.0}
            normalMax={36.0}
            icon={Wind}
            sensorModel="Acoustic / IMU"
          />
          <GaugeCard
            title="Activity Index"
            value={vitals.activity_level || 0.85}
            unit=""
            min={0.0}
            max={1.0}
            normalMin={0.65}
            normalMax={1.0}
            icon={Zap}
            sensorModel="MPU6050 (3-Axis IMU)"
          />
          <GaugeCard
            title="Feed Intake"
            value={vitals.feed_intake || 19.5}
            unit="kg"
            min={0.0}
            max={35.0}
            normalMin={14.0}
            normalMax={25.0}
            icon={TrendingUp}
            sensorModel="RC522 + Load Cell"
          />
          <GaugeCard
            title="Water Intake"
            value={vitals.water_intake || 65.0}
            unit="L"
            min={0.0}
            max={100.0}
            normalMin={40.0}
            normalMax={85.0}
            icon={Droplets}
            sensorModel="YF-S201 Flow Sensor"
          />
        </div>
      </div>

      {/* Historical Telemetry Charts */}
      <div className="glass-panel p-6 rounded-2xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-100">Telemetry History &amp; Vital Curve</h3>
            <p className="text-xs text-slate-400 font-mono">24-hour recorded timeline for {profile?.tag_id}</p>
          </div>
          <span className="text-xs font-mono text-slate-400">{history.length} Data Points</span>
        </div>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey="timestamp"
                tickFormatter={(t) => new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                stroke="#64748b"
                fontSize={11}
              />
              <YAxis yAxisId="temp" domain={[37.0, 42.0]} stroke="#ef4444" fontSize={11} />
              <YAxis yAxisId="hr" orientation="right" domain={[40, 130]} stroke="#38bdf8" fontSize={11} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
              />
              <Legend />
              <Line yAxisId="temp" type="monotone" dataKey="temperature" name="Temp (°C)" stroke="#ef4444" strokeWidth={2} dot={false} />
              <Line yAxisId="hr" type="monotone" dataKey="heart_rate" name="Heart Rate (bpm)" stroke="#38bdf8" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Health Timeline & Prediction Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Health Timeline */}
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-sm font-bold text-slate-100 mb-1 flex items-center gap-2">
            <Clock className="w-4 h-4 text-brand-400" />
            Health State Timeline
          </h3>
          <p className="text-xs text-slate-400 font-mono mb-4">Historical risk transitions</p>

          <div className="space-y-3">
            {predictions?.health_predictions?.slice(0, 6).map((hp: any, idx: number) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <div className="w-16 shrink-0 font-mono text-[11px] text-slate-400 mt-0.5">
                  {new Date(hp.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <StatusBadge status={hp.health_status} size="sm" />
                    <span className="text-xs font-mono text-slate-400">Risk: {hp.risk_score.toFixed(0)}/100</span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1">{hp.prediction_reason}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Multi-Disease Predictions */}
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-sm font-bold text-slate-100 mb-1 flex items-center gap-2">
            <Stethoscope className="w-4 h-4 text-sky-400" />
            Symptom-based Disease Inference History
          </h3>
          <p className="text-xs text-slate-400 font-mono mb-4">AI differential diagnoses</p>

          {predictions?.disease_predictions?.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-xs text-slate-500 mb-3">No symptom predictions logged for this cattle.</p>
              <Link
                to="/prediction"
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 inline-block font-semibold"
              >
                Run Disease Inference
              </Link>
            </div>
          ) : (
            <div className="space-y-3">
              {predictions?.disease_predictions?.slice(0, 4).map((dp: any) => (
                <div key={dp.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-100 capitalize">
                      {dp.predicted_disease.replace('_', ' ')}
                    </span>
                    <span className="text-xs font-mono text-brand-400 font-semibold">
                      {(dp.confidence * 100).toFixed(1)}% Confidence
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1.5">{dp.recommendation}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
