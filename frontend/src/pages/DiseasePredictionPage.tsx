import React, { useState, useEffect } from 'react';
import {
  Stethoscope,
  BrainCircuit,
  Search,
  CheckCircle2,
  AlertTriangle,
  Info,
  Sparkles,
  BarChart2,
  FileCheck2,
  RotateCcw
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { api } from '../services/api';

export const DiseasePredictionPage: React.FC = () => {
  const [cattleList, setCattleList] = useState<any[]>([]);
  const [selectedCattleId, setSelectedCattleId] = useState<number>(1);
  const [selectedModel, setSelectedModel] = useState<string>('Random Forest');

  const [symptoms, setSymptoms] = useState<{ key: string; display_name: string }[]>([]);
  const [activeSymptoms, setActiveSymptoms] = useState<Record<string, boolean>>({});
  const [searchTerm, setSearchTerm] = useState('');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const initData = async () => {
      try {
        const [cattleRes, symRes] = await Promise.all([
          api.getCattleList(),
          api.getFeatures().catch(() => api.getSymptoms())
        ]);
        setCattleList(cattleRes);
        if (cattleRes.length > 0) setSelectedCattleId(cattleRes[0].id);
        setSymptoms(symRes.symptoms);
      } catch (err) {
        console.error('Failed to initialize symptoms:', err);
      }
    };
    initData();
  }, []);

  const toggleSymptom = (key: string) => {
    setActiveSymptoms((prev) => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleClear = () => {
    setActiveSymptoms({});
    setResult(null);
  };

  // Preset symptom packages for quick academic evaluation
  const loadPreset = (presetName: string) => {
    const presets: Record<string, string[]> = {
      mastitis: ['fever', 'loss_of_appetite', 'udder_swelling', 'udder_heat', 'udder_pain', 'milk_flakes', 'milk_clots', 'reduction_milk_vields'],
      pneumonia: ['fever', 'coughing', 'diffculty_breath', 'nasel_discharges', 'rapid_breathing', 'shallow_breathing', 'depression'],
      bloat: ['abdominal_pain', 'colic', 'gaseous_stomach', 'moaning', 'unwillingness_to_move', 'bellowing'],
      foot_and_mouth: ['fever', 'blisters', 'drooling', 'frothing_of_mouth', 'lameness', 'salivation', 'ulcers']
    };

    const targetList = presets[presetName] || [];
    const newMap: Record<string, boolean> = {};
    targetList.forEach((s) => (newMap[s] = true));
    setActiveSymptoms(newMap);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const activeCount = Object.values(activeSymptoms).filter(Boolean).length;
    if (activeCount === 0) {
      alert('Please select at least 1 or 2 clinical symptoms.');
      return;
    }

    setLoading(true);
    try {
      const res = await api.predictDisease(selectedCattleId, activeSymptoms, selectedModel);
      setResult(res);
    } catch (err) {
      console.error('Prediction failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredSymptoms = symptoms.filter((s) =>
    s.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.key.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const activeCount = Object.values(activeSymptoms).filter(Boolean).length;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
          Symptom-Based Multi-Disease Prediction Engine
        </h1>
        <p className="text-xs text-slate-400 mt-1 font-mono">
          Decision-Support Classifier &bull; 93 Clinical Indicators &bull; 26 Target Conditions
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Form & Symptom Selection */}
        <div className="lg:col-span-7 space-y-6">
          <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-2xl space-y-5">
            {/* Configuration Selectors */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5 font-mono">
                  Select Cattle
                </label>
                <select
                  value={selectedCattleId}
                  onChange={(e) => setSelectedCattleId(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500 font-medium"
                >
                  {cattleList.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.tag_id} - {c.name} ({c.breed})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5 font-mono">
                  ML Algorithm
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500 font-medium"
                >
                  <option value="Random Forest">Random Forest (Primary - 100% CV)</option>
                  <option value="Gaussian Naive Bayes">Gaussian Naive Bayes</option>
                  <option value="Decision Tree">Decision Tree</option>
                  <option value="Logistic Regression">Logistic Regression</option>
                  <option value="k-NN">k-Nearest Neighbors (k-NN)</option>
                  <option value="Support Vector Machine">Support Vector Machine (SVM)</option>
                </select>
              </div>
            </div>

            {/* Presets Strip */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] uppercase tracking-wider font-mono text-slate-400">
                  Quick Clinical Presets:
                </span>
                <span className="text-xs font-mono text-brand-400">
                  {activeCount} symptom(s) selected
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => loadPreset('mastitis')}
                  className="px-2.5 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs text-slate-300 transition-colors"
                >
                  Bovine Mastitis
                </button>
                <button
                  type="button"
                  onClick={() => loadPreset('pneumonia')}
                  className="px-2.5 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs text-slate-300 transition-colors"
                >
                  Calf Pneumonia
                </button>
                <button
                  type="button"
                  onClick={() => loadPreset('bloat')}
                  className="px-2.5 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs text-slate-300 transition-colors"
                >
                  Rumen Bloat
                </button>
                <button
                  type="button"
                  onClick={() => loadPreset('foot_and_mouth')}
                  className="px-2.5 py-1 rounded-md bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs text-slate-300 transition-colors"
                >
                  Foot &amp; Mouth
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  className="px-2.5 py-1 rounded-md bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/60 text-xs text-rose-300 transition-colors flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" /> Clear
                </button>
              </div>
            </div>

            {/* Symptom Search Bar */}
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search symptoms (e.g. fever, coughing, udder pain, diarrhea)..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-brand-500"
              />
            </div>

            {/* 93 Symptoms Interactive Multi-Select Chips */}
            <div className="border border-slate-800 rounded-xl p-3 bg-slate-950/60 max-h-80 overflow-y-auto">
              <div className="flex flex-wrap gap-1.5">
                {filteredSymptoms.map((sym) => {
                  const isChecked = !!activeSymptoms[sym.key];
                  return (
                    <button
                      key={sym.key}
                      type="button"
                      onClick={() => toggleSymptom(sym.key)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all text-left flex items-center gap-1.5 ${
                        isChecked
                          ? 'bg-brand-600 text-slate-950 font-bold shadow-sm shadow-brand-500/20'
                          : 'bg-slate-900 hover:bg-slate-850 text-slate-300 border border-slate-800'
                      }`}
                    >
                      <span
                        className={`w-2 h-2 rounded-full ${
                          isChecked ? 'bg-slate-950' : 'bg-slate-600'
                        }`}
                      />
                      {sym.display_name}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-slate-950 font-bold text-sm transition-all shadow-lg shadow-brand-500/25 flex items-center justify-center gap-2"
            >
              <BrainCircuit className="w-5 h-5" />
              {loading ? 'Evaluating Model Inference...' : 'Execute Disease Prediction'}
            </button>
          </form>
        </div>

        {/* Right Column: Predictive Results & Explainable AI */}
        <div className="lg:col-span-5 space-y-6">
          {!result ? (
            <div className="glass-panel p-8 rounded-2xl text-center flex flex-col items-center justify-center h-full min-h-[400px]">
              <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500 mb-4">
                <Stethoscope className="w-8 h-8" />
              </div>
              <h3 className="text-base font-bold text-slate-200">Awaiting Clinical Symptoms</h3>
              <p className="text-xs text-slate-400 mt-2 max-w-sm leading-relaxed">
                Select observed symptoms on the left or click a preset, then trigger the predictive inference engine.
              </p>
            </div>
          ) : (
            <div className="glass-panel p-6 rounded-2xl space-y-6 animate-fadeIn">
              {/* Prediction Banner */}
              <div className="p-4 rounded-xl bg-gradient-to-br from-slate-900 to-slate-850 border border-brand-500/30">
                <span className="text-[10px] uppercase font-mono tracking-wider text-brand-400 block mb-1">
                  Primary Differential Prediction
                </span>
                <div className="flex items-baseline justify-between">
                  <h2 className="text-2xl font-bold text-white font-sans">
                    {result.display_name}
                  </h2>
                  <span className="text-xl font-extrabold font-mono text-brand-400">
                    {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 font-mono mt-1">
                  Algorithm: {result.model_name}
                </p>
              </div>

              {/* Top 3 Differential Diagnoses Chart */}
              <div>
                <h4 className="text-xs uppercase font-mono tracking-wider text-slate-300 mb-3 flex items-center gap-1.5">
                  <BarChart2 className="w-4 h-4 text-sky-400" />
                  Top 3 Differential Diagnoses
                </h4>
                <div className="h-40">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={result.top_predictions.map((p: any) => ({
                        name: p.display_name,
                        prob: Math.round(p.probability * 100)
                      }))}
                      layout="vertical"
                      margin={{ left: 10, right: 30, top: 5, bottom: 5 }}
                    >
                      <XAxis type="number" domain={[0, 100]} unit="%" stroke="#64748b" fontSize={10} />
                      <YAxis type="category" dataKey="name" width={110} stroke="#94a3b8" fontSize={10} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }} />
                      <Bar dataKey="prob" radius={[0, 4, 4, 0]}>
                        {result.top_predictions.map((_: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={index === 0 ? '#22c55e' : index === 1 ? '#38bdf8' : '#818cf8'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Explainable AI: Feature Signals */}
              {result.important_features?.length > 0 && (
                <div>
                  <h4 className="text-xs uppercase font-mono tracking-wider text-slate-300 mb-3 flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-amber-400" />
                    Key Contributing Symptoms (XAI Attribution)
                  </h4>
                  <div className="space-y-2">
                    {result.important_features.slice(0, 5).map((feat: any, idx: number) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 flex items-center justify-between text-xs">
                        <span className="text-slate-200">{feat.display_name}</span>
                        <span className="font-mono text-[11px] text-amber-400 font-semibold">
                          Importance: {(feat.importance * 100).toFixed(2)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Clinical Recommendation */}
              <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
                <span className="text-[11px] uppercase font-mono tracking-wider text-slate-400 block mb-1">
                  Automated Recommendation
                </span>
                <p className="text-xs text-slate-200 leading-relaxed font-sans">
                  {result.recommendation}
                </p>
              </div>

              {/* Safety Disclaimer */}
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800/80 text-[11px] text-slate-400 flex items-start gap-2">
                <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                <span>{result.disclaimer}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
