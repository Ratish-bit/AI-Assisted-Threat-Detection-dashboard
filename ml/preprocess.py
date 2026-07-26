import pandas as pd
from sklearn.preprocessing import LabelEncoder

"""
Preprocessing module for AI Threat Detection.
"""

def clean_data(df):
    """
    Cleans dataset and prepares it for machine learning.
    """

    df = df.copy()

    # Remove duplicates and null values
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # -----------------------------
    # Timestamp Feature Engineering
    # -----------------------------
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

        df["Hour"] = df["Timestamp"].dt.hour
        df["Day"] = df["Timestamp"].dt.day
        df["Month"] = df["Timestamp"].dt.month

        df.drop(columns=["Timestamp"], inplace=True)

    # -----------------------------
    # Remove Identifier Columns
    # -----------------------------
    drop_cols = [
        "Source_IP",
        "Destination_IP",
        "md5",
        "sha256",
        "filename",
        "filepath",
        "id"
    ]

    for col in drop_cols:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    return df


def preprocess_data(df, target_col="Attack_Type"):

    df = clean_data(df)

    if target_col in df.columns:
        X = df.drop(columns=[target_col])
        y = df[target_col]
    else:
        X = df
        y = None

    return X, y


def fit_transform_encoders(X_train, categorical_cols=None):

    if categorical_cols is None:
        categorical_cols = []

    X_train = X_train.copy()

    encoders = {}

    for col in categorical_cols:

        if col in X_train.columns:

            encoder = LabelEncoder()

            X_train[col] = encoder.fit_transform(
                X_train[col].astype(str)
            )

            encoders[col] = encoder

    return X_train, encoders


def transform_encoders(X_test, encoders):

    X_test = X_test.copy()

    for col, encoder in encoders.items():

        if col in X_test.columns:

            known = set(encoder.classes_)

            X_test[col] = X_test[col].astype(str).apply(
                lambda x: encoder.transform([x])[0]
                if x in known else 0
            )

    return X_test