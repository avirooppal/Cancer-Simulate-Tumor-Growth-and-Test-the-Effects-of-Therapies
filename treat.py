import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()

# df = pd.DataFrame(data=data.data, columns=data.feature_names)

# # Add the target column (0 = Benign, 1 = Malignant)
# df['target'] = data.target

# # Display the first few rows of the dataset
# print("First few rows of the dataset:")
# print(df.head())

# # Display information about the dataset
# print("\nDataset Info:")
# print(df.info())

# # Check for any missing values
# print("\nMissing values in the dataset:")
# print(df.isnull().sum())

# # Basic statistics about the dataset
# print("\nBasic Statistics of the dataset:")
# print(df.describe())

df = pd.DataFrame(data=data.data, columns=data.feature_names)
df['target'] = data.target  

X = df.drop(columns=['target'])  
y = df['target']  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

def recommend_treatment(prediction):
    if prediction == 0:
        return "Treatment Plan: Regular Monitoring"
    elif prediction == 1:
        return "Treatment Plan: Surgery, Chemotherapy, and/or Radiotherapy"

##Test the model with a new patient sample from test set
new_sample = X_test.iloc[0]  
new_sample = new_sample.values.reshape(1, -1)

#(0 for benign, 1 for malignant)
prediction = model.predict(new_sample)[0]

treatment_plan = recommend_treatment(prediction)

print(f"Prediction for the new sample (Benign or Malignant): {'Benign' if prediction == 0 else 'Malignant'}")
print(f"Personalized Treatment Plan: {treatment_plan}")
