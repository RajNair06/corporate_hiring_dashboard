# Run: streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------- MODEL --------
def logistic_growth(t, P0, K, r):
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Hiring Dashboard", layout="wide")

st.title("📊 Hiring Dashboard")

# -------- INPUTS --------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Inputs")

    P0 = st.number_input("Initial Employees", min_value=1, value=50)
    K = st.number_input("Max Workforce", min_value=1, value=500)
    r = st.number_input("Growth Rate", min_value=0.01, value=0.3)
    time_period = st.number_input("Time (Months)", min_value=1, value=24)

    simulate = st.button("Simulate")

# -------- OUTPUT --------
with col2:
    st.subheader("Analysis")

    if simulate:

        # Validation
        if K <= P0:
            st.error("Max Workforce must be greater than Initial Employees")
            st.stop()

        # Compute
        t = np.linspace(0, time_period, 100)
        employees = logistic_growth(t, P0, K, r)

        df = pd.DataFrame({
            "Time (Months)": np.round(t, 2),
            "Employees": employees.astype(int)
        })

        # -------- METRICS --------
        m1, m2, m3 = st.columns(3)
        m1.metric("Start", P0)
        m2.metric("End", int(df["Employees"].iloc[-1]))
        m3.metric("Capacity %", f"{(df['Employees'].iloc[-1]/K)*100:.1f}%")

        # -------- GRAPH --------
        fig, ax = plt.subplots(figsize=(8,4))

        ax.plot(df["Time (Months)"], df["Employees"], linewidth=3)
        ax.fill_between(df["Time (Months)"], df["Employees"], alpha=0.15)

        ax.axhline(K, linestyle="--", linewidth=2, label="Max Workforce")

        ax.set_title("Employee Growth")
        ax.set_xlabel("Time (Months)")
        ax.set_ylabel("Employees")

        ax.grid(alpha=0.3)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        # -------- TABLE --------
        st.dataframe(df, use_container_width=True)

        # -------- SIMPLE INTERACTION --------
        index = st.slider("Select Month Index", 0, len(df)-1, 0)

        row = df.iloc[index]
        st.write(f"Month: {row['Time (Months)']}")
        st.write(f"Employees: {row['Employees']}")