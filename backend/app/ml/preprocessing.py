"""
CATTLEX - Preprocessing & Feature Engineering Pipeline
Handles data cleaning, symptom feature validation, label encoding, and dataset transformations.
"""

from typing import List, Dict, Tuple, Any
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
import joblib

# Full list of 93 symptoms from the GitHub reference dataset (in original order)
SYMPTOM_FEATURES: List[str] = [
    'anorexia', 'abdominal_pain', 'anaemia', 'abortions', 'acetone', 'aggression', 'arthrogyposis',
    'ankylosis', 'anxiety', 'bellowing', 'blood_loss', 'blood_poisoning', 'blisters', 'colic',
    'Condemnation_of_livers', 'conjunctivae', 'coughing', 'depression', 'discomfort', 'dyspnea',
    'dysentery', 'diarrhoea', 'dehydration', 'drooling', 'dull', 'decreased_fertility', 'diffculty_breath',
    'emaciation', 'encephalitis', 'fever', 'facial_paralysis', 'frothing_of_mouth', 'frothing',
    'gaseous_stomach', 'highly_diarrhoea', 'high_pulse_rate', 'high_temp', 'high_proportion',
    'hyperaemia', 'hydrocephalus', 'isolation_from_herd', 'infertility', 'intermittent_fever',
    'jaundice', 'ketosis', 'loss_of_appetite', 'lameness', 'lack_of-coordination', 'lethargy',
    'lacrimation', 'milk_flakes', 'milk_watery', 'milk_clots', 'mild_diarrhoea', 'moaning',
    'mucosal_lesions', 'milk_fever', 'nausea', 'nasel_discharges', 'oedema', 'pain',
    'painful_tongue', 'pneumonia', 'photo_sensitization', 'quivering_lips', 'reduction_milk_vields',
    'rapid_breathing', 'rumenstasis', 'reduced_rumination', 'reduced_fertility', 'reduced_fat',
    'reduces_feed_intake', 'raised_breathing', 'stomach_pain', 'salivation', 'stillbirths',
    'shallow_breathing', 'swollen_pharyngeal', 'swelling', 'saliva', 'swollen_tongue',
    'tachycardia', 'torticollis', 'udder_swelling', 'udder_heat', 'udder_hardeness',
    'udder_redness', 'udder_pain', 'unwillingness_to_move', 'ulcers', 'vomiting',
    'weight_loss', 'weakness'
]

# Standardized human-readable symptom display names for the frontend & reports
SYMPTOM_DISPLAY_NAMES: Dict[str, str] = {
    feature: feature.replace('_', ' ').replace('-', ' ').title()
    for feature in SYMPTOM_FEATURES
}
SYMPTOM_DISPLAY_NAMES['Condemnation_of_livers'] = 'Liver Condemnation'
SYMPTOM_DISPLAY_NAMES['reduction_milk_vields'] = 'Reduction In Milk Yield'
SYMPTOM_DISPLAY_NAMES['nasel_discharges'] = 'Nasal Discharge'
SYMPTOM_DISPLAY_NAMES['udder_hardeness'] = 'Udder Hardness'
SYMPTOM_DISPLAY_NAMES['diffculty_breath'] = 'Difficulty Breathing'
SYMPTOM_DISPLAY_NAMES['reduces_feed_intake'] = 'Reduced Feed Intake'
SYMPTOM_DISPLAY_NAMES['lack_of-coordination'] = 'Lack Of Coordination'

# The 26 disease classes present in the actual reference dataset
DISEASE_CLASSES: List[str] = [
    'acetonaemia', 'blackleg', 'bloat', 'calf_diphtheria', 'calf_pneumonia',
    'coccidiosis', 'cryptosporidiosis', 'displaced_abomasum', 'fatty_liver_syndrome',
    'fog_fever', 'foot_and_mouth', 'foot_rot', 'gut_worms',
    'infectious_bovine_rhinotracheitis', 'listeriosis', 'liver_fluke', 'mastitis',
    'necrotic_enteritis', 'peri_weaning_diarrhoea', 'ragwort_poisoning',
    'rift_valley_fever', 'rumen_acidosis', 'schmallen_berg_virus',
    'traumatic_reticulitis', 'trypanosomosis', 'wooden_tongue'
]

DISEASE_DISPLAY_NAMES: Dict[str, str] = {
    d: d.replace('_', ' ').title() for d in DISEASE_CLASSES
}
DISEASE_DISPLAY_NAMES['schmallen_berg_virus'] = 'Schmallenberg Virus'
DISEASE_DISPLAY_NAMES['infectious_bovine_rhinotracheitis'] = 'Infectious Bovine Rhinotracheitis (IBR)'
DISEASE_DISPLAY_NAMES['foot_and_mouth'] = 'Foot-and-Mouth Disease (FMD)'
DISEASE_DISPLAY_NAMES['rift_valley_fever'] = 'Rift Valley Fever (RVF)'


class SymptomPreprocessor(BaseEstimator, TransformerMixin):
    """
    Transforms arbitrary symptom dictionary or DataFrame into aligned 93-feature binary matrix.
    """
    def __init__(self, feature_names: List[str] = None):
        self.feature_names = feature_names or SYMPTOM_FEATURES

    def fit(self, X, y=None):
        return self

    def transform(self, X: Any) -> np.ndarray:
        if isinstance(X, dict):
            vector = [1 if X.get(feat, False) in [True, 1, '1', 'true', 'True'] else 0 for feat in self.feature_names]
            return np.array([vector], dtype=np.int32)
        elif isinstance(X, list) and len(X) > 0 and isinstance(X[0], dict):
            matrix = []
            for row in X:
                vector = [1 if row.get(feat, False) in [True, 1, '1', 'true', 'True'] else 0 for feat in self.feature_names]
                matrix.append(vector)
            return np.array(matrix, dtype=np.int32)
        elif isinstance(X, pd.DataFrame):
            df = X.copy()
            for col in self.feature_names:
                if col not in df.columns:
                    df[col] = 0
            df = df[self.feature_names].fillna(0).astype(int)
            return df.values
        elif isinstance(X, np.ndarray):
            if X.shape[1] == len(self.feature_names):
                return X.astype(np.int32)
            raise ValueError(f"Input array has {X.shape[1]} columns; expected {len(self.feature_names)}")
        else:
            raise TypeError(f"Unsupported input type for SymptomPreprocessor: {type(X)}")


def load_raw_dataset(csv_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Loads raw CSV dataset, verifies schema, extracts X features and y labels.
    """
    df = pd.read_csv(csv_path)
    if 'prognosis' not in df.columns:
        raise ValueError("Missing 'prognosis' target column in dataset.")

    missing_features = [f for f in SYMPTOM_FEATURES if f not in df.columns]
    if missing_features:
        raise ValueError(f"Dataset missing required symptom features: {missing_features}")

    X = df[SYMPTOM_FEATURES].fillna(0).astype(int)
    y = df['prognosis'].astype(str).str.strip()
    return X, y
