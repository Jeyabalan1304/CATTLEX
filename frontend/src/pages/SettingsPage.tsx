import React, { useState } from 'react';
import { Settings, Save, ShieldCheck, Radio, Bell } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [mqttHost, setMqttHost] = useState('localhost');
  const [mqttPort, setMqttPort] = useState(1883);
  const [telemetryInterval, setTelemetryInterval] = useState(5);
  const [tempThreshold, setTempThreshold] = useState(39.4);
  const [heartRateThreshold, setHeartRateThreshold] = useState(84);
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white font-sans">System Settings</h1>
        <p className="text-xs text-slate-400 mt-1 font-mono">
          IoT Collar Ingestion Rates &bull; Safety Thresholds &bull; Message Broker Link
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* MQTT Config */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Radio className="w-4 h-4 text-brand-400" />
            MQTT Broker Connectivity
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">Broker Hostname / IP</label>
              <input
                type="text"
                value={mqttHost}
                onChange={(e) => setMqttHost(e.target.value)}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">Broker Port</label>
              <input
                type="number"
                value={mqttPort}
                onChange={(e) => setMqttPort(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-mono"
              />
            </div>
          </div>
        </div>

        {/* Safety Thresholds */}
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Bell className="w-4 h-4 text-rose-400" />
            Automated Alert Rule Thresholds
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">Fever Cutoff (°C)</label>
              <input
                type="number"
                step="0.1"
                value={tempThreshold}
                onChange={(e) => setTempThreshold(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-mono"
              />
              <span className="text-[10px] text-slate-500 font-mono">Default: 39.4°C</span>
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">Tachycardia Cutoff (bpm)</label>
              <input
                type="number"
                value={heartRateThreshold}
                onChange={(e) => setHeartRateThreshold(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-mono"
              />
              <span className="text-[10px] text-slate-500 font-mono">Default: 84 bpm</span>
            </div>
            <div>
              <label className="block text-xs font-mono text-slate-300 mb-1">Telemetry Rate (sec)</label>
              <input
                type="number"
                value={telemetryInterval}
                onChange={(e) => setTelemetryInterval(Number(e.target.value))}
                className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 font-mono"
              />
              <span className="text-[10px] text-slate-500 font-mono">Default: 5s interval</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            type="submit"
            className="px-5 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs flex items-center gap-2 transition-colors shadow-md shadow-brand-500/20"
          >
            <Save className="w-4 h-4" />
            Save Parameters
          </button>
          {saved && (
            <span className="text-xs text-emerald-400 font-mono flex items-center gap-1">
              <ShieldCheck className="w-4 h-4" /> Parameters saved successfully.
            </span>
          )}
        </div>
      </form>
    </div>
  );
};
