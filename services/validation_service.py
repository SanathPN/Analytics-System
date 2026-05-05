import pandas as pd


def validate_csv(file_path):
    """
    Validates the uploaded CSV file.
    Checks:
    - Required columns exist
    - No missing values
    - Correct data types
    """

    # Load CSV file
    df = pd.read_csv(file_path)

    # Required columns for Phase 1
    required_columns = ["revenue", "frequency"]

    # Check if required columns exist
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: '{column}'")

    # Check for missing values
    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values in required columns")

    # Validate numeric types
    try:
        df["revenue"] = df["revenue"].astype(float)
        df["frequency"] = df["frequency"].astype(int)
    except ValueError:
        raise ValueError("Revenue must be numeric and Frequency must be integer")

    # Validate logical constraints
    if (df["revenue"] < 0).any():
        raise ValueError("Revenue cannot be negative")

    if (df["frequency"] < 0).any():
        raise ValueError("Frequency cannot be negative")

    return df