from sklearn.cluster import KMeans
import pandas as pd


def segment_customers(df):
    """
    Segments customers using K-Means clustering
    based on revenue and frequency.
    Phase 2: ML-based segmentation.
    """

    # Ensure required columns exist
    if "revenue" not in df.columns or "frequency" not in df.columns:
        raise ValueError("Required columns missing for segmentation")

    # Select features for clustering
    features = df[["revenue", "frequency"]]

    # Initialize KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

    # Fit and predict clusters
    df["cluster"] = kmeans.fit_predict(features)

    # Calculate cluster centers
    cluster_centers = pd.DataFrame(
        kmeans.cluster_centers_,
        columns=["revenue", "frequency"]
    )

    # Rank clusters based on revenue
    cluster_centers["rank"] = cluster_centers["revenue"].rank(ascending=False)

    # Map cluster numbers to business labels dynamically
    cluster_label_map = {}

    for idx, row in cluster_centers.iterrows():
        if row["rank"] == 1:
            cluster_label_map[idx] = "Premium"
        elif row["rank"] == 2:
            cluster_label_map[idx] = "Mid Value"
        else:
            cluster_label_map[idx] = "Low Value"

    # Assign segment labels
    df["segment"] = df["cluster"].map(cluster_label_map)

    return df