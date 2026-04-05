
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ─────────────────────────────────────────────────────────────
# LOGISTIC GROWTH MODEL (Simple & Realistic)
# ─────────────────────────────────────────────────────────────
def logistic_growth(t, P0, K, r):
    """Logistic growth formula used in business forecasting.
    - Starts fast when capacity is abundant
    - Gradually slows as the workforce approaches maximum capacity (K)"""
    return K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hiring Growth Simulator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Hiring Growth Simulator")
st.markdown("""
**A professional tool to forecast workforce expansion.**  
This simulator uses a **logistic growth model** — the same approach many companies use to plan hiring while respecting real-world limits like budget, office space, and management bandwidth.
""")

# ─────────────────────────────────────────────────────────────
# SIDEBAR – INPUT PARAMETERS (Clean & Professional)
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Simulation Parameters")
    
    P0 = st.number_input(
        "Initial Employees",
        min_value=1,
        value=50,
        help="Starting size of your workforce."
    )
    
    K = st.number_input(
        "Maximum Workforce Capacity",
        min_value=10,
        value=500,
        help="Target headcount the company plans to support (budget, space, infrastructure)."
    )
    
    r = st.number_input(
        "Growth Rate (per month)",
        min_value=0.01,
        max_value=2.0,
        value=0.30,
        step=0.01,
        help="How quickly hiring happens early on. Higher = faster initial ramp-up."
    )
    
    time_period = st.number_input(
        "Simulation Period (Months)",
        min_value=1,
        value=24,
        help="How many months into the future you want to project."
    )
    
    st.caption("Tip: Try different values to see how growth changes.")

# ─────────────────────────────────────────────────────────────
# MAIN AREA – RESULTS
# ─────────────────────────────────────────────────────────────
st.subheader("📈 Simulation Results")

# Basic validation
if K <= P0:
    st.error("⚠️ Maximum Workforce Capacity must be greater than Initial Employees.")
    st.stop()

# Run simulation (automatically updates when you change inputs)
t = np.linspace(0, time_period, 200)                    # 200 points for smooth curve
employees = logistic_growth(t, P0, K, r)

# Create clean DataFrame
df = pd.DataFrame({
    "Time (Months)": np.round(t, 1),
    "Employees": np.round(employees).astype(int)
})

final_emp = df["Employees"].iloc[-1]
capacity_used = (final_emp / K) * 100

# ── KEY METRICS ──
col1, col2, col3 = st.columns(3)
col1.metric("Starting Headcount", f"{P0:,}")
col2.metric("Projected Headcount", f"{final_emp:,}", 
            delta=f"+{final_emp - P0:,} employees")
col3.metric("Capacity Utilization", f"{capacity_used:.1f}%")

# ── SIMPLE GROWTH INSIGHTS ──
st.subheader("📌 Growth Phase Analysis")

mid_index = len(df) // 2
start_val = df["Employees"].iloc[0]
mid_val   = df["Employees"].iloc[mid_index]
end_val   = df["Employees"].iloc[-1]

early_growth = mid_val - start_val
late_growth  = end_val - mid_val

if early_growth > late_growth * 1.5:
    st.success("📈 **Hiring is still accelerating** — most of the growth is still ahead.")
elif late_growth > early_growth * 1.5:
    st.info("📉 **Hiring momentum is slowing** — capacity limits are beginning to take effect.")
else:
    st.info("⚖️ **Hiring is at its peak growth phase** — this is typically the fastest period of expansion.")

# Gentle, professional notes
if r > 0.8:
    st.caption("Note: A very high growth rate is shown. In reality, operational limits (training, culture, budget) usually slow hiring before the model predicts.")
elif r < 0.08:
    st.caption("Note: Growth is gradual. Depending on your hiring strategy, reaching the target may take longer than shown.")

if capacity_used > 85:
    st.caption("The workforce is approaching its planned maximum capacity.")
elif capacity_used < 40:
    st.caption("There is still significant room for expansion.")

# ── VISUAL DEMONSTRATION ──
st.subheader("Growth Curve")
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(df["Time (Months)"], df["Employees"], 
        color="#1f77b4", linewidth=3.5, label="Projected Employees")
ax.fill_between(df["Time (Months)"], df["Employees"], 
                color="#1f77b4", alpha=0.15)

ax.axhline(y=K, color="#d62728", linestyle="--", linewidth=2, 
           label=f"Maximum Capacity ({K} employees)")

ax.set_title("Workforce Growth Over Time", fontsize=16, pad=20)
ax.set_xlabel("Time (Months)", fontsize=12)
ax.set_ylabel("Number of Employees", fontsize=12)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

# Clean up plot
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

# ── DATA TABLE & INSPECTOR ──
st.subheader("📋 Detailed Data")

with st.expander("View full simulation table", expanded=False):
    st.dataframe(
        df.style.format({"Employees": "{:,}"}),
        use_container_width=True,
        hide_index=True
    )

# Interactive inspector
st.markdown("**Inspect any month**")
index = st.slider(
    "Select month to inspect",
    min_value=0,
    max_value=len(df)-1,
    value=0,
    step=1
)

selected = df.iloc[index]
st.markdown(f"""
**Month {selected['Time (Months)']:.1f}**  
**Employees:** {selected['Employees']:,}
""")

# ── SIMPLE MODEL EXPLANATION (for easy understanding) ──
with st.expander("💡 How the Logistic Growth Model Works"):
    st.markdown("""
    This model is widely used in business because it reflects **real-world hiring**:
    
    1. **Early stage** → Hiring is fast (lots of open roles, easy to scale)  
    2. **Middle stage** → Growth reaches its maximum speed  
    3. **Late stage** → Growth naturally slows as the company approaches its planned capacity (budget, office space, management bandwidth)
    
    The curve you see is called an **S-curve** — the most realistic way to forecast workforce expansion.
    """)