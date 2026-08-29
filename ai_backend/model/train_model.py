import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


FEATURES = [
    "temperature",
    "humidity",
    "voltage",
    "current",
    "vibration"
]


# Load the sensor dataset
df = pd.read_csv("data/sensor_data.csv")


# Select the sensor values used by the AI
X = df[FEATURES]

# Select the correct answers
y = df["label"]


# Split the dataset into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create the Random Forest machine-learning model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train the model
model.fit(X_train, y_train)


# Test the trained model
predictions = model.predict(X_test)


# Calculate accuracy
accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model accuracy:", accuracy)


# Save the trained model
joblib.dump(
    model,
    "model/anomaly_model.pkl"
)

print("Model saved successfully.")