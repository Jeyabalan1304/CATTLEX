import pytest
from app.ml.preprocessing import SymptomPreprocessor, SYMPTOM_FEATURES, DISEASE_CLASSES
from app.ml.predict import predict_disease, predict_health_risk
from app.ml.explain import explain_prediction

def test_symptom_preprocessor():
    preprocessor = SymptomPreprocessor()
    # Test dictionary input
    sample_dict = {"fever": True, "coughing": 1, "lameness": "true"}
    vec = preprocessor.transform(sample_dict)
    assert vec.shape == (1, len(SYMPTOM_FEATURES))
    assert vec[0, SYMPTOM_FEATURES.index("fever")] == 1
    assert vec[0, SYMPTOM_FEATURES.index("coughing")] == 1
    assert vec[0, SYMPTOM_FEATURES.index("lameness")] == 1

def test_disease_prediction_mastitis():
    symptoms = {
        "fever": True,
        "loss_of_appetite": True,
        "udder_swelling": True,
        "udder_heat": True,
        "udder_pain": True,
        "milk_flakes": True,
        "milk_clots": True
    }
    result = predict_disease(symptoms, model_name="Random Forest")
    assert "predicted_disease" in result
    assert result["predicted_disease"] == "mastitis"
    assert result["confidence"] > 0.0
    assert len(result["top_predictions"]) <= 3
    assert "recommendation" in result

def test_disease_prediction_alternative_models():
    symptoms = {"fever": True, "diarrhoea": True, "loss_of_appetite": True}
    for model_name in ["Random Forest", "Gaussian Naive Bayes", "Decision Tree"]:
        res = predict_disease(symptoms, model_name=model_name)
        assert res["predicted_disease"] in DISEASE_CLASSES

def test_health_risk_healthy():
    normal_vitals = {
        "temperature": 38.6,
        "heart_rate": 65.0,
        "respiratory_rate": 26.0,
        "activity_level": 0.85,
        "feed_intake": 19.0,
        "water_intake": 65.0
    }
    res = predict_health_risk(normal_vitals)
    assert res["health_status"] == "HEALTHY"
    assert res["risk_score"] < 35.0

def test_health_risk_critical_pyrexia():
    fever_vitals = {
        "temperature": 40.8,
        "heart_rate": 110.0,
        "respiratory_rate": 55.0,
        "activity_level": 0.15,
        "feed_intake": 4.0,
        "water_intake": 15.0
    }
    res = predict_health_risk(fever_vitals)
    assert res["health_status"] == "CRITICAL"
    assert res["risk_score"] >= 70.0
    assert "fever" in res["prediction_reason"].lower() or "pyrexia" in res["prediction_reason"].lower()

def test_explainable_ai_feature_importance():
    symptoms = {"fever": True, "udder_swelling": True, "reduced_milk_yield": True}
    explanations = explain_prediction(symptoms)
    assert isinstance(explanations, list)
    for item in explanations:
        assert "feature" in item
        assert "importance_score" in item
