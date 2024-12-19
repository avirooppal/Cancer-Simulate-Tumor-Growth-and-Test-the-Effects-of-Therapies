import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv('data.csv')

# Display column names to verify
print(data.columns)

# Set the target column and the feature columns
X = data.drop(columns=['diagnosis', 'Unnamed: 32', 'id'])  # Drop 'diagnosis', 'Unnamed: 32' and 'id' as they are not features
y = data['diagnosis']  # 'diagnosis' is the target variable

# Encode target variable (convert 'M' and 'B' to numeric)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)  # 'M' -> 1, 'B' -> 0

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Predict for a new sample (example)
new_sample = X_test.iloc[0]  # Take the first sample from the test set
new_sample = new_sample.values.reshape(1, -1)  # Reshape to match model input
prediction = model.predict(new_sample)
prediction = label_encoder.inverse_transform(prediction)  # Convert numeric back to 'M' or 'B'
print(f'Prediction for the new sample: {prediction[0]}')
