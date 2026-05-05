import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from services.segmentation_service import segment_customers

API_URL = "http://127.0.0.1:5000/upload"

st.set_page_config(page_title="ML Analytics Dashboard", layout="wide")

# ==========================
# ROLE DEFINITIONS
# ==========================
USERS = {
    "admin": {"password": "1234", "role": "Admin"},
    "analyst": {"password": "abcd", "role": "Analyst"}
}

# ==========================
# SESSION INIT
# ==========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "role" not in st.session_state:
    st.session_state.role = None

# ==========================
# LOGIN PAGE
# ==========================
if not st.session_state.authenticated:

    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.role = USERS[username]["role"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ==========================
# DASHBOARD
# ==========================
st.title("📊 Intelligent Marketing Analytics System (ML-Based)")

st.sidebar.success(f"Logged in as: {st.session_state.role}")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.role = None
    st.rerun()

# ==========================
# UPLOAD (ADMIN ONLY)
# ==========================
if st.session_state.role == "Admin":
    st.header("Upload Dataset (Admin Access)")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:

        with st.spinner("Processing dataset..."):

            with open("temp.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())

            files = {"file": open("temp.csv", "rb")}
            response = requests.post(API_URL, files=files)

            if response.status_code == 200:
                st.success("File processed successfully!")
            else:
                st.error("Error processing file.")
                st.write(response.text)

else:
    st.info("📊 Analyst role: View-only access")

# ==========================
# DISPLAY DASHBOARD
# ==========================
if os.path.exists("temp.csv"):

    df = pd.read_csv("temp.csv")
    df = segment_customers(df)

    # Compute locally for analyst view
    total_revenue = df["revenue"].sum()
    avg_revenue = df["revenue"].mean()
    total_customers = len(df)
    avg_frequency = df["frequency"].mean()

    st.header("Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${total_revenue:.2f}")
    col2.metric("Avg Revenue", f"${avg_revenue:.2f}")
    col3.metric("Total Customers", total_customers)
    col4.metric("Avg Frequency", f"{avg_frequency:.2f}")

    # Segment Distribution
    st.header("Segment Distribution")
    st.bar_chart(df["segment"].value_counts())

    # Revenue by Segment
    st.header("Revenue by Segment")
    st.bar_chart(df.groupby("segment")["revenue"].sum())

    # Cluster Visualization
    st.header("Customer Segmentation (Cluster Visualization)")

    fig, ax = plt.subplots(figsize=(3.5, 2.5))

    for segment in df["segment"].unique():
        subset = df[df["segment"] == segment]
        ax.scatter(
            subset["revenue"],
            subset["frequency"],
            label=segment,
            alpha=0.7
        )

    ax.set_xlabel("Revenue")
    ax.set_ylabel("Frequency")
    ax.set_title("Revenue vs Frequency Clusters")
    ax.legend()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.pyplot(fig)

else:
    st.warning("No dataset uploaded yet.")