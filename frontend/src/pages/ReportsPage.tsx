import React from 'react';
import { Download, FileSpreadsheet, ShieldAlert, Activity, Stethoscope } from 'lucide-react';
import { api } from '../services/api';

export const ReportsPage: React.FC = () => {
  const downloadCSV = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  };

  const exportCattleHealthCSV = async () => {
    const list = await api.getCattleList();
    const headers = ['ID', 'Tag ID', 'Name', 'Breed', 'Age (Mo)', 'Weight (kg)', 'Status', 'Risk Score', 'Latest Temp', 'Latest HR'];
    const rows = list.map((c) => [
      c.id,
      c.tag_id,
      c.name,
      c.breed,
      c.age,
      c.weight,
      c.status,
      c.risk_score || 12,
      c.latest_temperature || '',
      c.latest_heart_rate || ''
    ]);
    const csvContent = [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    downloadCSV(`cattlex_herd_health_${new Date().toISOString().slice(0, 10)}.csv`, csvContent);
  };

  const exportAlertsCSV = async () => {
    const alerts = await api.getAlerts();
    const headers = ['ID', 'Cattle ID', 'Severity', 'Type', 'Status', 'Created At', 'Message'];
    const rows = alerts.map((a) => [
      a.id,
      a.cattle_id,
      a.severity,
      a.type,
      a.status,
      `"${a.created_at}"`,
      `"${a.message.replace(/"/g, '""')}"`
    ]);
    const csvContent = [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    downloadCSV(`cattlex_alerts_audit_${new Date().toISOString().slice(0, 10)}.csv`, csvContent);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
          Analytics &amp; Audit Exports
        </h1>
        <p className="text-xs text-slate-400 mt-1 font-mono">
          Export herd data, IoT sensor history, and clinical diagnosis logs in CSV format
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-xl bg-brand-950/80 border border-brand-800/80 flex items-center justify-center text-brand-400 mb-4">
              <Activity className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Herd Health &amp; Telemetry Export</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Downloads complete record of registered cattle, physiological status classifications, latest sensor values, and computed health risk scores.
            </p>
          </div>
          <button
            onClick={exportCattleHealthCSV}
            className="mt-6 px-4 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 transition-colors self-start"
          >
            <Download className="w-4 h-4" />
            Export Herd CSV
          </button>
        </div>

        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <div className="w-10 h-10 rounded-xl bg-rose-950/80 border border-rose-800/80 flex items-center justify-center text-rose-400 mb-4">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-white">Incident &amp; Triage Alerts Export</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Export all automated alerts triggered by physiological threshold violations (pyrexia, tachycardia, lethargy, dehydration).
            </p>
          </div>
          <button
            onClick={exportAlertsCSV}
            className="mt-6 px-4 py-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-100 font-semibold text-xs flex items-center justify-center gap-2 transition-colors border border-slate-700 self-start"
          >
            <Download className="w-4 h-4" />
            Export Alerts CSV
          </button>
        </div>
      </div>
    </div>
  );
};
