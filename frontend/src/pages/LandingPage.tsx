import React from 'react';
import { Link } from 'react-router-dom';
import {
  Radio,
  BrainCircuit,
  Activity,
  ShieldAlert,
  CalendarCheck,
  Sun,
  FileCheck,
  ArrowRight,
  Database,
  CheckCircle2,
  ChevronRight
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-brand-500 selection:text-white">
      {/* Top Navbar */}
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
              <Radio className="w-5 h-5 text-slate-950 font-bold" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight font-sans text-white">CATTLEX</span>
              <span className="ml-2 text-xs font-mono px-2 py-0.5 rounded bg-brand-500/20 text-brand-400 border border-brand-500/30">
                Production AI
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/dashboard"
              className="px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-white text-sm font-semibold transition-all shadow-md shadow-brand-600/20 flex items-center gap-1.5"
            >
              Open Dashboard
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-16 pb-20 px-6 overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-1/3 left-1/4 w-80 h-80 bg-sky-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-700 text-xs text-brand-400 mb-6 font-mono">
            <Sun className="w-3.5 h-3.5 text-amber-400 animate-spin" />
            Solar-Powered Smart Collar IoT + Multiclass Machine Learning
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight font-sans">
            AI-Integrated Livestock Health & <br />
            <span className="bg-gradient-to-r from-brand-400 via-emerald-300 to-sky-400 bg-clip-text text-transparent">
              Multi-Disease Predictive Analytics
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-3xl mx-auto leading-relaxed">
            CATTLEX is an end-to-end cattle intelligence system uniting autonomous solar collars,
            real-time physiological vital signs inference, and multiclass disease diagnosis across 26 bovine conditions.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              to="/dashboard"
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-slate-950 font-bold text-base transition-all shadow-lg shadow-brand-500/25 flex items-center gap-2"
            >
              Launch Live Dashboard
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/prediction"
              className="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-base transition-all flex items-center gap-2"
            >
              <BrainCircuit className="w-5 h-5 text-brand-400" />
              Test Disease Prediction
            </Link>
          </div>

          {/* Academic Badge */}
          <div className="mt-12 p-4 rounded-xl bg-slate-900/60 border border-slate-800/80 max-w-2xl mx-auto flex items-center justify-center gap-3 text-xs text-slate-400 font-mono">
            <FileCheck className="w-4 h-4 text-brand-400 shrink-0" />
            <span>
              Validated Multi-Disease Classification &bull; 433 Unique Clinical Symptom Signatures &bull; 26 Conditions
            </span>
          </div>
        </div>
      </section>

      {/* Core Architectural Pillars */}
      <section className="py-16 px-6 max-w-7xl mx-auto w-full">
        <div className="text-center mb-12">
          <h2 className="text-xs uppercase font-mono tracking-widest text-brand-400">System Architecture</h2>
          <p className="text-2xl sm:text-3xl font-bold text-slate-100 mt-1 font-sans">
            Autonomous Health Intelligence at Every Layer
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Card 1 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-brand-950/60 border border-brand-800/60 flex items-center justify-center text-brand-400 mb-4 group-hover:scale-105 transition-transform">
              <BrainCircuit className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Multi-Disease ML Model</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              Trained on 2,044 clinical records and 93 symptom signals. Benchmarks Random Forest against Gaussian NB, Decision Tree, Logistic Regression, k-NN, and SVM.
            </p>
          </div>

          {/* Card 2 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-sky-950/60 border border-sky-800/60 flex items-center justify-center text-sky-400 mb-4 group-hover:scale-105 transition-transform">
              <Radio className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Solar Collar IoT Ingestion</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              Simulated & physical IoT architecture capturing MLX90614 body temperature, MAX30102 heart rate, MPU6050 rumination activity, load cell feed, and flow meter water intake.
            </p>
          </div>

          {/* Card 3 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-amber-950/60 border border-amber-800/60 flex items-center justify-center text-amber-400 mb-4 group-hover:scale-105 transition-transform">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Vital Risk Scoring Engine</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              Continuously grades physiological deviations against veterinary bovine reference ranges, producing clear health classifications: HEALTHY, AT_RISK, or CRITICAL.
            </p>
          </div>

          {/* Card 4 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-rose-950/60 border border-rose-800/60 flex items-center justify-center text-rose-400 mb-4 group-hover:scale-105 transition-transform">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Automated Triage & Alerts</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              Multi-condition threshold evaluation flags pyrexia, tachycardia, lethargy, and nutritional collapse, instantly broadcasting alerts to farmer devices.
            </p>
          </div>

          {/* Card 5 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-purple-950/60 border border-purple-800/60 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
              <CalendarCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Veterinary RPA Workflow</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              When cattle risk spikes, the system automatically dispatches clinical triage tickets, assigns veterinary personnel, and sets diagnostic priority.
            </p>
          </div>

          {/* Card 6 */}
          <div className="glass-panel p-6 rounded-2xl hover:border-slate-700 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-emerald-950/60 border border-emerald-800/60 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-105 transition-transform">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Explainable AI (XAI)</h3>
            <p className="text-sm text-slate-400 mt-2 leading-relaxed">
              Transparent Gini feature importance attribution reveals exactly which clinical signs drove each multi-disease prediction without opaque black-box outputs.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-8 px-6 text-center text-xs text-slate-500 font-mono">
        <p>CATTLEX Research Platform &bull; Solar-Powered IoT &amp; AI-Integrated Multi-Disease Management</p>
        <p className="mt-1 text-slate-600">Decision-support research prototype. Certified veterinary evaluation required for clinical diagnosis.</p>
      </footer>
    </div>
  );
};
