import pandas as pd


def validate_dataset(df):
    """
    Validates uploaded dataset before processing.

    Checks:
    - Required columns exist
    - No empty dataset
    - Numeric type enforcement
    - Non-negative enforcement
    - Zero frequency protection
    """

    # -------------------------------
    # Standardize Column Names
    # -------------------------------
    df.columns = df.columns.str.lower().str.strip()

    required_columns = ["revenue", "frequency"]

    # -------------------------------
    # Check Required Columns
    # -------------------------------
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # -------------------------------
    # Check Empty Dataset
    # -------------------------------
    if df.empty:
        raise ValueError("Uploaded dataset is empty")

    # -------------------------------
    # Convert to Numeric (Strict)
    # -------------------------------
    try:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="raise")
        df["frequency"] = pd.to_numeric(df["frequency"], errors="raise")
    except Exception:
        raise ValueError("Revenue and Frequency must contain only numeric values")

    # -------------------------------
    # Check Missing Values
    # -------------------------------
    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values in required columns")

    # -------------------------------
    # Check for Negative Values
    # -------------------------------
    if (df["revenue"] < 0).any():
        raise ValueError("Revenue must be non-negative")

    if (df["frequency"] < 0).any():
        raise ValueError("Frequency must be non-negative")

    # -------------------------------
    # Prevent Zero Frequency (division safety)
    # -------------------------------
    if (df["frequency"] == 0).any():
        raise ValueError("Frequency must be greater than zero")

    return True