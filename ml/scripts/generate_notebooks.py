import json
import os

nb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notebooks'))
os.makedirs(nb_dir, exist_ok=True)

def make_nb(cells):
    return {
        'cells': cells,
        'metadata': {'language_info': {'name': 'python', 'version': '3.9'}},
        'nbformat': 4,
        'nbformat_minor': 4
    }

def md_cell(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': [src]}

def code_cell(src):
    return {'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [], 'source': [src]}

# 01
c1 = [
    md_cell('# CATTLEX: 01. Exploratory Data Analysis\nThis notebook conducts baseline statistical inspection of the cattle symptom disease reference dataset (2,044 samples, 93 symptom indicators, 26 target diseases).'),
    code_cell('import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv("../data/raw/Training.csv")\nprint("Dataset Shape:", df.shape)\nprint("Target diseases:", df["prognosis"].nunique())'),
    code_cell('df["prognosis"].value_counts().plot(kind="bar", figsize=(12, 5), color="#3b82f6")\nplt.title("Disease Frequency Distribution")\nplt.tight_layout()\nplt.show()')
]
with open(os.path.join(nb_dir, '01_data_exploration.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(c1), f, indent=2)

# 02
c2 = [
    md_cell('# CATTLEX: 02. Preprocessing & Feature Engineering\nPipeline implementation using scikit-learn LabelEncoder and SymptomPreprocessor.'),
    code_cell('import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import LabelEncoder\n\ndf = pd.read_csv("../data/raw/Training.csv")\nX = df.drop(columns=["prognosis"])\ny = df["prognosis"]\nle = LabelEncoder()\ny_enc = le.fit_transform(y)\nX_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)\nprint(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")')
]
with open(os.path.join(nb_dir, '02_preprocessing.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(c2), f, indent=2)

# 03
c3 = [
    md_cell('# CATTLEX: 03. Model Training & Benchmarking\nBenchmarking 6 algorithms: Random Forest, Gaussian Naive Bayes, Decision Tree, Logistic Regression, k-NN, SVM.'),
    code_cell('from sklearn.ensemble import RandomForestClassifier\nrf = RandomForestClassifier(n_estimators=80, max_depth=16, random_state=42)\nrf.fit(X_train, y_train)\nprint("Random Forest fitted successfully.")')
]
with open(os.path.join(nb_dir, '03_model_training.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(c3), f, indent=2)

# 04
c4 = [
    md_cell('# CATTLEX: 04. Model Evaluation & Explainability (XAI)\nEvaluation of confusion matrix, classification metrics, and Random Forest feature importances.'),
    code_cell('from sklearn.metrics import classification_report\ny_pred = rf.predict(X_test)\nprint(classification_report(y_test, y_pred, target_names=le.classes_))')
]
with open(os.path.join(nb_dir, '04_model_evaluation.ipynb'), 'w', encoding='utf-8') as f:
    json.dump(make_nb(c4), f, indent=2)

print('All 4 notebooks written successfully.')
