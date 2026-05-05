import pandas as pd
import os
from datetime import datetime


def export_csv(df, output_folder="reports"):
    """
    Exports the processed DataFrame to a CSV file.
    Returns the file path.
    """

    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analytics_report_{timestamp}.csv"
    file_path = os.path.join(output_folder, filename)

    df.to_csv(file_path, index=False)

    return file_path


def generate_summary_report(kpis, output_folder="reports"):
    """
    Generates a simple text-based summary report
    containing calculated KPI metrics.
    Returns the file path.
    """

    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kpi_summary_{timestamp}.txt"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, "w") as f:
        f.write("=== KPI SUMMARY REPORT ===\n\n")
        f.write(f"Total Revenue: {kpis.get('total_revenue', 0)}\n")
        f.write(f"Average Revenue: {kpis.get('average_revenue', 0)}\n")
        f.write(f"Total Customers: {kpis.get('total_customers', 0)}\n")
        f.write(f"Average Frequency: {kpis.get('average_frequency', 0)}\n\n")

        f.write("Segment Distribution:\n")
        for segment, count in kpis.get("segment_distribution", {}).items():
            f.write(f"  - {segment}: {count}\n")

        f.write("\nRevenue by Segment:\n")
        for segment, revenue in kpis.get("revenue_by_segment", {}).items():
            f.write(f"  - {segment}: {revenue}\n")

    return file_path