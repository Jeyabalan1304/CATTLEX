"""
CATTLEX - Transparent Health-Risk Engine
Computes explainable bovine health risk scores (0 to 100) and classifications
based on physiological vital signs and veterinary clinical deviation thresholds.
Distinct from the disease classification engine.
"""

from typing import Dict, Any, List

class HealthRiskEngine:
    """
    Transparent, explainable bovine physiological risk calculation:
    - 0 to 35: HEALTHY
    - 36 to 70: AT_RISK
    - 71 to 100: CRITICAL
    """

    # Bovine physiological reference ranges (Dairy & Beef cattle standards)
    NORMAL_TEMP_MIN = 38.0
    NORMAL_TEMP_MAX = 39.3
    FEVER_CRITICAL = 40.2
    HYPOTHERMIA_CRITICAL = 37.0

    NORMAL_HR_MIN = 48.0
    NORMAL_HR_MAX = 84.0
    TACHYCARDIA_CRITICAL = 100.0
    BRADYCARDIA_CRITICAL = 40.0

    NORMAL_RR_MIN = 24.0
    NORMAL_RR_MAX = 36.0
    TACHYPNEA_CRITICAL = 48.0
    BRADYPNEA_CRITICAL = 14.0

    NORMAL_ACTIVITY_MIN = 0.65
    LETHARGY_CRITICAL = 0.25

    NORMAL_FEED_MIN = 14.0  # kg/day
    ANOREXIA_CRITICAL = 6.0

    NORMAL_WATER_MIN = 40.0 # L/day
    DEHYDRATION_CRITICAL = 20.0

    def calculate_risk(self, telemetry: Dict[str, float]) -> Dict[str, Any]:
        temp = float(telemetry.get("temperature", 38.6))
        hr = float(telemetry.get("heart_rate", 64.0))
        rr = float(telemetry.get("respiratory_rate", 26.0))
        act = float(telemetry.get("activity", telemetry.get("activity_level", 0.85)))
        feed = float(telemetry.get("feed_intake", 19.0))
        water = float(telemetry.get("water_intake", 65.0))
        amb_temp = float(telemetry.get("ambient_temperature", 24.0))
        humidity = float(telemetry.get("humidity", 60.0))

        factors: List[Dict[str, Any]] = []
        raw_score = 0.0

        # 1. Temperature evaluation (Weight: up to 35 points)
        temp_contrib = 0.0
        if temp > self.FEVER_CRITICAL:
            temp_contrib = min(35.0, 25.0 + (temp - self.FEVER_CRITICAL) * 10.0)
            factors.append({
                "factor": "temperature",
                "contribution": round(temp_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Severe pyrexia/fever ({temp:.1f}°C > {self.FEVER_CRITICAL}°C threshold)"
            })
        elif temp > self.NORMAL_TEMP_MAX:
            temp_contrib = ((temp - self.NORMAL_TEMP_MAX) / (self.FEVER_CRITICAL - self.NORMAL_TEMP_MAX)) * 22.0
            factors.append({
                "factor": "temperature",
                "contribution": round(temp_contrib, 1),
                "severity": "WARNING",
                "detail": f"Elevated temperature ({temp:.1f}°C > {self.NORMAL_TEMP_MAX}°C normal)"
            })
        elif temp < self.HYPOTHERMIA_CRITICAL:
            temp_contrib = 30.0
            factors.append({
                "factor": "temperature",
                "contribution": round(temp_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Severe hypothermia ({temp:.1f}°C < {self.HYPOTHERMIA_CRITICAL}°C)"
            })
        elif temp < self.NORMAL_TEMP_MIN:
            temp_contrib = 15.0
            factors.append({
                "factor": "temperature",
                "contribution": round(temp_contrib, 1),
                "severity": "WARNING",
                "detail": f"Subnormal temperature ({temp:.1f}°C < {self.NORMAL_TEMP_MIN}°C)"
            })
        raw_score += temp_contrib

        # 2. Heart rate evaluation (Weight: up to 25 points)
        hr_contrib = 0.0
        if hr > self.TACHYCARDIA_CRITICAL:
            hr_contrib = min(25.0, 18.0 + (hr - self.TACHYCARDIA_CRITICAL) * 0.5)
            factors.append({
                "factor": "heart_rate",
                "contribution": round(hr_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Tachycardia ({hr:.0f} bpm > {self.TACHYCARDIA_CRITICAL} bpm critical threshold)"
            })
        elif hr > self.NORMAL_HR_MAX:
            hr_contrib = ((hr - self.NORMAL_HR_MAX) / (self.TACHYCARDIA_CRITICAL - self.NORMAL_HR_MAX)) * 16.0
            factors.append({
                "factor": "heart_rate",
                "contribution": round(hr_contrib, 1),
                "severity": "WARNING",
                "detail": f"Elevated pulse ({hr:.0f} bpm > {self.NORMAL_HR_MAX} bpm normal)"
            })
        elif hr < self.BRADYCARDIA_CRITICAL:
            hr_contrib = 22.0
            factors.append({
                "factor": "heart_rate",
                "contribution": round(hr_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Bradycardia ({hr:.0f} bpm < {self.BRADYCARDIA_CRITICAL} bpm)"
            })
        raw_score += hr_contrib

        # 3. Respiratory rate evaluation (Weight: up to 20 points)
        rr_contrib = 0.0
        if rr > self.TACHYPNEA_CRITICAL:
            rr_contrib = min(20.0, 14.0 + (rr - self.TACHYPNEA_CRITICAL) * 0.5)
            factors.append({
                "factor": "respiratory_rate",
                "contribution": round(rr_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Tachypnea / labored breathing ({rr:.0f} bpm > {self.TACHYPNEA_CRITICAL} bpm)"
            })
        elif rr > self.NORMAL_RR_MAX:
            rr_contrib = ((rr - self.NORMAL_RR_MAX) / (self.TACHYPNEA_CRITICAL - self.NORMAL_RR_MAX)) * 12.0
            factors.append({
                "factor": "respiratory_rate",
                "contribution": round(rr_contrib, 1),
                "severity": "WARNING",
                "detail": f"Rapid breathing ({rr:.0f} bpm > {self.NORMAL_RR_MAX} bpm)"
            })
        elif rr < self.BRADYPNEA_CRITICAL:
            rr_contrib = 18.0
            factors.append({
                "factor": "respiratory_rate",
                "contribution": round(rr_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Depressed respiration ({rr:.0f} bpm < {self.BRADYPNEA_CRITICAL} bpm)"
            })
        raw_score += rr_contrib

        # 4. Activity evaluation (Weight: up to 25 points)
        act_contrib = 0.0
        if act < self.LETHARGY_CRITICAL:
            act_contrib = 25.0
            factors.append({
                "factor": "activity",
                "contribution": round(act_contrib, 1),
                "severity": "CRITICAL",
                "detail": f"Severe lethargy / immobility ({act:.2f} < {self.LETHARGY_CRITICAL})"
            })
        elif act < self.NORMAL_ACTIVITY_MIN:
            act_contrib = ((self.NORMAL_ACTIVITY_MIN - act) / (self.NORMAL_ACTIVITY_MIN - self.LETHARGY_CRITICAL)) * 18.0
            factors.append({
                "factor": "activity",
                "contribution": round(act_contrib, 1),
                "severity": "WARNING",
                "detail": f"Subdued movement ({act:.2f} < {self.NORMAL_ACTIVITY_MIN})"
            })
        raw_score += act_contrib

        # 5. Nutritional Intake (Feed & Water) (Weight: up to 20 points)
        nutr_contrib = 0.0
        if feed < self.ANOREXIA_CRITICAL:
            nutr_contrib += 12.0
            factors.append({
                "factor": "feed_intake",
                "contribution": 12.0,
                "severity": "CRITICAL",
                "detail": f"Acute anorexia / reduced feed ({feed:.1f} kg < {self.ANOREXIA_CRITICAL} kg)"
            })
        elif feed < self.NORMAL_FEED_MIN:
            nutr_contrib += 6.0
            factors.append({
                "factor": "feed_intake",
                "contribution": 6.0,
                "severity": "WARNING",
                "detail": f"Reduced daily feed intake ({feed:.1f} kg < {self.NORMAL_FEED_MIN} kg)"
            })

        if water < self.DEHYDRATION_CRITICAL:
            nutr_contrib += 10.0
            factors.append({
                "factor": "water_intake",
                "contribution": 10.0,
                "severity": "CRITICAL",
                "detail": f"Severe dehydration risk ({water:.1f} L < {self.DEHYDRATION_CRITICAL} L)"
            })
        elif water < self.NORMAL_WATER_MIN:
            nutr_contrib += 5.0
            factors.append({
                "factor": "water_intake",
                "contribution": 5.0,
                "severity": "WARNING",
                "detail": f"Subnormal water consumption ({water:.1f} L < {self.NORMAL_WATER_MIN} L)"
            })
        raw_score += nutr_contrib

        # 6. Environmental Heat Stress Index (THI contribution)
        if amb_temp > 32.0 and humidity > 70.0:
            thi_contrib = 8.0
            factors.append({
                "factor": "heat_stress",
                "contribution": thi_contrib,
                "severity": "WARNING",
                "detail": f"Pasture heat-humidity stress (Ambient: {amb_temp:.1f}°C, Humidity: {humidity:.0f}%)"
            })
            raw_score += thi_contrib

        # Bound score between 5.0 and 99.0
        final_score = round(min(max(raw_score, 5.0), 99.0), 1)

        # Categorize
        if final_score >= 71.0:
            level = "CRITICAL"
        elif final_score >= 36.0:
            level = "AT_RISK"
        else:
            level = "HEALTHY"
            if not factors:
                factors.append({
                    "factor": "vitals_normal",
                    "contribution": 5.0,
                    "severity": "INFO",
                    "detail": "All physiological vital parameters within normal bovine reference ranges."
                })

        return {
            "risk_score": final_score,
            "risk_level": level,
            "factors": factors,
            "explanation": f"Health Risk: {level} ({final_score}/100). {len(factors)} contributing physiological signal(s)."
        }

risk_engine = HealthRiskEngine()
