export interface Cattle {
  id: number;
  tag_id: string;
  name: string;
  breed: string;
  age: number;
  sex: string;
  weight: number;
  farm_id: string;
  status: 'HEALTHY' | 'AT_RISK' | 'CRITICAL';
  created_at: string;
  updated_at: string;
  latest_temperature?: number;
  latest_heart_rate?: number;
  latest_activity?: number;
  risk_score?: number;
  active_alerts_count?: number;
}

export interface SensorReading {
  id?: number;
  cattle_id: number;
  temperature: number;
  heart_rate: number;
  respiratory_rate: number;
  activity_level: number;
  feed_intake: number;
  water_intake: number;
  ambient_temperature?: number;
  humidity?: number;
  timestamp: string;
}

export interface DiseaseProbability {
  disease: string;
  display_name: string;
  probability: number;
}

export interface ImportantFeature {
  feature: string;
  display_name: string;
  importance: number;
  present: boolean;
}

export interface DiseasePredictionResponse {
  cattle_id: number;
  predicted_disease: string;
  display_name: string;
  confidence: number;
  model_name: string;
  top_predictions: DiseaseProbability[];
  important_features: ImportantFeature[];
  recommendation: string;
  disclaimer: string;
  timestamp: string;
}

export interface Alert {
  id: number;
  cattle_id: number;
  type: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  message: string;
  status: 'ACTIVE' | 'RESOLVED' | 'DISMISSED';
  created_at: string;
  resolved_at?: string;
}

export interface VeterinaryAppointment {
  id: number;
  cattle_id: number;
  veterinarian_name: string;
  reason: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT';
  scheduled_at: string;
  status: 'PENDING' | 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  notes?: string;
  created_at: string;
}

export interface DashboardSummary {
  kpis: {
    total_cattle: number;
    healthy: number;
    at_risk: number;
    critical: number;
    active_alerts: number;
  };
  average_vitals: {
    temperature: number;
    heart_rate: number;
    respiratory_rate: number;
    activity_level: number;
    feed_intake: number;
    water_intake: number;
  };
  recent_alerts: Alert[];
  recent_predictions: any[];
}
