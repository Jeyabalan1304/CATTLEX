# Cattlex - AI Powered Livestock Health Monitoring

Cattlex is an AI-driven solution to monitor livestock health in real time. This system uses machine learning models such as Decision Tree, Random Forest, Naive Bayes, and K-Nearest Neighbors to predict and analyze livestock health status based on collected data.
## Features
- Train various machine learning models on livestock health data.
- Test model performance on new data.
- Predict livestock health status based on symptoms.

## Dataset
The system uses a dataset (`training.csv` and `Testing.csv`) with features such as:
- Temperature
- Respiratory rate
- Heart rate
- Feed intake
- Water intake
- Target variable: Disease prognosis

## Requirements
Install the required Python libraries before running the scripts:
```bash
pip install pandas numpy scikit-learn joblib
