import sys
import os

# Add project root to Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from services.segmentation_service import segment_customers
from services.validation_service import validate_dataset

API_URL = "https://your-render-url.onrender.com/upload"  # UPDATE THIS

st.set_page_config(page_title="ML Analytics Dashboard", layout="wide")

TEMP_PATH = os.path.join(BASE_DIR, "temp.csv")

# ==========================
# CACHING FUNCTIONS
# ==========================

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

@st.cache_data
def get_segmented_data(df):
    return segment_customers(df)

@st.cache_data
def compute_kpis(df):
    return {
        "total_revenue": df["revenue"].sum(),
        "avg_revenue": df["revenue"].mean(),
        "total_customers": len(df),
        "avg_frequency": df["frequency"].mean()
    }

# ==========================
# ROLE SETUP
# ==========================

USERS = {
    "admin": {"password": "1234", "role": "Admin"},
    "analyst": {"password": "abcd", "role": "Analyst"}
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None

# ==========================
# LOGIN
# ==========================

if not st.session_state.authenticated:
    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.role = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("Controls")
st.sidebar.success(f"Logged in as: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.role = None
    st.rerun()

# ==========================
# ADMIN UPLOAD
# ==========================

if st.session_state.role == "Admin":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        with open(TEMP_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())

        files = {"file": open(TEMP_PATH, "rb")}
        requests.post(API_URL, files=files)

# ==========================
# LOAD DATA
# ==========================

if os.path.exists(TEMP_PATH):

    try:
        df = load_data(TEMP_PATH)

        # Validate first
        validate_dataset(df)

        # Then segment
        df = get_segmented_data(df)

    except Exception as e:
        st.error(f"Validation Error: {str(e)}")
        st.stop()

    # ==========================
    # SIDEBAR FILTERS
    # ==========================

    st.sidebar.subheader("Filters")

    selected_segments = st.sidebar.multiselect(
        "Select Segments",
        options=df["segment"].unique(),
        default=df["segment"].unique()
    )

    min_revenue = st.sidebar.slider(
        "Minimum Revenue",
        min_value=int(df["revenue"].min()),
        max_value=int(df["revenue"].max()),
        value=int(df["revenue"].min())
    )

    df = df[df["segment"].isin(selected_segments)]
    df = df[df["revenue"] >= min_revenue]

    # ==========================
    # TABS
    # ==========================

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 Segment Comparison", "📥 Download"])

    with tab1:
        st.title("📊 Executive Dashboard")

        kpis = compute_kpis(df)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Revenue", f"${kpis['total_revenue']:.2f}")
        col2.metric("Avg Revenue", f"${kpis['avg_revenue']:.2f}")
        col3.metric("Customers", kpis["total_customers"])
        col4.metric("Avg Frequency", f"{kpis['avg_frequency']:.2f}")

        st.subheader("Segment Distribution")
        st.bar_chart(df["segment"].value_counts())

        st.subheader("Revenue by Segment")
        st.bar_chart(df.groupby("segment")["revenue"].sum())

        st.subheader("Customer Segmentation (Scatter View)")

        fig, ax = plt.subplots(figsize=(4, 3))

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
        ax.legend()

        st.pyplot(fig)

    with tab2:
        st.title("📈 Segment Comparison Analysis")

        comparison_df = df.groupby("segment").agg(
            revenue_sum=("revenue", "sum"),
            avg_frequency=("frequency", "mean"),
            customer_count=("segment", "count")
        )

        st.dataframe(comparison_df)
        st.bar_chart(comparison_df["revenue_sum"])

    with tab3:
        st.title("📥 Download Data")

        csv_data = df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

else:
    st.warning("No dataset uploaded yet.")