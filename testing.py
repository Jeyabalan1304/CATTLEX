import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Load the training data (to get the correct column names)
df_train = pd.read_csv("training.csv")
X_train = df_train.iloc[:, :-1]  # All columns except the last one

# Load the testing data
df_test = pd.read_csv("Testing.csv")

# Prepare the features (X_test) and target variable (y_test)
X_test = df_test.iloc[:, :-1]  # All columns except the last one
y_test = df_test.iloc[:, -1]   # Last column (prognosis)

# Encode the target variable
le = LabelEncoder()
y_test = le.fit_transform(y_test)

# Ensure X_test has the same columns as X_train
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# Train the models (if not already trained)
dt_clf = DecisionTreeClassifier(random_state=42)
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
nb_clf = GaussianNB()
knn_clf = KNeighborsClassifier(n_neighbors=5)

models = [
    ("Decision Tree", dt_clf),
    ("Random Forest", rf_clf),
    ("Naive Bayes", nb_clf),
    ("K-Nearest Neighbors", knn_clf)
]

# Train each model if not already trained
for name, model in models:
    if not hasattr(model, 'classes_'):
        model.fit(X_train, le.fit_transform(df_train.iloc[:, -1]))

# Test and evaluate each model
for name, model in models:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy on Testing Data: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))
    print("/n")

# Function to make predictions
def predict_disease(symptoms, models, le):
    input_data = [1 if symptom in symptoms else 0 for symptom in X_train.columns]
    input_array = np.array(input_data).reshape(1, -1)
    
    predictions = {}
    for name, model in models:
        prediction = le.inverse_transform(model.predict(input_array))[0]
        predictions[name] = prediction
    
    return predictions

# Example usage with a sample from the testing data
sample_symptoms = X_test.iloc[0]
sample_symptoms = sample_symptoms[sample_symptoms == 1].index.tolist()
predictions = predict_disease(sample_symptoms, models, le)
print("Sample Symptoms:", sample_symptoms)
print("Predictions:", predictions)
print("Actual Disease:", le.inverse_transform([y_test[0]])[0])
print(accuracy_score(y_test,y_pred))