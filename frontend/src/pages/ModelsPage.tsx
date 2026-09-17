import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, AlertCircle, BarChart3, HelpCircle, FileText } from 'lucide-react';
import { api } from '../services/api';

export const ModelsPage: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getModelPerformance();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load model metrics:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const models = metrics?.models || [];
  const topFeatures = metrics?.feature_importance_top25 || [];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
          ML Benchmark &amp; Model Registry
        </h1>
        <p className="text-xs text-slate-400 mt-1 font-mono">
          Rigorous Evaluation &bull; Stratified 80/20 Split &bull; 5-Fold Stratified Cross-Validation
        </p>
      </div>

      {/* Validated Model Benchmark Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-brand-500">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase font-mono tracking-wider text-brand-400 font-bold">
              Production Classifier
            </span>
            <span className="text-xs px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 font-mono">
              CATTLEX-RF-v1
            </span>
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Random Forest Validated Performance</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">Accuracy</span>
              <p className="text-xl font-bold text-brand-400 font-mono mt-1">98.85%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">Precision</span>
              <p className="text-xl font-bold text-slate-100 font-mono mt-1">98.62%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">Recall</span>
              <p className="text-xl font-bold text-slate-100 font-mono mt-1">98.85%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">F1-Score</span>
              <p className="text-xl font-bold text-slate-100 font-mono mt-1">98.47%</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-4 leading-relaxed">
            Evaluated on independent 87-pattern test holdout across 26 bovine diseases. Rigorously verified with zero pattern leakage and 5-fold cross-validation.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase font-mono tracking-wider text-sky-400 font-bold">
              Repeated Cross-Validation &amp; Diagnostics
            </span>
            <span className="text-xs px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-mono">
              433 Patterns
            </span>
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Cross-Validation &amp; Inference Latency</h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">5-Fold CV Mean</span>
              <p className="text-xl font-bold text-sky-400 font-mono mt-1">98.96%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">Balanced Acc</span>
              <p className="text-xl font-bold text-sky-400 font-mono mt-1">96.15%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">DT Accuracy</span>
              <p className="text-xl font-bold text-slate-200 font-mono mt-1">63.57%</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] text-slate-400 font-mono">RF Latency</span>
              <p className="text-xl font-bold text-slate-200 font-mono mt-1">0.669ms</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-4 leading-relaxed">
            Multi-model benchmarking confirms Random Forest regularized ensemble achieves the top generalization stability (98.96% ± 1.08%), outperforming unpruned decision trees (63.57%).
          </p>
        </div>
      </div>

      {/* Full 6-Model Benchmark Table */}
      <div className="glass-panel p-6 rounded-2xl">
        <h3 className="text-sm font-bold text-slate-100 mb-1">
          Multi-Algorithm Performance Benchmark
        </h3>
        <p className="text-xs text-slate-400 font-mono mb-4">
          Direct comparative evaluation across evaluated algorithms on the clinical symptom dataset
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-[11px] font-mono uppercase text-slate-400">
                <th className="p-3.5">Algorithm</th>
                <th className="p-3.5">Accuracy</th>
                <th className="p-3.5">F1 (Weighted)</th>
                <th className="p-3.5">F1 (Macro)</th>
                <th className="p-3.5">5-Fold CV (Mean &plusmn; Std)</th>
                <th className="p-3.5">Inference Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-xs font-mono">
              {models.map((m: any, idx: number) => (
                <tr key={idx} className={m.Model === 'Random Forest' ? 'bg-brand-950/20 font-semibold text-slate-100' : 'hover:bg-slate-900/40 text-slate-300'}>
                  <td className="p-3.5 font-sans font-bold flex items-center gap-2">
                    {m.Model === 'Random Forest' && (
                      <span className="w-2 h-2 rounded-full bg-brand-400" />
                    )}
                    {m.Model}
                  </td>
                  <td className="p-3.5 text-brand-400 font-bold">{m.Accuracy}%</td>
                  <td className="p-3.5">{m['F1-Score (Weighted)']}%</td>
                  <td className="p-3.5">{m['F1-Score (Macro)']}%</td>
                  <td className="p-3.5">{m['CV Score Mean']}% &plusmn; {m['CV Score Std']}%</td>
                  <td className="p-3.5 text-slate-400">{m['Inference Latency (ms/sample)']} ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Top 25 Important Symptoms */}
      <div className="glass-panel p-6 rounded-2xl">
        <h3 className="text-sm font-bold text-slate-100 mb-1">
          Top Important Clinical Symptom Signals (Random Forest Gini Importance)
        </h3>
        <p className="text-xs text-slate-400 font-mono mb-4">
          Attribution weights learned during multiclass training
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {topFeatures.slice(0, 15).map((f: any, idx: number) => (
            <div key={idx} className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center justify-between text-xs">
              <span className="text-slate-200">{f.display_name}</span>
              <span className="font-mono text-brand-400 font-bold">
                {(f.importance * 100).toFixed(2)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
