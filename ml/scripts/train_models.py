"""
CATTLEX - Multi-Model Training & Evaluation Script
Reproducible training of 6 algorithms on the actual 2,044 cattle symptom records,
along with the Vital Signs Health Risk engine.
"""

import os
import sys
import time
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from sklearn.pipeline import Pipeline
import joblib

# Add backend directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.ml.preprocessing import SYMPTOM_FEATURES, SYMPTOM_DISPLAY_NAMES, DISEASE_CLASSES, load_raw_dataset

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

def train_and_evaluate_disease_models():
    print("=" * 70)
    print("CATTLEX: Commencing Reproducible ML Training & Benchmark Pipeline")
    print("=" * 70)

    raw_data_path = os.path.join(PROJECT_ROOT, 'ml', 'data', 'raw', 'Training.csv')
    models_dir = os.path.join(PROJECT_ROOT, 'ml', 'models')
    reports_dir = os.path.join(PROJECT_ROOT, 'ml', 'reports')
    backend_models_dir = os.path.join(PROJECT_ROOT, 'backend', 'app', 'ml', 'saved_models')

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(backend_models_dir, exist_ok=True)

    print(f"Loading raw dataset from: {raw_data_path}")
    X_df, y_series = load_raw_dataset(raw_data_path)
    print(f"Dataset shape: {X_df.shape}, Classes: {y_series.nunique()}")

    # Encode disease targets
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_series)
    class_names = list(label_encoder.classes_)

    # Save LabelEncoder and preprocessor
    joblib.dump(label_encoder, os.path.join(models_dir, 'label_encoder.joblib'))
    joblib.dump(label_encoder, os.path.join(backend_models_dir, 'label_encoder.joblib'))

    # Stratified 80/20 train/test split to guarantee class distribution balance
    X_train, X_test, y_train, y_test = train_test_split(
        X_df.values, y_encoded, test_size=0.20, random_state=RANDOM_STATE, stratify=y_encoded
    )
    print(f"Train samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

    # Model definitions
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=120, max_depth=16, min_samples_split=2, min_samples_leaf=1,
            random_state=RANDOM_STATE, n_jobs=-1
        ),
        'Gaussian Naive Bayes': GaussianNB(),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=18, min_samples_split=2, min_samples_leaf=1, random_state=RANDOM_STATE
        ),
        'Logistic Regression': LogisticRegression(
            max_iter=1000, C=1.0, random_state=RANDOM_STATE
        ),
        'k-NN': KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2),
        'Support Vector Machine': SVC(
            kernel='linear', C=1.0, probability=True, random_state=RANDOM_STATE
        )
    }

    # Hyperparameter tuning for Random Forest to find optimal parameters
    print("\nTuning Random Forest Hyperparameters via GridSearchCV...")
    rf_param_grid = {
        'n_estimators': [80, 120, 160],
        'max_depth': [12, 16, 20],
        'min_samples_split': [2, 4]
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
        rf_param_grid, cv=cv, scoring='f1_weighted', n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    best_rf = grid_search.best_estimator_
    print(f"Best RF Parameters: {grid_search.best_params_}")
    models['Random Forest'] = best_rf

    results = []
    trained_estimators = {}

    print("\nTraining and Benchmarking Algorithms:")
    for name, clf in models.items():
        # Training time
        t0 = time.perf_counter()
        clf.fit(X_train, y_train)
        train_time = time.perf_counter() - t0

        # Inference latency on test set
        t0 = time.perf_counter()
        y_pred = clf.predict(X_test)
        inference_time = (time.perf_counter() - t0) / len(X_test) * 1000  # ms per sample

        # Cross-validation
        cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring='accuracy', n_jobs=-1)

        acc = accuracy_score(y_test, y_pred)
        prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
        prec_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
        rec_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1_m = f1_score(y_test, y_pred, average='macro', zero_division=0)
        f1_w = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        results.append({
            'Model': name,
            'Accuracy': round(float(acc) * 100, 2),
            'Precision (Weighted)': round(float(prec_weighted) * 100, 2),
            'Recall (Weighted)': round(float(rec_weighted) * 100, 2),
            'F1-Score (Weighted)': round(float(f1_w) * 100, 2),
            'Precision (Macro)': round(float(prec_macro) * 100, 2),
            'Recall (Macro)': round(float(rec_macro) * 100, 2),
            'F1-Score (Macro)': round(float(f1_m) * 100, 2),
            'CV Score Mean': round(float(cv_scores.mean()) * 100, 2),
            'CV Score Std': round(float(cv_scores.std()) * 100, 2),
            'Training Time (s)': round(float(train_time), 4),
            'Inference Latency (ms/sample)': round(float(inference_time), 4)
        })

        trained_estimators[name] = clf
        print(f" -> {name:22} | Acc: {acc*100:6.2f}% | F1-Weighted: {f1_w*100:6.2f}% | CV: {cv_scores.mean()*100:6.2f}% (±{cv_scores.std()*100:.2f}%) | Latency: {inference_time:.3f}ms")

    # Serialize trained models
    model_filename_map = {
        'Random Forest': 'random_forest_disease.joblib',
        'Gaussian Naive Bayes': 'gaussian_nb_disease.joblib',
        'Decision Tree': 'decision_tree_disease.joblib',
        'Logistic Regression': 'logistic_regression_disease.joblib',
        'k-NN': 'knn_disease.joblib',
        'Support Vector Machine': 'svm_disease.joblib'
    }

    for name, filename in model_filename_map.items():
        joblib.dump(trained_estimators[name], os.path.join(models_dir, filename))
        joblib.dump(trained_estimators[name], os.path.join(backend_models_dir, filename))

    # Save comparison CSV
    df_results = pd.DataFrame(results)
    csv_report_path = os.path.join(reports_dir, 'model_comparison.csv')
    df_results.to_csv(csv_report_path, index=False)
    print(f"\nSaved model comparison CSV to {csv_report_path}")

    # Primary model evaluation details (Random Forest)
    primary_clf = trained_estimators['Random Forest']
    y_pred_rf = primary_clf.predict(X_test)
    class_report_str = classification_report(y_test, y_pred_rf, target_names=class_names, zero_division=0)
    with open(os.path.join(reports_dir, 'classification_report.txt'), 'w', encoding='utf-8') as f:
        f.write("CATTLEX Random Forest Classification Report:\n\n")
        f.write(class_report_str)

    # 1. Confusion Matrix Plot
    plt.figure(figsize=(16, 14))
    cm = confusion_matrix(y_test, y_pred_rf)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=[c.replace('_', ' ') for c in class_names],
                yticklabels=[c.replace('_', ' ') for c in class_names])
    plt.title('CATTLEX Random Forest Confusion Matrix (Actual Test Set)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Predicted Disease Class', fontsize=12)
    plt.ylabel('True Disease Class', fontsize=12)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'confusion_matrix.png'), dpi=200)
    plt.close()

    # 2. Feature Importance Plot (Top 25 Symptoms)
    importances = primary_clf.feature_importances_
    indices = np.argsort(importances)[::-1][:25]
    top_features = [SYMPTOM_DISPLAY_NAMES.get(SYMPTOM_FEATURES[i], SYMPTOM_FEATURES[i]) for i in indices]
    top_scores = importances[indices]

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_scores, y=top_features, palette='viridis')
    plt.title('Top 25 Important Predictive Features (Random Forest)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Relative Feature Importance Score', fontsize=12)
    plt.ylabel('Symptom Signal', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'feature_importance.png'), dpi=200)
    plt.close()

    # 3. Model Comparison Bar Chart
    plt.figure(figsize=(12, 6))
    x_pos = np.arange(len(df_results))
    width = 0.22
    plt.bar(x_pos - width, df_results['Accuracy'], width, label='Accuracy', color='#3b82f6')
    plt.bar(x_pos, df_results['F1-Score (Weighted)'], width, label='F1 (Weighted)', color='#10b981')
    plt.bar(x_pos + width, df_results['CV Score Mean'], width, label='5-Fold CV Mean', color='#8b5cf6')
    plt.xticks(x_pos, df_results['Model'], rotation=15, ha='right', fontsize=10)
    plt.ylabel('Percentage (%)', fontsize=11)
    plt.title('CATTLEX Multi-Model Performance Benchmark', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(60, 105)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(reports_dir, 'model_comparison.png'), dpi=200)
    plt.close()

    # 4. Save structured JSON for API and UI consumption
    feature_importance_dict = {
        SYMPTOM_FEATURES[i]: float(importances[i]) for i in np.argsort(importances)[::-1]
    }
    metrics_payload = {
        "metadata": {
            "dataset": "Cattle Disease Dataset (Reference: thyagarajank/Cattle-disease-prediction-using-Machine-Learning)",
            "total_samples": len(X_df),
            "total_features": len(SYMPTOM_FEATURES),
            "disease_classes_count": len(class_names),
            "disease_classes": class_names,
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "evaluation_strategy": "Stratified 80/20 Split + 5-Fold Stratified Cross Validation",
            "paper_reported_rf": {
                "accuracy": 92.31,
                "precision": 89.74,
                "recall": 92.31,
                "f1_score": 90.38,
                "note": "Reported metrics in the research paper publication reference"
            }
        },
        "models": results,
        "feature_importance_top25": [
            {"symptom": SYMPTOM_FEATURES[i], "display_name": SYMPTOM_DISPLAY_NAMES.get(SYMPTOM_FEATURES[i], SYMPTOM_FEATURES[i]), "importance": round(float(importances[i]), 5)}
            for i in indices
        ]
    }

    with open(os.path.join(reports_dir, 'model_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2)
    with open(os.path.join(backend_models_dir, 'model_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2)

    # 5. Model Registry JSON
    model_registry = {
        "registry_version": "1.0.0",
        "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "primary_model": "Random Forest",
        "models": {
            name: {
                "algorithm": name,
                "version": "1.0.0",
                "file_path": f"app/ml/saved_models/{model_filename_map[name]}",
                "accuracy": res['Accuracy'],
                "f1_weighted": res['F1-Score (Weighted)'],
                "training_time_seconds": res['Training Time (s)'],
                "status": "active"
            }
            for name, res in zip(df_results['Model'], results)
        }
    }
    with open(os.path.join(reports_dir, 'model_registry.json'), 'w', encoding='utf-8') as f:
        json.dump(model_registry, f, indent=2)
    with open(os.path.join(backend_models_dir, 'model_registry.json'), 'w', encoding='utf-8') as f:
        json.dump(model_registry, f, indent=2)

    print("\nDisease models successfully trained and serialized.")
    return metrics_payload


def train_vital_signs_health_risk_model():
    """
    Trains a vital signs physiological risk classifier and scoring model.
    Inputs:
      - temperature (°C): Normal 38.0 - 39.3, Fever > 39.8, Hypothermia < 37.5
      - heart_rate (bpm): Normal 48 - 84, Tachycardia > 95, Bradycardia < 42
      - respiratory_rate (bpm): Normal 24 - 36, Dyspnea/Tachypnea > 45, Bradypnea < 18
      - activity_level (0-1): Normal 0.70 - 0.95, Lethargy < 0.40
      - feed_intake (kg): Normal 15.0 - 24.0, Anorexia < 8.0
      - water_intake (L): Normal 45.0 - 85.0, Dehydration/Low < 25.0
      - ambient_temperature (°C): Ambient climate
      - humidity (%): Ambient relative humidity
    """
    print("\n" + "=" * 70)
    print("CATTLEX: Training Vital Signs Health Risk Engine")
    print("=" * 70)

    models_dir = os.path.join(PROJECT_ROOT, 'ml', 'models')
    backend_models_dir = os.path.join(PROJECT_ROOT, 'backend', 'app', 'ml', 'saved_models')

    # Generate calibrated synthetic training set adhering to veterinary physiology
    np.random.seed(RANDOM_STATE)
    n_samples = 4000

    records = []
    labels = []
    risk_scores = []

    for _ in range(n_samples):
        # 60% healthy, 25% at_risk, 15% critical
        state = np.random.choice(['HEALTHY', 'AT_RISK', 'CRITICAL'], p=[0.60, 0.25, 0.15])

        amb_temp = np.random.uniform(18.0, 34.0)
        humidity = np.random.uniform(40.0, 85.0)

        if state == 'HEALTHY':
            temp = np.random.normal(38.6, 0.3)
            hr = np.random.normal(66, 6)
            rr = np.random.normal(28, 3)
            act = np.random.uniform(0.70, 0.95)
            feed = np.random.normal(19.0, 2.0)
            water = np.random.normal(65.0, 8.0)
            risk = np.random.uniform(5.0, 32.0)
        elif state == 'AT_RISK':
            temp = np.random.choice([np.random.normal(39.6, 0.3), np.random.normal(37.7, 0.2)])
            hr = np.random.choice([np.random.normal(88, 6), np.random.normal(46, 3)])
            rr = np.random.choice([np.random.normal(40, 4), np.random.normal(20, 2)])
            act = np.random.uniform(0.35, 0.65)
            feed = np.random.normal(12.0, 2.5)
            water = np.random.normal(38.0, 6.0)
            risk = np.random.uniform(38.0, 68.0)
        else:  # CRITICAL
            temp = np.random.choice([np.random.normal(40.6, 0.5), np.random.normal(36.8, 0.4)])
            hr = np.random.choice([np.random.normal(105, 8), np.random.normal(38, 4)])
            rr = np.random.choice([np.random.normal(52, 6), np.random.normal(14, 2)])
            act = np.random.uniform(0.10, 0.32)
            feed = np.random.normal(5.0, 2.0)
            water = np.random.normal(18.0, 5.0)
            risk = np.random.uniform(72.0, 98.0)

        records.append([temp, hr, rr, act, feed, water, amb_temp, humidity])
        labels.append(state)
        risk_scores.append(risk)

    vital_cols = [
        'temperature', 'heart_rate', 'respiratory_rate', 'activity_level',
        'feed_intake', 'water_intake', 'ambient_temperature', 'humidity'
    ]
    X_vital = pd.DataFrame(records, columns=vital_cols)
    y_vital = np.array(labels)
    y_scores = np.array(risk_scores)

    # Train vital classifier pipeline
    vital_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_STATE))
    ])
    vital_pipeline.fit(X_vital, y_vital)

    # Save vital risk model
    joblib.dump(vital_pipeline, os.path.join(models_dir, 'vital_health_risk_model.joblib'))
    joblib.dump(vital_pipeline, os.path.join(backend_models_dir, 'vital_health_risk_model.joblib'))
    print("Vital signs health risk engine trained and serialized.")


if __name__ == '__main__':
    train_and_evaluate_disease_models()
    train_vital_signs_health_risk_model()
    print("\nAll CATTLEX ML pipelines executed successfully!")
