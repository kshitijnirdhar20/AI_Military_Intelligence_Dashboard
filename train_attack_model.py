import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

os.makedirs("models", exist_ok=True)

print("=" * 60)
print("AI Military Intelligence - Attack Prediction Model")
print("=" * 60)

print("\nLoading Global Terrorism Dataset...")

df = pd.read_csv(
    "data/globalterrorism.csv",
    encoding="latin1",
    low_memory=False
)

print("\nDataset Loaded Successfully")

print(f"Rows : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

features = [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname",
    "success",
    "suicide",
    "nkill",
    "nwound"
]

target = "attacktype1_txt"

df = df[features + [target]]

df = df.dropna()

print("\nAfter Data Cleaning")

print(f"Rows : {df.shape[0]:,}")

print(f"Attack Types : {df[target].nunique()}")

print(f"Countries : {df['country_txt'].nunique()}")

encoders = {}

categorical_columns = [
    "country_txt",
    "region_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "gname"
]

for col in categorical_columns:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder

target_encoder = LabelEncoder()

df[target] = target_encoder.fit_transform(df[target])

X = df[features]

y = df[target]

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Samples :", X_train.shape[0])

print("Testing Samples :", X_test.shape[0])

print("\nTraining Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)

print("Model Training Completed")

pred = model.predict(X_test)

train_accuracy = model.score(
    X_train,
    y_train
)

test_accuracy = accuracy_score(
    y_test,
    pred
)

print("\n" + "=" * 60)

print("MODEL PERFORMANCE")

print("=" * 60)

print(f"Training Accuracy : {train_accuracy:.4f}")

print(f"Testing Accuracy  : {test_accuracy:.4f}")

print("\nClassification Report")

print(classification_report(
    y_test,
    pred
))

print("Confusion Matrix")

print(confusion_matrix(
    y_test,
    pred
))

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")

print(importance)

joblib.dump(
    model,
    "models/attack_prediction_model.pkl"
)

joblib.dump(
    target_encoder,
    "models/target_encoder.pkl"
)

joblib.dump(
    encoders,
    "models/feature_encoders.pkl"
)

importance.to_csv(
    "models/feature_importance.csv",
    index=False
)

print("\nSaving Files...")

print("✔ attack_prediction_model.pkl")

print("✔ feature_encoders.pkl")

print("✔ target_encoder.pkl")

print("✔ feature_importance.csv")

print("\n" + "=" * 60)

print("AI Attack Prediction Model Generated Successfully")

print("=" * 60)