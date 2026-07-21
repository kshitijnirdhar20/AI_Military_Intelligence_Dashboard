import streamlit as st

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Military Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

st.sidebar.title("🛡️ AI Military Dashboard")
st.sidebar.markdown("### Version 2.0")

st.sidebar.info("""
Welcome to the AI-Based Military Intelligence Dashboard.

Use the sidebar to navigate through different modules.
""")

st.sidebar.markdown("---")

st.sidebar.success("""
Modules

🏠 Home

🌍 Global Threat Map

🌎 Country Analysis

🤖 Attack Prediction

🚨 Threat Level

📈 Forecasting

🧠 AI Intelligence Report

📊 Data Explorer

⚙ Settings
""")

st.sidebar.markdown("---")
st.sidebar.caption("Internship Project | Version 2.0")

# -----------------------------------------------------
# Main Page
# -----------------------------------------------------

st.title("🛡️ AI-Based Military Intelligence Dashboard")

st.markdown("""
## Welcome

The AI-Based Military Intelligence Dashboard is designed to analyze
terrorism-related incidents using Machine Learning and Data Analytics.

It provides:

- 🌍 Global Threat Monitoring
- 📊 Data Visualization
- 🤖 AI-Based Attack Prediction
- 🚨 Threat Level Assessment
- 📈 Forecasting
- 🧠 Intelligence Report Generation
""")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("🎯 Objectives")

    st.write("""
- Analyze historical terrorism incidents

- Predict attack types using Machine Learning

- Forecast future threats

- Generate intelligence reports

- Assist strategic decision-making
""")

with col2:

    st.subheader("🛠 Technologies Used")

    st.write("""
- Python

- Streamlit

- Pandas

- Plotly

- Scikit-Learn

- Joblib
""")

st.divider()

st.success("👈 Select any module from the left sidebar to begin.")

st.caption("Developed as an Internship Project | AI Military Intelligence Dashboard Version 2.0")