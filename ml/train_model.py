import os
import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from preprocess import preprocess_data, fit_transform_encoders, transform_encoders
from evaluate import evaluate_model

"""
Machine Learning Model Training Pipeline for Network Threat Detection
"""

def main():

    # -------------------------------------------------------------
    # 1. Load Dataset
    # -------------------------------------------------------------
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(project_root, "ml", "dataset.csv")

    print(f"Loading Dataset from: {dataset_path}")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path)

    print(df.head())
    print(df.columns)
    print(df["Attack_Type"].value_counts())

    # -------------------------------------------------------------
    # 2. Convert Timestamp to Numeric Features
    # -------------------------------------------------------------
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Hour"] = df["Timestamp"].dt.hour
    df["Day"] = df["Timestamp"].dt.day
    df["Month"] = df["Timestamp"].dt.month

    # Remove original timestamp
    df.drop(columns=["Timestamp"], inplace=True)

    # -------------------------------------------------------------
    # 3. Remove IP Address Columns
    # -------------------------------------------------------------
    df.drop(columns=["Source_IP", "Destination_IP"], inplace=True)

    # -------------------------------------------------------------
    # 4. Feature / Target Separation
    # -------------------------------------------------------------
    X, y = preprocess_data(df, target_col="Attack_Type")

    print("\nExtracted Features:")
    print(X.columns.tolist())

    # -------------------------------------------------------------
    # 5. Train/Test Split
    # -------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(f"\nTrain Samples : {len(X_train)}")
    print(f"Test Samples  : {len(X_test)}")

    # -------------------------------------------------------------
    # 6. Encode Categorical Features
    # -------------------------------------------------------------
    categorical_cols = [
        "Protocol",
        "Country",
        "Threat_Level"
    ]

    X_train_encoded, encoders = fit_transform_encoders(
        X_train,
        categorical_cols
    )

    X_test_encoded = transform_encoders(
        X_test,
        encoders
    )

    print("\nFeature Data Types")
    print(X_train_encoded.dtypes)

    # -------------------------------------------------------------
    # 7. Encode Labels
    # -------------------------------------------------------------
    label_encoder = LabelEncoder()

    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)

    print("\nAttack Classes:")
    print(label_encoder.classes_)

    # -------------------------------------------------------------
    # 8. Build Model
    # -------------------------------------------------------------
    model = XGBClassifier(
        objective="multi:softprob",
        num_class=len(label_encoder.classes_),
        n_estimators=300,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="mlogloss"
    )

    # -------------------------------------------------------------
    # 9. Train
    # -------------------------------------------------------------
    print("Training Model...")

    print("\nColumn Types:")
    print(X_train_encoded.dtypes)

    print("\nRemaining Object Columns:")
    print(X_train_encoded.select_dtypes(include="object").columns.tolist())

    model.fit(X_train_encoded, y_train)

    print("Model Training Completed Successfully!")

    # -------------------------------------------------------------
    # 10. Evaluate
    # -------------------------------------------------------------
    print("\nEvaluating Model...")

    evaluate_model(
        model,
        X_test_encoded,
        y_test
    )

    # -------------------------------------------------------------
    # 11. Save Model
    # -------------------------------------------------------------
    ml_dir = os.path.join(project_root, "ml")

    os.makedirs(ml_dir, exist_ok=True)

    joblib.dump(model, os.path.join(ml_dir, "threat_model.pkl"))
    joblib.dump(encoders, os.path.join(ml_dir, "encoders.pkl"))
    joblib.dump(label_encoder, os.path.join(ml_dir, "label_encoder.pkl"))

    print("\nModel Saved Successfully.")

    print("\nTraining Pipeline Finished Successfully.")

if __name__ == "__main__":
    main()