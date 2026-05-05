import pandas as pd
import numpy as np
import time
from services.segmentation_service import segment_customers

def generate_dataset(size):
    return pd.DataFrame({
        "revenue": np.random.randint(100, 5000, size),
        "frequency": np.random.randint(1, 20, size)
    })

def test_performance(size):
    df = generate_dataset(size)

    start_time = time.time()

    df = segment_customers(df)

    end_time = time.time()

    processing_time = end_time - start_time

    print(f"\nDataset Size: {size}")
    print(f"Processing Time: {processing_time:.4f} seconds")
    print(f"Records per second: {size / processing_time:.2f}")

if __name__ == "__main__":
    test_performance(10000)
    test_performance(50000)