const API_BASE = '/api';

export async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('cattlex_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { ...options, headers });
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API error (${response.status}): ${errorBody}`);
  }
  return response.json();
}

export const api = {
  // Auth
  login: (data: any) => fetchJson<any>(`${API_BASE}/auth/login`, { method: 'POST', body: JSON.stringify(data) }),
  register: (data: any) => fetchJson<any>(`${API_BASE}/auth/register`, { method: 'POST', body: JSON.stringify(data) }),

  // Dashboard
  getDashboardSummary: () => fetchJson<any>(`${API_BASE}/dashboard/summary`),
  getHerdTrends: (cattleId?: number) => fetchJson<any>(`${API_BASE}/dashboard/trends${cattleId ? `?cattle_id=${cattleId}` : ''}`),

  // Cattle
  getCattleList: () => fetchJson<any[]>(`${API_BASE}/cattle`),
  getCattleProfile: (id: number) => fetchJson<any>(`${API_BASE}/cattle/${id}`),
  addCattle: (data: any) => fetchJson<any>(`${API_BASE}/cattle`, { method: 'POST', body: JSON.stringify(data) }),
  updateCattle: (id: number, data: any) => fetchJson<any>(`${API_BASE}/cattle/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Sensors & Telemetry
  getSensorHistory: (cattleId: number) => fetchJson<any[]>(`${API_BASE}/sensors/${cattleId}`),
  getLatestSensor: (cattleId: number) => fetchJson<any>(`${API_BASE}/sensors/${cattleId}/latest`),
  ingestReading: (data: any) => fetchJson<any>(`${API_BASE}/sensors/readings`, { method: 'POST', body: JSON.stringify(data) }),

  // Diseases & Predictions
  getSymptoms: () => fetchJson<{ count: number; symptoms: { key: string; display_name: string }[] }>(`${API_BASE}/diseases/symptoms`),
  getDiseaseClasses: () => fetchJson<any>(`${API_BASE}/diseases/classes`),
  predictDisease: (cattleId: number, symptoms: Record<string, boolean>, modelName = 'Random Forest') =>
    fetchJson<any>(`${API_BASE}/predictions/disease`, {
      method: 'POST',
      body: JSON.stringify({ cattle_id: cattleId, symptoms, model_name: modelName }),
    }),
  getPredictionHistory: (cattleId: number) => fetchJson<any>(`${API_BASE}/predictions/${cattleId}`),

  // Alerts
  getAlerts: (status?: string) => fetchJson<any[]>(`${API_BASE}/alerts${status ? `?status=${status}` : ''}`),
  resolveAlert: (alertId: number) => fetchJson<any>(`${API_BASE}/alerts/${alertId}/resolve`, { method: 'POST' }),

  // Veterinary
  getAppointments: (status?: string) => fetchJson<any[]>(`${API_BASE}/veterinarians/appointments${status ? `?status=${status}` : ''}`),
  createAppointment: (data: any) => fetchJson<any>(`${API_BASE}/veterinarians/appointments`, { method: 'POST', body: JSON.stringify(data) }),
  updateAppointment: (id: number, data: any) => fetchJson<any>(`${API_BASE}/veterinarians/appointments/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Models & Registry
  getModelPerformance: () => fetchJson<any>(`${API_BASE}/models/performance`),
  getModelRegistry: () => fetchJson<any>(`${API_BASE}/models`),

  // IoT Simulator
  getSimulatorStatus: () => fetchJson<any>(`${API_BASE}/simulator/status`),
  startSimulator: () => fetchJson<any>(`${API_BASE}/simulator/start`, { method: 'POST' }),
  stopSimulator: () => fetchJson<any>(`${API_BASE}/simulator/stop`, { method: 'POST' }),
  triggerAbnormal: (tagId: string) => fetchJson<any>(`${API_BASE}/simulator/trigger-abnormal`, { method: 'POST', body: JSON.stringify({ tag_id: tagId }) }),
  resetSimulator: () => fetchJson<any>(`${API_BASE}/simulator/reset`, { method: 'POST' }),
};
