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
  getFeatures: () => fetchJson<{ count: number; features: string[]; symptoms: { key: string; display_name: string }[] }>(`${API_BASE}/v1/predictions/features`),
  getSymptoms: () => fetchJson<{ count: number; symptoms: { key: string; display_name: string }[] }>(`${API_BASE}/diseases/symptoms`),
  getDiseaseClasses: () => fetchJson<any>(`${API_BASE}/diseases/classes`),
  predictDisease: (cattleId: any, symptoms: Record<string, any>, modelName = 'Random Forest') =>
    fetchJson<any>(`${API_BASE}/v1/predictions/disease`, {
      method: 'POST',
      body: JSON.stringify({ cattle_id: cattleId, symptoms, model_name: modelName }),
    }),
  getPredictionHistory: (cattleId: any) => fetchJson<any>(`${API_BASE}/predictions/${cattleId}`),

  // Alerts
  getAlerts: (status?: string, severity?: string) => 
    fetchJson<any[]>(`${API_BASE}/v1/alerts${status ? `?status=${status}` : ''}${severity ? `&severity=${severity}` : ''}`),
  acknowledgeAlert: (alertId: number) => fetchJson<any>(`${API_BASE}/v1/alerts/${alertId}/acknowledge`, { method: 'POST' }),
  resolveAlert: (alertId: number) => fetchJson<any>(`${API_BASE}/v1/alerts/${alertId}/resolve`, { method: 'POST' }),

  // Veterinary
  getAppointments: (status?: string) => fetchJson<any[]>(`${API_BASE}/veterinarians/appointments${status ? `?status=${status}` : ''}`),
  createAppointment: (data: any) => fetchJson<any>(`${API_BASE}/veterinarians/appointments`, { method: 'POST', body: JSON.stringify(data) }),
  updateAppointment: (id: number, data: any) => fetchJson<any>(`${API_BASE}/veterinarians/appointments/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Models & Registry
  getModelInfo: () => fetchJson<any>(`${API_BASE}/v1/ml/model-info`),
  getModelPerformance: () => fetchJson<any>(`${API_BASE}/models/performance`),
  getModelRegistry: () => fetchJson<any>(`${API_BASE}/models`),

  // Analytics & Explainability
  getAnalyticsOverview: (days = 30) => fetchJson<any>(`${API_BASE}/v1/analytics/overview?days=${days}`),
  getDiseaseAnalytics: (days = 30) => fetchJson<any>(`${API_BASE}/v1/analytics/diseases?days=${days}`),
  getFeatureImportance: (top_n = 20) => fetchJson<any>(`${API_BASE}/v1/analytics/feature-importance?top_n=${top_n}`),
  getHealthAnalytics: (days = 7) => fetchJson<any>(`${API_BASE}/v1/analytics/health?days=${days}`),

  // IoT Simulator
  getSimulatorStatus: () => fetchJson<any>(`${API_BASE}/v1/simulation/status`),
  startSimulator: (scenario = 'NORMAL', interval = 4.0) => 
    fetchJson<any>(`${API_BASE}/v1/simulation/start`, { 
      method: 'POST', 
      body: JSON.stringify({ scenario, interval_seconds: interval }) 
    }),
  stopSimulator: () => fetchJson<any>(`${API_BASE}/v1/simulation/stop`, { method: 'POST' }),
  triggerAbnormal: (tagId: string) => fetchJson<any>(`${API_BASE}/v1/simulation/trigger-abnormal`, { method: 'POST', body: JSON.stringify({ tag_id: tagId }) }),
  resetSimulator: () => fetchJson<any>(`${API_BASE}/v1/simulation/reset`, { method: 'POST' }),

  // Health
  getHealth: () => fetchJson<any>(`${API_BASE}/v1/health`),
  getReadiness: () => fetchJson<any>(`${API_BASE}/v1/health/readiness`),
  deleteCattle: (id: any) => fetchJson<any>(`${API_BASE}/cattle/${id}`, { method: 'DELETE' }),
};
