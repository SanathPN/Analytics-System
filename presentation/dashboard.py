import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from services.segmentation_service import segment_customers

API_URL = "https://your-render-url.onrender.com/upload"  # UPDATE THIS

st.set_page_config(page_title="ML Analytics Dashboard", layout="wide")

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
        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        files = {"file": open("temp.csv", "rb")}
        requests.post(API_URL, files=files)

# ==========================
# LOAD DATA
# ==========================
if os.path.exists("temp.csv"):

    df = pd.read_csv("temp.csv")
    df = segment_customers(df)

    # Sidebar Filters
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

    # --------------------------
    # TAB 1: MAIN DASHBOARD
    # --------------------------
    with tab1:

        st.title("📊 Executive Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Revenue", f"${df['revenue'].sum():.2f}")
        col2.metric("Avg Revenue", f"${df['revenue'].mean():.2f}")
        col3.metric("Customers", len(df))
        col4.metric("Avg Frequency", f"{df['frequency'].mean():.2f}")

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

    # --------------------------
    # TAB 2: SEGMENT COMPARISON
    # --------------------------
    with tab2:

        st.title("📈 Segment Comparison Analysis")

        comparison_df = df.groupby("segment").agg(
            revenue_sum=("revenue", "sum"),
            avg_frequency=("frequency", "mean"),
            customer_count=("segment", "count")
        )

        st.dataframe(comparison_df)

        st.bar_chart(comparison_df["revenue_sum"])

    # --------------------------
    # TAB 3: DOWNLOAD
    # --------------------------
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
