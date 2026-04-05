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
st.caption("Simulate how a company's workforce grows over time using a logistic model.")

# -------- SESSION STATE --------
if "run_simulation" not in st.session_state:
    st.session_state.run_simulation = False

# -------- INPUTS --------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Inputs")

    P0 = st.number_input("Initial Employees", min_value=1, value=50)
    K = st.number_input("Max Workforce (Capacity)", min_value=1, value=500)
    r = st.number_input("Growth Rate", min_value=0.01, value=0.3)
    time_period = st.number_input("Time (Months)", min_value=1, value=24)

    if st.button("Simulate"):
        st.session_state.run_simulation = True

    st.markdown("---")

    # -------- EXPLANATION --------
    st.info(
        "📘 Hiring starts fast, then slows as it approaches maximum capacity.\n\n"
        "This model reflects real-world constraints like budget, space, and management limits."
    )

# -------- OUTPUT --------
with col2:
    st.subheader("Analysis")

    if st.session_state.run_simulation:

        if K <= P0:
            st.error("Max Workforce must be greater than Initial Employees")
            st.stop()

        # -------- COMPUTE --------
        t = np.linspace(0, time_period, 100)
        employees = logistic_growth(t, P0, K, r)

        df = pd.DataFrame({
            "Time (Months)": np.round(t, 2),
            "Employees": employees.astype(int)
        })

        final_emp = int(df["Employees"].iloc[-1])
        capacity_used = (final_emp / K) * 100

        # -------- METRICS --------
        m1, m2, m3 = st.columns(3)
        m1.metric("Start", P0)
        m2.metric("End", final_emp)
        m3.metric("Capacity Used", f"{capacity_used:.1f}%")

        # -------- SMART INSIGHTS (IMPROVED) --------

        mid_index = len(df) // 2

        start_val = df["Employees"].iloc[0]
        mid_val = df["Employees"].iloc[mid_index]
        end_val = df["Employees"].iloc[-1]

        early_growth = mid_val - start_val
        late_growth = end_val - mid_val

        # Detect phase of growth
        if early_growth > late_growth * 1.5:
            st.info("📈 Hiring is still accelerating. Most of the growth is ahead.")
        elif late_growth > early_growth * 1.5:
            st.info("📉 Hiring momentum is slowing down as capacity limits start to take effect.")
        else:
            st.info("⚖️ Hiring is near its peak growth phase — this is where expansion happens fastest.")

        # Subtle realism checks (not aggressive warnings)
        if r > 0.8:
            st.caption("Note: The growth rate is quite high — real-world hiring usually faces operational limits.")
        elif r < 0.08:
            st.caption("Note: Growth is gradual — scaling may take longer depending on hiring strategy.")

        # Capacity interpretation (more natural)
        if capacity_used > 85:
            st.caption("The workforce is approaching its planned limit.")
        elif capacity_used < 40:
            st.caption("There is still significant room for expansion.")

        # -------- GRAPH --------
        fig, ax = plt.subplots(figsize=(8,4))

        ax.plot(df["Time (Months)"], df["Employees"], linewidth=3)
        ax.fill_between(df["Time (Months)"], df["Employees"], alpha=0.15)
        ax.axhline(K, linestyle="--", linewidth=2, label="Max Workforce")

        ax.set_title("Employee Growth Over Time")
        ax.set_xlabel("Time (Months)")
        ax.set_ylabel("Employees")

        ax.grid(alpha=0.3)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        # -------- TABLE --------
        with st.expander("📋 View Data Table"):
            st.dataframe(df, use_container_width=True)

        # -------- INTERACTIVE POINT --------
        index = st.slider("Inspect Month", 0, len(df)-1, 0)

        row = df.iloc[index]

        st.markdown(
            f"""
            **📍 Month:** {row['Time (Months)']}  
            **👥 Employees:** {row['Employees']}
            """
        )

    else:
        st.info("Enter values and click **Simulate** to view results.")