import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="AgNPs Simulation App", layout="wide")

# Title and description
st.title("🧬 Silver Nanoparticles Simulation & Applications")
st.markdown("""
This interactive tool simulates the applications of **green-synthesized silver nanoparticles (AgNPs)** in:
- Antibacterial activity
- Biofilm inhibition
- Antioxidant capacity
- Photocatalytic dye degradation

Adjust the concentration to see how AgNPs perform across biomedical and environmental applications.
""")

# Sidebar controls
st.sidebar.header("🔧 Simulation Parameters")
max_conc = st.sidebar.slider("Maximum Concentration (µg/ml)", 10, 200, 100, step=10)
conc_step = st.sidebar.slider("Step Size (µg/ml)", 1, 20, 10)
decay_rate = st.sidebar.slider("Dye Degradation Rate (0.01 - 0.2)", 0.01, 0.2, 0.05, step=0.01)

# Generate concentration and time arrays
concentrations = np.arange(0, max_conc + conc_step, conc_step)
time = np.linspace(0, 60, 13)  # 0 to 60 minutes, 5-minute intervals

# Mathematical models for AgNPs effects
# Zone of Inhibition (mm) - quadratic model with diminishing returns
zoi = 5 + 0.15 * concentrations - 0.001 * concentrations**2
zoi = np.maximum(zoi, 0)  # Ensure non-negative values

# Biofilm Inhibition (%) - quadratic model with saturation
biofilm_inhibition = 20 + 0.6 * concentrations - 0.003 * concentrations**2
biofilm_inhibition = np.clip(biofilm_inhibition, 0, 100)  # Keep between 0-100%

# Antioxidant RSA (%) - quadratic model with saturation
antioxidant_rsa = 10 + 0.7 * concentrations - 0.002 * concentrations**2
antioxidant_rsa = np.clip(antioxidant_rsa, 0, 100)  # Keep between 0-100%

# Dye degradation - exponential decay model
dye_conc = 100 * np.exp(-decay_rate * time)

# Create DataFrames
df_applications = pd.DataFrame({
    "Concentration (µg/ml)": concentrations,
    "Zone of Inhibition (mm)": np.round(zoi, 2),
    "Biofilm Inhibition (%)": np.round(biofilm_inhibition, 2),
    "Antioxidant RSA (%)": np.round(antioxidant_rsa, 2)
})

df_dye_degradation = pd.DataFrame({
    "Time (min)": time,
    "Remaining Dye (mg/L)": np.round(dye_conc, 2)
})

# Display data table
st.subheader("📊 AgNPs Biomedical Applications Data")
st.dataframe(df_applications, use_container_width=True)

# Create plots in two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Antibacterial Activity**")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(concentrations, zoi, marker='o', linewidth=2, markersize=6, color='blue')
    ax1.set_xlabel("Concentration (µg/ml)", fontsize=12)
    ax1.set_ylabel("Zone of Inhibition (mm)", fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Antibacterial Activity vs Concentration", fontsize=14)
    st.pyplot(fig1)
    plt.close()
    
    st.markdown("**Antioxidant Activity**")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.plot(concentrations, antioxidant_rsa, marker='^', linewidth=2, markersize=6, color='orange')
    ax3.set_xlabel("Concentration (µg/ml)", fontsize=12)
    ax3.set_ylabel("RSA (%)", fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.set_title("Antioxidant Activity vs Concentration", fontsize=14)
    ax3.set_ylim(0, 100)
    st.pyplot(fig3)
    plt.close()

with col2:
    st.markdown("**Biofilm Inhibition**")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(concentrations, biofilm_inhibition, marker='s', linewidth=2, markersize=6, color='green')
    ax2.set_xlabel("Concentration (µg/ml)", fontsize=12)
    ax2.set_ylabel("Biofilm Inhibition (%)", fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_title("Biofilm Inhibition vs Concentration", fontsize=14)
    ax2.set_ylim(0, 100)
    st.pyplot(fig2)
    plt.close()
    
    st.markdown("**Photocatalytic Dye Degradation**")
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    ax4.plot(time, dye_conc, marker='x', linewidth=2, markersize=8, color='red')
    ax4.set_xlabel("Time (min)", fontsize=12)
    ax4.set_ylabel("Dye Concentration (mg/L)", fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.set_title("Dye Degradation Over Time", fontsize=14)
    st.pyplot(fig4)
    plt.close()

# Summary statistics
st.subheader("📈 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Max Zone of Inhibition", f"{np.max(zoi):.1f} mm", f"at {concentrations[np.argmax(zoi)]:.0f} µg/ml")

with col2:
    st.metric("Max Biofilm Inhibition", f"{np.max(biofilm_inhibition):.1f}%", f"at {concentrations[np.argmax(biofilm_inhibition)]:.0f} µg/ml")

with col3:
    st.metric("Max Antioxidant RSA", f"{np.max(antioxidant_rsa):.1f}%", f"at {concentrations[np.argmax(antioxidant_rsa)]:.0f} µg/ml")

with col4:
    st.metric("Dye Degradation (60 min)", f"{100 - dye_conc[-1]:.1f}%", f"Rate: {decay_rate:.3f}")

# Export options
st.subheader("📥 Download Data")
col1, col2 = st.columns(2)

with col1:
    csv_applications = df_applications.to_csv(index=False)
    st.download_button(
        label="📊 Download Applications Data (CSV)",
        data=csv_applications,
        file_name="agnp_applications.csv",
        mime="text/csv"
    )

with col2:
    csv_degradation = df_dye_degradation.to_csv(index=False)
    st.download_button(
        label="🧪 Download Dye Degradation Data (CSV)",
        data=csv_degradation,
        file_name="dye_degradation.csv",
        mime="text/csv"
    )

# Additional information
st.subheader("ℹ️ Model Information")
st.markdown("""
**Mathematical Models Used:**
- **Antibacterial Activity**: Quadratic model with diminishing returns at higher concentrations
- **Biofilm Inhibition**: Concentration-dependent with saturation effect
- **Antioxidant Activity**: Dose-response relationship with plateau
- **Dye Degradation**: First-order exponential decay kinetics

**Parameters:**
- All biological activities are modeled to show realistic dose-response relationships
- Dye degradation follows photocatalytic kinetics with adjustable rate constant
- Values are representative of typical AgNPs performance in literature
""")

# Footer
st.markdown("""
---
**Developed by Muhammad Nabeel Saddique**  
4th Year MBBS, King Edward Medical University  
Founder, Nibras Research Academy

**Developed by Hira Tariq, BS, MS**  
Masters in Microbiology, Punjab University  
Ambassador, Nibras Research Academy

*This simulation is for educational and research purposes. Actual experimental results may vary.*
""")
