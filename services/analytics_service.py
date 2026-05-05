import pandas as pd


def calculate_kpis(df):
    """
    Calculates key performance indicators (KPIs).
    Phase 1 KPIs:
    - Total Revenue
    - Average Revenue
    - Total Customers
    - Average Frequency
    - Segment Distribution
    - Revenue by Segment
    """

    # Ensure dataframe is not empty
    if df.empty:
        return {
            "total_revenue": 0,
            "average_revenue": 0,
            "total_customers": 0,
            "average_frequency": 0,
            "segment_distribution": {},
            "revenue_by_segment": {}
        }

    # Basic KPIs
    total_revenue = float(df["revenue"].sum())
    average_revenue = float(df["revenue"].mean())
    total_customers = int(len(df))
    average_frequency = float(df["frequency"].mean())

    # Segment distribution count
    segment_distribution = df["segment"].value_counts().to_dict()

    # Revenue contribution by segment
    revenue_by_segment = (
        df.groupby("segment")["revenue"]
        .sum()
        .to_dict()
    )

    return {
        "total_revenue": total_revenue,
        "average_revenue": average_revenue,
        "total_customers": total_customers,
        "average_frequency": average_frequency,
        "segment_distribution": segment_distribution,
        "revenue_by_segment": revenue_by_segment
    }