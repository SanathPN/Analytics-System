import os
import time
import logging
import pandas as pd
from flask import Flask, request, jsonify

from services.validation_service import validate_dataset
from services.preprocessing_service import preprocess_dataset
from services.segmentation_service import segment_customers
from services.analytics_service import calculate_kpis
from database.repository import save_records

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# -------------------------------
# Health Check Route
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    logger.info("Health check endpoint accessed")
    return jsonify({
        "status": "Analytics System Running",
        "message": "Cloud Deployment Active"
    })


# -------------------------------
# Upload & Process Route
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():

    start_time = time.time()

    if "file" not in request.files:
        logger.warning("Upload attempt without file")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        logger.info("File upload received")

        # Read CSV
        df = pd.read_csv(file)

        logger.info(f"Dataset size received: {len(df)} records")

        # Validate
        validate_dataset(df)
        logger.info("Dataset validation completed")

        # Preprocess
        df = preprocess_dataset(df)
        logger.info("Preprocessing completed")

        # Segment
        df = segment_customers(df)
        logger.info("Segmentation completed")

        # Calculate KPIs
        kpis = calculate_kpis(df)
        logger.info("KPI calculation completed")

        # Save to database
        save_records(df)
        logger.info("Database save completed")

        end_time = time.time()
        processing_time = round(end_time - start_time, 4)

        logger.info(f"Processing time: {processing_time} seconds")

        return jsonify({
            "message": "File processed successfully",
            "records_processed": len(df),
            "processing_time_seconds": processing_time,
            "kpis": kpis
        })

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Run Application (Cloud Ready)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)