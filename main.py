from flask import Flask, request, jsonify
import os
import pandas as pd

# Import services
from services.validation_service import validate_csv
from services.preprocessing_service import preprocess_data
from services.segmentation_service import segment_customers
from services.analytics_service import calculate_kpis
from database.repository import save_to_database

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -------------------------------
# Home Route (Health Check)
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Analytics System Running",
        "message": "Phase 1 Prototype Active"
    })


# -------------------------------
# File Upload + Processing Route
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload_file():

    # Check file presence
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400

    try:
        # Save uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Step 1: Validate
        df = validate_csv(file_path)

        # Step 2: Preprocess
        df = preprocess_data(df)

        # Step 3: Segmentation
        df = segment_customers(df)

        # Step 4: Analytics
        kpis = calculate_kpis(df)

        # Step 5: Save to Database
        save_to_database(df)

        return jsonify({
            "message": "File processed successfully",
            "records_processed": len(df),
            "kpis": kpis
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)