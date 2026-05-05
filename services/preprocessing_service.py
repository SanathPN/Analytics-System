import pandas as pd


def preprocess_data(df):
    """
    Preprocesses validated dataset.
    Operations:
    - Ensure correct data types
    - Remove duplicates
    - Create derived metrics
    - Normalize basic values if needed
    """

    # Ensure numeric types (safety check)
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce")

    # Drop rows with conversion errors
    df = df.dropna(subset=["revenue", "frequency"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Derived metric: revenue per frequency
    df["revenue_per_transaction"] = df["revenue"] / df["frequency"]

    # Handle divide-by-zero cases
    df["revenue_per_transaction"] = df["revenue_per_transaction"].replace(
        [float("inf"), -float("inf")], 0
    )

    # Optional normalization (for future ML use)
    max_revenue = df["revenue"].max()
    if max_revenue != 0:
        df["normalized_revenue"] = df["revenue"] / max_revenue
    else:
        df["normalized_revenue"] = 0

    return df