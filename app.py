# NOTE:
# Run using: streamlit run app.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# -------- MODEL --------
def logistic_growth(t, P0, K, r):
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Hiring Dashboard", layout="wide")

# -------- CUSTOM UI --------
st.markdown("""
<style>
.stApp { background-color: #1E1F3A; }
.main > div {
    background-color: #25274D;
    border: 3px solid #6C63FF;
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(157,78,221,0.6);
    padding: 20px;
}
.header-box {
    background: linear-gradient(90deg, #5F4BFF, #A259FF, #C77DFF);
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box">📊 Corporate Hiring Dashboard</div>', unsafe_allow_html=True)

# -------- INPUTS --------
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("🧾 Inputs")

    P0 = st.number_input("Initial Employees", min_value=1, value=50)
    K = st.number_input("Max Workforce", min_value=1, value=500)
    r = st.number_input("Growth Rate", min_value=0.01, value=0.3)
    time_period = st.number_input("Time (Months)", min_value=1, value=24)

    simulate = st.button("Simulate")

# -------- OUTPUT --------
with col2:
    st.subheader("📊 Analysis")

    if simulate:

        # -------- VALIDATION --------
        if K <= P0:
            st.error("Max Workforce (K) must be greater than Initial Employees (P0)")
            st.stop()

        # -------- COMPUTATION --------
        t = np.linspace(0, time_period, 50)
        employees = logistic_growth(t, P0, K, r)

        df = pd.DataFrame({
            "Time (Months)": np.round(t, 2),
            "Employees": employees.astype(int)
        })

        # -------- LAYOUT --------
        gcol, tcol = st.columns([1.2, 1])

        # -------- GRAPH --------
        with gcol:
            selected_col = st.radio("Select Data", df.columns.tolist(), horizontal=True)

            fig, ax = plt.subplots(figsize=(7,4))  # bigger figure

            # -------- MAIN LINE --------
            ax.plot(
                df["Time (Months)"], 
                df[selected_col],
                linewidth=3,
                marker='o',
                markersize=4
            )

            # -------- AREA FILL (important visual improvement) --------
            if selected_col == "Employees":
                ax.fill_between(
                    df["Time (Months)"], 
                    df["Employees"], 
                    alpha=0.2
                )

            # -------- GRID --------
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

            # -------- LABELS --------
            ax.set_xlabel("Time (Months)", fontsize=10)
            ax.set_ylabel(selected_col, fontsize=10)

            # -------- TITLE --------
            ax.set_title(f"{selected_col} Growth Over Time", fontsize=13, weight='bold')

            # -------- DARK THEME FIX --------
            ax.set_facecolor('#25274D')
            fig.patch.set_facecolor('#25274D')

            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')

            # -------- SPINES (clean look) --------
            for spine in ax.spines.values():
                spine.set_color("#6C63FF")

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)  # ✅ IMPORTANT FIX

        # -------- TABLE --------
        with tcol:
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection(selection_mode="single", use_checkbox=True)
            gridOptions = gb.build()

            grid_response = AgGrid(df, gridOptions=gridOptions, height=300)

            selected = grid_response.get("selected_rows", [])

            if selected:
                row = selected[0]
                st.write(f"📍 Selected Month: {row['Time (Months)']}")
                st.write(f"👥 Employees: {row['Employees']}")