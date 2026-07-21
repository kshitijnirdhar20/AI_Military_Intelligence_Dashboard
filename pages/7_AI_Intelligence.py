import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Intelligence Report",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Intelligence Report")

st.markdown("""
Generate an AI-assisted intelligence assessment using the Global Terrorism Database (GTD).
""")

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    return df

df = load_data()

st.sidebar.header("Report Filters")

years = sorted(df["iyear"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + list(years)
)

if selected_year != "All":

    df = df[
        df["iyear"] == selected_year
    ]

total_incidents = len(df)

total_killed = int(
    df["nkill"].sum()
)

total_wounded = int(
    df["nwound"].sum()
)

countries = df["country_txt"].nunique()

groups = df["gname"].nunique()

avg_killed = df["nkill"].mean()

top_countries = (
    df["country_txt"]
    .value_counts()
    .head(10)
)

top_groups = (
    df["gname"]
    .value_counts()
    .head(10)
)

attack_types = (
    df["attacktype1_txt"]
    .value_counts()
)

weapon_types = (
    df["weaptype1_txt"]
    .value_counts()
)

if avg_killed < 2:

    threat = "🟢 LOW"

elif avg_killed < 5:

    threat = "🟡 MEDIUM"

else:

    threat = "🔴 HIGH"

st.subheader("📊 Key Intelligence Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{total_incidents:,}"
)

c2.metric(
    "Fatalities",
    f"{total_killed:,}"
)

c3.metric(
    "Injuries",
    f"{total_wounded:,}"
)

c4.metric(
    "Threat Level",
    threat
)

st.divider()
st.subheader("🧠 Executive Intelligence Summary")

summary = f"""
### Executive Summary

During the selected period, **{total_incidents:,}** terrorist incidents were recorded across **{countries}** countries.

These incidents resulted in **{total_killed:,}** fatalities and **{total_wounded:,}** injuries.

The overall threat level is assessed as **{threat}**.

The highest number of incidents was recorded in **{top_countries.index[0]}**.

The most active terrorist organization was **{top_groups.index[0]}**.

The most common attack type was **{attack_types.index[0]}**.

The most frequently used weapon was **{weapon_types.index[0]}**.
"""

st.info(summary)

st.divider()

st.subheader("📈 Intelligence Visual Analytics")

left, right = st.columns(2)

with left:

    st.subheader("🌍 Top 10 High-Risk Countries")

    country_chart = (
        top_countries
        .reset_index()
    )

    country_chart.columns = [
        "Country",
        "Incidents"
    ]

    fig = px.bar(
        country_chart,
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

with right:

    st.subheader("👥 Top Terrorist Organizations")

    group_chart = (
        top_groups
        .reset_index()
    )

    group_chart.columns = [
        "Group",
        "Attacks"
    ]

    fig = px.bar(
        group_chart,
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

left, right = st.columns(2)

with left:

    st.subheader("🎯 Attack Type Distribution")

    attack_chart = (
        attack_types
        .reset_index()
    )

    attack_chart.columns = [
        "Attack Type",
        "Count"
    ]

    fig = px.pie(
        attack_chart,
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

    st.subheader("🔫 Top Weapon Types")

    weapon_chart = (
        weapon_types
        .head(10)
        .reset_index()
    )

    weapon_chart.columns = [
        "Weapon",
        "Count"
    ]

    fig = px.bar(
        weapon_chart,
        x="Weapon",
        y="Count",
        color="Count"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
st.subheader("🚨 AI Threat Assessment")

if "LOW" in threat:
    st.success(f"Overall Threat Assessment : {threat}")
elif "MEDIUM" in threat:
    st.warning(f"Overall Threat Assessment : {threat}")
else:
    st.error(f"Overall Threat Assessment : {threat}")

st.write(
    f"""
The historical GTD records indicate an average of **{avg_killed:.2f} fatalities**
per recorded incident.

The country with the highest number of incidents is **{top_countries.index[0]}**,
while **{top_groups.index[0]}** remains the most frequently recorded terrorist organization.

The dominant attack method is **{attack_types.index[0]}**, with
**{weapon_types.index[0]}** being the most commonly used weapon type.
"""
)

st.divider()

st.subheader("🛡 Strategic Intelligence Recommendations")

recommendations = [
    f"Increase surveillance and intelligence gathering in {top_countries.index[0]}.",
    f"Monitor activities associated with {top_groups.index[0]}.",
    "Strengthen protection of high-risk public infrastructure.",
    "Enhance border security and intelligence sharing between agencies.",
    "Deploy AI-based predictive analytics for early threat identification.",
    "Increase monitoring of explosive and firearm related attacks."
]

for i, rec in enumerate(recommendations, start=1):
    st.success(f"{i}. {rec}")

st.divider()

st.subheader("📌 Intelligence Insights")

col1, col2 = st.columns(2)

with col1:

    st.info(f"""
### Operational Overview

• Total Incidents : {total_incidents:,}

• Countries Covered : {countries}

• Terrorist Organizations : {groups}

• Fatalities : {total_killed:,}

• Injuries : {total_wounded:,}
""")

with col2:

    st.warning(f"""
### Key Intelligence Findings

• Highest Risk Country : {top_countries.index[0]}

• Most Active Organization : {top_groups.index[0]}

• Most Common Attack : {attack_types.index[0]}

• Most Common Weapon : {weapon_types.index[0]}

• Current Threat : {threat}
""")

st.divider()

st.subheader("🎯 Executive Risk Indicators")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average Fatalities",
    f"{avg_killed:.2f}"
)

c2.metric(
    "Highest Risk Country",
    top_countries.index[0]
)

c3.metric(
    "Threat Level",
    threat
)

st.divider()
st.subheader("📄 Download Intelligence Report")

report = f"""
====================================================
          AI MILITARY INTELLIGENCE REPORT
====================================================

REPORT SUMMARY
-------------------------------
Year Selected        : {selected_year}
Total Incidents      : {total_incidents:,}
Countries Covered    : {countries}
Terrorist Groups     : {groups}

CASUALTY ANALYSIS
-------------------------------
Fatalities           : {total_killed:,}
Injuries             : {total_wounded:,}
Average Fatalities   : {avg_killed:.2f}

THREAT ASSESSMENT
-------------------------------
Overall Threat Level : {threat}

Highest Risk Country : {top_countries.index[0]}
Top Terrorist Group  : {top_groups.index[0]}
Common Attack Type   : {attack_types.index[0]}
Common Weapon Type   : {weapon_types.index[0]}

STRATEGIC RECOMMENDATIONS
-------------------------------
1. Increase surveillance in high-risk regions.
2. Strengthen intelligence sharing among agencies.
3. Enhance protection of critical infrastructure.
4. Improve monitoring of terrorist organizations.
5. Expand AI-driven predictive threat analysis.
6. Continue long-term trend monitoring.

====================================================
End of Report
====================================================
"""

st.download_button(
    label="📥 Download Intelligence Report",
    data=report,
    file_name="AI_Intelligence_Report.txt",
    mime="text/plain"
)

st.divider()

st.subheader("✅ Report Status")

status1, status2, status3 = st.columns(3)

status1.success("✔ Dataset Analysed")

status2.success("✔ Intelligence Generated")

status3.success("✔ Report Ready for Download")

st.divider()

st.subheader("ℹ️ Intelligence Note")

st.info(
    """
This report is generated using historical records from the Global Terrorism Database (GTD).
The insights are intended for academic analysis and decision-support purposes only.
Predictions and recommendations are based on historical trends and machine learning models,
and should not be considered real-time intelligence.
"""
)

st.divider()

st.caption(
    "AI-Based Military Intelligence Dashboard • Version 2.0 • Internship Project"
)