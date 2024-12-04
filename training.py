import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the data
df = pd.read_csv("training.csv")

# Prepare the features (X) and target variable (y)
X = df.iloc[:, :-1]  # All columns except the last one
y = df.iloc[:, -1]   # Last column (prognosis)

# Encode the target variable
le = LabelEncoder()
y = le.fit_transform(y)
# Split the data


# List to store models
models = [
    ("Decision Tree", DecisionTreeClassifier(random_state=42)),
    ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42)),
    ("Naive Bayes", GaussianNB()),
    ("K-Nearest Neighbors", KNeighborsClassifier(n_neighbors=5))
]

# Train and evaluate each model
for name, model in models:
    model.fit(X, y)
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    print(f"{name} Accuracy: {accuracy:.4f}")
    print(classification_report(y, y_pred))
    print("\n")

# Function to make predictions
def predict_disease(symptoms, models, le):
    input_data = [1 if symptom in symptoms else 0 for symptom in X.columns]
    input_array = np.array(input_data).reshape(1, -1)
    
    predictions = {}
    for name, model in models:
        prediction = le.inverse_transform(model.predict(input_array))[0]
        predictions[name] = prediction
    
    return predictions

# Example usage
symptoms = ["anorexia", "abdominal_pain", "fever"]
predictions = predict_disease(symptoms, models, le)
print("Predictions:", predictions)
joblib.dump(df,"d")