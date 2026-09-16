import React, { useState, useEffect } from 'react';
import { CalendarCheck, UserCheck, Plus, CheckCircle, Clock, AlertTriangle, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

export const VeterinaryPage: React.FC = () => {
  const [appointments, setAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // New appointment form modal state
  const [showModal, setShowModal] = useState(false);
  const [cattleId, setCattleId] = useState(1);
  const [vetName, setVetName] = useState('Dr. Sarah Jenkins, DVM');
  const [priority, setPriority] = useState('HIGH');
  const [reason, setReason] = useState('');

  const loadAppointments = async () => {
    try {
      const data = await api.getAppointments();
      setAppointments(data);
    } catch (err) {
      console.error('Failed to load appointments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  const handleStatusChange = async (id: number, newStatus: string) => {
    try {
      await api.updateAppointment(id, { status: newStatus });
      loadAppointments();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.createAppointment({
        cattle_id: cattleId,
        veterinarian_name: vetName,
        priority: priority,
        reason: reason,
        status: 'SCHEDULED'
      });
      setShowModal(false);
      setReason('');
      loadAppointments();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans">
            Veterinary Consultation &amp; RPA Triage
          </h1>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Automated Clinical Escalation &bull; Diagnostic Dispatch Workflow
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 font-bold text-xs flex items-center gap-1.5 transition-all shadow-md shadow-brand-500/20 self-start"
        >
          <Plus className="w-4 h-4" />
          Schedule Consultation
        </button>
      </div>

      {/* Triage Queue */}
      <div className="space-y-4">
        {appointments.length === 0 ? (
          <div className="glass-panel p-12 text-center rounded-2xl">
            <CheckCircle className="w-10 h-10 text-brand-400 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-slate-200">All Clinical Appointments Cleared</h3>
            <p className="text-xs text-slate-400 mt-1">No pending veterinary consults currently scheduled.</p>
          </div>
        ) : (
          appointments.map((apt) => (
            <div
              key={apt.id}
              className="glass-panel p-5 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4 border border-slate-800"
            >
              <div className="space-y-2">
                <div className="flex items-center gap-3">
                  <span className="px-2.5 py-0.5 rounded font-mono text-[10px] font-bold tracking-wider bg-rose-950/80 text-rose-400 border border-rose-800/80">
                    PRIORITY: {apt.priority}
                  </span>
                  <StatusBadge status={apt.status} size="sm" />
                  <span className="text-xs font-mono text-slate-400">
                    Cattle Tag ID: #{apt.cattle_id}
                  </span>
                </div>

                <p className="text-sm font-semibold text-slate-100">{apt.reason}</p>

                <div className="flex items-center gap-4 text-xs text-slate-400 font-mono">
                  <span>Assigned Clinician: <strong className="text-slate-200">{apt.veterinarian_name}</strong></span>
                  <span>&bull;</span>
                  <span>Scheduled: {new Date(apt.scheduled_at).toLocaleDateString()}</span>
                </div>
              </div>

              {/* Status Update Actions */}
              <div className="flex items-center gap-2 shrink-0">
                {apt.status === 'PENDING' && (
                  <button
                    onClick={() => handleStatusChange(apt.id, 'SCHEDULED')}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700"
                  >
                    Confirm Schedule
                  </button>
                )}
                {apt.status === 'SCHEDULED' && (
                  <button
                    onClick={() => handleStatusChange(apt.id, 'IN_PROGRESS')}
                    className="px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-slate-950 text-xs font-bold"
                  >
                    Begin Examination
                  </button>
                )}
                {apt.status === 'IN_PROGRESS' && (
                  <button
                    onClick={() => handleStatusChange(apt.id, 'COMPLETED')}
                    className="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 text-xs font-bold"
                  >
                    Mark Resolved
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal Dialog for Scheduling */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 rounded-2xl border border-slate-700 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white">Create Veterinary Consultation</h3>

            <form onSubmit={handleCreate} className="space-y-3">
              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Cattle ID (1-5)</label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  value={cattleId}
                  onChange={(e) => setCattleId(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Attending Veterinarian</label>
                <input
                  type="text"
                  value={vetName}
                  onChange={(e) => setVetName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Priority</label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100"
                >
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                  <option value="URGENT">URGENT</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-300 mb-1">Clinical Reason</label>
                <textarea
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="Suspected respiratory infection, elevated pyrexia..."
                  rows={3}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-100"
                  required
                />
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-brand-600 hover:bg-brand-500 text-slate-950 text-xs font-bold"
                >
                  Confirm Appointment
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
