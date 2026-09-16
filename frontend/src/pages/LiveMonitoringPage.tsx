import React, { useState, useEffect } from 'react';
import {
  Radio,
  Play,
  Square,
  AlertOctagon,
  RotateCcw,
  Thermometer,
  Heart,
  Wind,
  Zap,
  TrendingUp,
  Droplets,
  Activity,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { api } from '../services/api';
import { GaugeCard } from '../components/GaugeCard';
import { StatusBadge } from '../components/StatusBadge';

export const LiveMonitoringPage: React.FC = () => {
  const [cattleList, setCattleList] = useState<any[]>([]);
  const [selectedTag, setSelectedTag] = useState<string>('COW001');
  const [selectedCattle, setSelectedCattle] = useState<any>(null);

  const [simRunning, setSimRunning] = useState<boolean>(false);
  const [simStatusMsg, setSimStatusMsg] = useState<string>('');
  const [telemetryLog, setTelemetryLog] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const [cattleRes, simRes] = await Promise.all([
        api.getCattleList(),
        api.getSimulatorStatus()
      ]);
      setCattleList(cattleRes);
      setSimRunning(simRes.running);

      const target = cattleRes.find((c: any) => c.tag_id === selectedTag) || cattleRes[0];
      if (target) {
        setSelectedCattle(target);
      }
    } catch (err) {
      console.error('Failed to load telemetry:', err);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000); // 3s polling for live simulation
    return () => clearInterval(interval);
  }, [selectedTag]);

  const handleStartSim = async () => {
    try {
      const res = await api.startSimulator();
      setSimRunning(res.running);
      setSimStatusMsg('Simulation started: Ingesting periodic telemetry for all cattle.');
    } catch (err) {
      console.error(err);
    }
  };

  const handleStopSim = async () => {
    try {
      const res = await api.stopSimulator();
      setSimRunning(res.running);
      setSimStatusMsg('Simulation paused.');
    } catch (err) {
      console.error(err);
    }
  };

  const handleTriggerAbnormal = async () => {
    try {
      const res = await api.triggerAbnormal(selectedTag);
      setSimStatusMsg(res.message);
      // Ensure simulator is active
      if (!simRunning) {
        await api.startSimulator();
        setSimRunning(true);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleReset = async () => {
    try {
      const res = await api.resetSimulator();
      setSimStatusMsg(res.message);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const vitals = {
    temperature: selectedCattle?.latest_temperature || 38.6,
    heart_rate: selectedCattle?.latest_heart_rate || 65.0,
    respiratory_rate: 26.0,
    activity_level: selectedCattle?.latest_activity || 0.84,
    feed_intake: 19.5,
    water_intake: 65.0
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
            Live IoT Pasture Telemetry &amp; Simulator
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Smart Collar Edge Node &bull; MQTT: cattlex/cattle/{selectedTag}/telemetry
          </p>
        </div>

        {/* Simulator Running Badge */}
        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold border ${
              simRunning
                ? 'bg-emerald-950/80 text-emerald-400 border-emerald-800 animate-pulse'
                : 'bg-slate-900 text-slate-400 border-slate-800'
            }`}
          >
            <span
              className={`w-2 h-2 rounded-full ${
                simRunning ? 'bg-emerald-400' : 'bg-slate-500'
              }`}
            />
            {simRunning ? 'SIMULATOR ACTIVE' : 'SIMULATOR IDLE'}
          </span>
        </div>
      </div>

      {/* Control Console */}
      <div className="glass-panel p-5 rounded-2xl space-y-4">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-3 w-full md:w-auto">
            <span className="text-xs font-semibold uppercase tracking-wider font-mono text-slate-400">
              Target Cattle:
            </span>
            <select
              value={selectedTag}
              onChange={(e) => setSelectedTag(e.target.value)}
              className="px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-semibold focus:outline-none focus:border-brand-500 font-mono"
            >
              {cattleList.map((c) => (
                <option key={c.id} value={c.tag_id}>
                  {c.tag_id} - {c.name} ({c.status})
                </option>
              ))}
            </select>
            {selectedCattle && <StatusBadge status={selectedCattle.status} size="sm" />}
          </div>

          <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
            {!simRunning ? (
              <button
                onClick={handleStartSim}
                className="px-3.5 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs flex items-center gap-1.5 transition-all shadow-md shadow-brand-500/20"
              >
                <Play className="w-3.5 h-3.5" /> Start Simulator
              </button>
            ) : (
              <button
                onClick={handleStopSim}
                className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs flex items-center gap-1.5 transition-colors border border-slate-700"
              >
                <Square className="w-3.5 h-3.5" /> Pause Simulator
              </button>
            )}

            <button
              onClick={handleTriggerAbnormal}
              className="px-3.5 py-2 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center gap-1.5 transition-all shadow-md shadow-rose-600/20"
            >
              <AlertOctagon className="w-3.5 h-3.5" /> Trigger Sickness ({selectedTag})
            </button>

            <button
              onClick={handleReset}
              className="px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-850 border border-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Reset Vitals
            </button>
          </div>
        </div>

        {simStatusMsg && (
          <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-brand-300 font-mono flex items-center gap-2">
            <Radio className="w-4 h-4 shrink-0 text-brand-400 animate-pulse" />
            <span>{simStatusMsg}</span>
          </div>
        )}
      </div>

      {/* Live Physical Sensor Gauges */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xs uppercase font-mono tracking-wider text-slate-400">
            Real-Time Physiological Telemetry ({selectedTag})
          </h3>
          <span className="text-xs font-mono text-slate-400">
            Health Risk Score: <strong className="text-slate-100">{selectedCattle?.risk_score || 12}/100</strong>
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <GaugeCard
            title="Body Temperature"
            value={vitals.temperature}
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
            value={vitals.heart_rate}
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
            value={vitals.respiratory_rate}
            unit="bpm"
            min={10.0}
            max={70.0}
            normalMin={24.0}
            normalMax={36.0}
            icon={Wind}
            sensorModel="Acoustic / Accelerometer"
          />
          <GaugeCard
            title="Activity Index"
            value={vitals.activity_level}
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
            value={vitals.feed_intake}
            unit="kg"
            min={0.0}
            max={35.0}
            normalMin={14.0}
            normalMax={25.0}
            icon={TrendingUp}
            sensorModel="RC522 RFID + Load Cell"
          />
          <GaugeCard
            title="Water Intake"
            value={vitals.water_intake}
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

      {/* Environmental Context */}
      <div className="glass-panel p-5 rounded-xl flex flex-wrap items-center justify-between gap-4 text-xs">
        <div className="flex items-center gap-3">
          <span className="text-slate-400 font-mono uppercase">Pasture Microclimate:</span>
          <span className="text-slate-200">Ambient: 24.8&deg;C &bull; Humidity: 61% &bull; Solar Battery: 4.14V (Charging)</span>
        </div>
        <span className="text-brand-400 font-mono font-semibold">LoRaWAN Gateway &bull; SNR: 9.2 dB</span>
      </div>
    </div>
  );
};
