
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Terrorism Forecasting System")

st.markdown(
    """
Forecast future terrorist incidents using historical GTD records and Machine Learning.
"""
)

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

    return df

df = load_data()

st.sidebar.header("Forecast Settings")

countries = sorted(
    df["country_txt"].dropna().unique()
)

country = st.sidebar.selectbox(
    "Country",
    countries
)

forecast_years = st.sidebar.slider(
    "Forecast Years",
    1,
    10,
    5
)

country_df = df[
    df["country_txt"] == country
]

yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

yearly = yearly.sort_values(
    "iyear"
)

if len(yearly) < 5:

    st.warning(
        "Not enough historical data available for forecasting."
    )

    st.stop()

X = yearly[["iyear"]]

y = yearly["Attacks"]

model = LinearRegression()

model.fit(
    X,
    y
)

last_year = yearly["iyear"].max()

future_years = np.arange(
    last_year + 1,
    last_year + forecast_years + 1
)

future_df = pd.DataFrame({
    "iyear": future_years
})

predictions = model.predict(
    future_df
)

predictions = np.maximum(
    predictions,
    0
)

forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": predictions.astype(int)
})
st.divider()

st.subheader("📈 Historical vs Forecast Analysis")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=yearly["iyear"],
        y=yearly["Attacks"],
        mode="lines+markers",
        name="Historical Attacks"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast["Year"],
        y=forecast["Forecasted Attacks"],
        mode="lines+markers",
        name="Forecasted Attacks"
    )
)

fig.update_layout(
    height=600,
    xaxis_title="Year",
    yaxis_title="Number of Attacks",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("📊 Forecast Summary")

left, right = st.columns([2, 1])

with left:

    st.dataframe(
        forecast,
        use_container_width=True,
        height=300
    )

with right:

    current_attacks = int(
        yearly.iloc[-1]["Attacks"]
    )

    forecast_attacks = int(
        forecast.iloc[-1]["Forecasted Attacks"]
    )

    growth = (
        (forecast_attacks - current_attacks)
        / max(current_attacks, 1)
    ) * 100

    st.metric(
        "Current Attacks",
        current_attacks
    )

    st.metric(
        f"Forecast ({forecast_years} Years)",
        forecast_attacks
    )

    st.metric(
        "Growth",
        f"{growth:.2f}%"
    )

st.divider()

st.subheader("📌 Forecast Highlights")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Selected Country",
    country
)

c2.metric(
    "Historical Records",
    len(yearly)
)

c3.metric(
    "Forecast Years",
    forecast_years
)

c4.metric(
    "Latest Year",
    int(last_year)
)

st.divider()
if growth < 0:
    trend = "🟢 Decreasing"
    risk = "LOW"
elif growth < 15:
    trend = "🟡 Stable"
    risk = "MEDIUM"
else:
    trend = "🔴 Increasing"
    risk = "HIGH"

st.subheader("🧠 AI Forecast Intelligence")

st.info(f"""
### Executive Summary

Based on historical GTD records, the AI forecasting model predicts **{forecast_attacks}** terrorist incidents in **{country}** over the selected forecast period.

Current Recorded Attacks : **{current_attacks}**

Forecasted Attacks : **{forecast_attacks}**

Expected Growth : **{growth:.2f}%**

Threat Trend : **{trend}**

The forecast indicates an overall **{risk}** risk trend. These projections are generated using historical attack data and should be considered as decision-support information for intelligence planning.
""")

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🚨 Threat Trend Assessment")

    if risk == "LOW":
        st.success("🟢 Low Future Risk")

    elif risk == "MEDIUM":
        st.warning("🟡 Moderate Future Risk")

    else:
        st.error("🔴 High Future Risk")

    st.metric(
        "Growth Rate",
        f"{growth:.2f}%"
    )

    st.metric(
        "Forecast Trend",
        trend
    )

with right:

    st.subheader("📌 Strategic Recommendations")

    if risk == "LOW":

        st.success(f"""
✔ Continue routine monitoring

✔ Maintain intelligence sharing

✔ Protect critical infrastructure

✔ Review security policies periodically
""")

    elif risk == "MEDIUM":

        st.warning(f"""
✔ Increase surveillance operations

✔ Allocate additional intelligence resources

✔ Improve border and infrastructure security

✔ Monitor emerging attack patterns
""")

    else:

        st.error(f"""
✔ Immediate strategic planning recommended

✔ Increase military preparedness

✔ Deploy additional surveillance assets

✔ Enhance inter-agency intelligence coordination

✔ Strengthen protection of vulnerable targets
""")

st.divider()

st.subheader("📊 Operational Insights")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Threat Trend",
    trend
)

c2.metric(
    "Risk Level",
    risk
)

c3.metric(
    "Forecast Growth",
    f"{growth:.2f}%"
)

st.divider()
st.subheader("📄 Forecast Intelligence Report")

report = f"""
========================================

AI FORECAST INTELLIGENCE REPORT

========================================

Country : {country}

Forecast Period : {forecast_years} Years

Latest Historical Year : {int(last_year)}

Current Recorded Attacks : {current_attacks}

Forecasted Attacks : {forecast_attacks}

Expected Growth : {growth:.2f}%

Threat Trend : {trend}

Risk Level : {risk}

----------------------------------------

AI Executive Summary

The forecasting model predicts approximately {forecast_attacks} terrorist incidents in {country} over the selected forecast period.

Historical analysis indicates a {trend} trend with an estimated growth rate of {growth:.2f}%.

----------------------------------------

Strategic Recommendations

• Continue monitoring historical attack patterns.

• Strengthen intelligence sharing among agencies.

• Enhance protection of high-risk regions.

• Allocate resources based on forecast trends.

• Periodically retrain forecasting models using updated GTD data.

----------------------------------------

Generated By

AI Military Intelligence Dashboard
Forecasting Module Version 2.0
"""

st.download_button(
    "📥 Download Forecast Report",
    report,
    file_name=f"{country}_Forecast_Report.txt",
    mime="text/plain"
)

st.divider()

st.subheader("✅ AI Decision Support")

if risk == "LOW":

    st.success(
        "The forecast indicates a decreasing threat trend. Continue preventive monitoring while maintaining existing security measures."
    )

elif risk == "MEDIUM":

    st.warning(
        "The forecast indicates a stable threat trend. Strengthen surveillance and regularly review intelligence reports."
    )

else:

    st.error(
        "The forecast indicates an increasing threat trend. Immediate strategic planning and enhanced security operations are recommended."
    )

st.divider()

st.subheader("📌 Forecast Insights")

left, right = st.columns(2)

with left:

    st.info(f"""
**Key Findings**

• Country Analyzed: **{country}**

• Forecast Duration: **{forecast_years} Years**

• Historical Records Used: **{len(yearly)} Years**

• Forecasted Incidents: **{forecast_attacks}**
""")

with right:

    st.info(f"""
**Operational Assessment**

• Threat Trend: **{trend}**

• Risk Level: **{risk}**

• Expected Growth: **{growth:.2f}%**

• AI Model: **Linear Regression**
""")

st.divider()

st.caption(
    "AI Military Intelligence Dashboard • Forecasting & Predictive Analytics • Version 2.0"
)