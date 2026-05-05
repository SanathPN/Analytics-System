import pandas as pd


def preprocess_dataset(df):
    """
    Performs preprocessing before segmentation.

    Steps:
    - Standardize column names
    - Remove duplicates
    - Convert to numeric safely
    - Remove invalid rows
    - Enforce non-negative values
    - Handle zero frequency safely
    - Create derived features
    """

    # -------------------------------
    # Standardize Column Names
    # -------------------------------
    df.columns = df.columns.str.lower().str.strip()

    # -------------------------------
    # Remove Duplicates
    # -------------------------------
    df = df.drop_duplicates()

    # -------------------------------
    # Convert to Numeric (Safe)
    # -------------------------------
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")

    # -------------------------------
    # Remove Rows with Invalid Data
    # -------------------------------
    df = df.dropna(subset=["revenue", "frequency"])

    # -------------------------------
    # Enforce Non-Negative Values
    # -------------------------------
    df = df[(df["revenue"] >= 0) & (df["frequency"] >= 0)]

    # -------------------------------
    # Avoid Division by Zero
    # -------------------------------
    df = df[df["frequency"] != 0]

    # -------------------------------
    # Derived Feature
    # -------------------------------
    df["revenue_per_transaction"] = df["revenue"] / df["frequency"]

    # -------------------------------
    # Reset Index
    # -------------------------------
    df = df.reset_index(drop=True)

    return df