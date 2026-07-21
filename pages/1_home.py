import streamlit as st
import plotly.express as px
from utils.data_loader import (
    load_data,
    dashboard_stats,
    yearly_attacks,
    top_countries,
    top_groups,
    attack_distribution,
    calculate_threat
)

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

df = load_data()

stats = dashboard_stats(df)

country_data = top_countries(df)
group_data = top_groups(df)
attack_data = attack_distribution(df)
yearly = yearly_attacks(df)
threat = calculate_threat(df)

top_country = country_data.iloc[0]["Country"]
top_group = group_data.iloc[0]["Group"]
top_attack = attack_data.iloc[0]["Attack Type"]
top_weapon = df["weaptype1_txt"].value_counts().idxmax()

st.title("🛡 Military Intelligence Command Center")

st.markdown(
    """
    Analyze global terrorism trends using AI, Machine Learning and Interactive Visualizations.
    """
)

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{stats['incidents']:,}"
)

c2.metric(
    "Fatalities",
    f"{stats['fatalities']:,}"
)

c3.metric(
    "Injured",
    f"{stats['injured']:,}"
)

c4.metric(
    "Countries",
    f"{stats['countries']}"
)

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("📈 Terrorist Attacks Over Years")

    fig = px.line(
        yearly,
        x="iyear",
        y="Attacks",
        markers=True
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🌍 Top 10 High-Risk Countries")

    fig = px.bar(
        country_data,
        x="Incidents",
        y="Country",
        orientation="h",
        color="Incidents"
    )

    fig.update_layout(
        height=450,
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🎯 Attack Type Distribution")

    fig = px.pie(
        attack_data,
        names="Attack Type",
        values="Count",
        hole=0.45
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("👥 Top Terrorist Organizations")

    fig = px.bar(
        group_data,
        x="Attacks",
        y="Group",
        orientation="h",
        color="Attacks"
    )

    fig.update_layout(
        height=450,
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("📊 Attack Trend Snapshot")

    latest_year = yearly.iloc[-1]["iyear"]
    latest_attacks = yearly.iloc[-1]["Attacks"]

    first_year = yearly.iloc[0]["iyear"]
    first_attacks = yearly.iloc[0]["Attacks"]

    growth = (
        (latest_attacks - first_attacks)
        / max(first_attacks, 1)
    ) * 100

    st.metric(
        "Latest Recorded Year",
        int(latest_year)
    )

    st.metric(
        "Recorded Attacks",
        int(latest_attacks),
        f"{growth:.2f}% Overall Growth"
    )

with col2:

    st.subheader("🚨 Threat Level")

    if "LOW" in threat:
        st.success(threat)

    elif "MEDIUM" in threat:
        st.warning(threat)

    else:
        st.error(threat)

    st.metric(
        "Average Fatalities",
        f"{df['nkill'].mean():.2f}"
    )

st.divider()
st.subheader("🧠 AI Intelligence Summary")

summary = f"""
### Executive Summary

- 🌍 **Highest Risk Country:** **{top_country}**
- 👥 **Most Active Terrorist Organization:** **{top_group}**
- 🎯 **Most Common Attack Type:** **{top_attack}**
- 🔫 **Most Frequently Used Weapon:** **{top_weapon}**
- 🚨 **Current Threat Assessment:** **{threat}**

Based on historical GTD data, **{top_country}** has experienced the highest number of recorded terrorist incidents. The dominant attack method remains **{top_attack}**, while **{top_group}** appears most frequently among recorded organizations. Intelligence agencies should prioritize surveillance in high-risk regions and continue monitoring emerging attack patterns using predictive analytics.
"""

st.info(summary)

st.divider()

st.subheader("💡 Quick Intelligence Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
✔ Total Incidents Analysed : {stats['incidents']:,}

✔ Countries Covered : {stats['countries']}

✔ Fatalities Recorded : {stats['fatalities']:,}

✔ Injured Victims : {stats['injured']:,}
""")

with col2:

    st.warning(f"""
✔ Highest Risk Country : {top_country}

✔ Top Organization : {top_group}

✔ Common Attack : {top_attack}

✔ Common Weapon : {top_weapon}
""")

st.divider()

st.subheader("🚀 Available Dashboard Modules")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("""
🌍 Global Threat Map

Visualize terrorist incidents across the world.
""")

with c2:
    st.info("""
🤖 Attack Prediction

Predict possible attack types using Machine Learning.
""")

with c3:
    st.info("""
📈 Forecasting

Forecast future terrorism trends from historical data.
""")

with c4:
    st.info("""
🧠 AI Intelligence Report

Generate intelligence summaries and strategic insights.
""")

st.divider()

st.caption("AI Military Intelligence Dashboard • Version 2.0 • Internship Project")