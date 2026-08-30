import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ============================================================
# FEATURES USED BY THE AI MODEL
# ============================================================

FEATURES = [
    "temperature",
    "aqi",
    "vibration"
]


# ============================================================
# LOAD SENSOR DATASET
# ============================================================

df = pd.read_csv("data/sensor_data.csv")


# ============================================================
# SELECT SENSOR FEATURES
# ============================================================

X = df[FEATURES]


# ============================================================
# SELECT TARGET LABEL
# 0 = NORMAL
# 1 = ANOMALOUS
# ============================================================

y = df["label"]


# ============================================================
# SPLIT DATA INTO TRAINING AND TESTING DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================================================
# CREATE RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# ============================================================
# TRAIN MODEL
# ============================================================

model.fit(
    X_train,
    y_train
)


# ============================================================
# TEST MODEL
# ============================================================

predictions = model.predict(
    X_test
)


# ============================================================
# CALCULATE ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "Model accuracy:",
    accuracy
)


# ============================================================
# SAVE TRAINED MODEL
# ============================================================

joblib.dump(
    model,
    "model/anomaly_model.pkl"
)


print(
    "Model saved successfully."
)