import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Dashboard Settings")

st.markdown("""
Configure the AI-Based Military Intelligence Dashboard.
""")

st.sidebar.header("Quick Settings")

theme = st.sidebar.selectbox(
    "Dashboard Theme",
    [
        "Light",
        "Dark"
    ]
)

layout = st.sidebar.selectbox(
    "Layout",
    [
        "Wide",
        "Centered"
    ]
)

chart_style = st.sidebar.selectbox(
    "Chart Style",
    [
        "Plotly",
        "Bar",
        "Line",
        "Pie"
    ]
)

st.subheader("🎨 Appearance")

c1, c2, c3 = st.columns(3)

with c1:

    theme = st.selectbox(
        "Theme",
        [
            "Light",
            "Dark"
        ]
    )

with c2:

    layout = st.selectbox(
        "Dashboard Layout",
        [
            "Wide",
            "Centered"
        ]
    )

with c3:

    chart_style = st.selectbox(
        "Default Chart",
        [
            "Plotly",
            "Bar",
            "Line",
            "Pie"
        ]
    )

st.divider()

st.subheader("🌍 Default Dashboard Settings")

col1, col2 = st.columns(2)

with col1:

    default_country = st.text_input(
        "Default Country",
        "India"
    )

    forecast_years = st.slider(
        "Forecast Years",
        1,
        10,
        5
    )

with col2:

    confidence = st.slider(
        "Minimum Prediction Confidence",
        50,
        100,
        80
    )

    refresh_rate = st.selectbox(
        "Auto Refresh",
        [
            "Off",
            "30 Seconds",
            "1 Minute",
            "5 Minutes"
        ]
    )

st.divider()
st.subheader("🗺️ Map Configuration")

col1, col2 = st.columns(2)

with col1:

    map_style = st.selectbox(
        "Map Style",
        [
            "Natural Earth",
            "OpenStreetMap",
            "Carto Positron",
            "Carto Dark"
        ]
    )

    marker_size = st.slider(
        "Marker Size",
        2,
        20,
        8
    )

with col2:

    show_cluster = st.checkbox(
        "Enable Marker Clustering",
        value=True
    )

    show_heatmap = st.checkbox(
        "Enable Heatmap",
        value=False
    )

st.divider()

st.subheader("🤖 AI & Machine Learning Settings")

left, right = st.columns(2)

with left:

    prediction_model = st.selectbox(
        "Attack Prediction Model",
        [
            "Random Forest",
            "Decision Tree",
            "Gradient Boosting"
        ]
    )

    forecasting_model = st.selectbox(
        "Forecasting Model",
        [
            "Linear Regression",
            "ARIMA",
            "Prophet"
        ]
    )

with right:

    show_probability = st.checkbox(
        "Show Prediction Probability",
        value=True
    )

    show_feature_importance = st.checkbox(
        "Show Feature Importance",
        value=True
    )

st.divider()

st.subheader("⚡ Dashboard Performance")

p1, p2, p3 = st.columns(3)

p1.metric(
    "Prediction Engine",
    "Online"
)

p2.metric(
    "Forecast Model",
    "Ready"
)

p3.metric(
    "Dashboard Status",
    "Active"
)

st.divider()
st.subheader("📄 Report Settings")

left, right = st.columns(2)

with left:

    report_format = st.selectbox(
        "Default Report Format",
        [
            "PDF",
            "Word",
            "Text"
        ]
    )

    include_charts = st.checkbox(
        "Include Charts",
        value=True
    )

    include_tables = st.checkbox(
        "Include Tables",
        value=True
    )

with right:

    report_theme = st.selectbox(
        "Report Theme",
        [
            "Professional",
            "Military",
            "Minimal"
        ]
    )

    auto_download = st.checkbox(
        "Auto Download Report",
        value=False
    )

    watermark = st.checkbox(
        "Add Watermark",
        value=True
    )

st.divider()

st.subheader("🔔 Notification Settings")

n1, n2, n3 = st.columns(3)

with n1:

    attack_alert = st.checkbox(
        "Attack Alerts",
        value=True
    )

with n2:

    forecast_alert = st.checkbox(
        "Forecast Alerts",
        value=True
    )

with n3:

    report_notification = st.checkbox(
        "Report Notifications",
        value=False
    )

st.divider()

st.subheader("📊 Dataset Information")

try:

    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

    st.success("Dataset Loaded Successfully")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        f"{df.shape[0]:,}"
    )

    c2.metric(
        "Columns",
        df.shape[1]
    )

    c3.metric(
        "Countries",
        df["country_txt"].nunique()
    )

    c4.metric(
        "Regions",
        df["region_txt"].nunique()
    )

except Exception:

    st.error("Unable to load dataset.")

st.divider()

st.subheader("📋 Current Configuration")

config = pd.DataFrame({
    "Setting": [
        "Theme",
        "Layout",
        "Chart Style",
        "Prediction Model",
        "Forecast Model",
        "Report Format",
        "Default Country"
    ],
    "Value": [
        theme,
        layout,
        chart_style,
        prediction_model,
        forecasting_model,
        report_format,
        default_country
    ]
})

st.dataframe(
    config,
    use_container_width=True,
    hide_index=True
)

st.divider()
st.subheader("💾 Dashboard Actions")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):

        st.success(
            "Settings saved successfully."
        )

        st.balloons()

with col2:

    if st.button(
        "🔄 Reset Settings",
        use_container_width=True
    ):

        st.warning(
            "Settings have been reset to default values."
        )

st.divider()

st.subheader("🖥️ System Status")

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Dashboard",
    "Online"
)

s2.metric(
    "Dataset",
    "Loaded"
)

s3.metric(
    "Prediction Model",
    "Ready"
)

s4.metric(
    "Forecast Engine",
    "Active"
)

st.divider()

st.subheader("📌 About Dashboard")

st.info(
    """
This AI-Based Military Intelligence Dashboard has been developed using:

• Streamlit for interactive web application development.

• Plotly for dynamic visualizations.

• Scikit-learn for machine learning models.

• Global Terrorism Database (GTD) for historical terrorism records.

The dashboard provides military intelligence analytics, attack prediction,
threat assessment, forecasting, country-wise analysis and interactive
data exploration for academic and research purposes.
"""
)

st.divider()

st.subheader("🚀 Dashboard Features")

left, right = st.columns(2)

with left:

    st.success("""
✔ Home Dashboard

✔ Global Threat Map

✔ Country Intelligence

✔ Attack Prediction

✔ Threat Level Prediction
""")

with right:

    st.success("""
✔ Forecasting

✔ AI Intelligence Report

✔ Data Explorer

✔ Dashboard Settings

✔ CSV Report Download
""")

st.divider()

st.caption(
    "🛡 AI-Based Military Intelligence Dashboard | Version 2.0 | Developed using Streamlit, Plotly & Machine Learning"
)