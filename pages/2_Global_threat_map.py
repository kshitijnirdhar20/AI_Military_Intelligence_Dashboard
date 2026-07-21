import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Global Threat Map",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Threat Intelligence Map")

st.markdown(
    "Analyze global terrorist incidents using interactive maps and advanced filters."
)

df = load_data()

st.sidebar.header("Filters")

years = sorted(df["iyear"].unique())
countries = sorted(df["country_txt"].dropna().unique())
regions = sorted(df["region_txt"].dropna().unique())
attacks = sorted(df["attacktype1_txt"].dropna().unique())

year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + regions
)

attack = st.sidebar.selectbox(
    "Attack Type",
    ["All"] + attacks
)

filtered = df.copy()

if year != "All":
    filtered = filtered[
        filtered["iyear"] == year
    ]

if country != "All":
    filtered = filtered[
        filtered["country_txt"] == country
    ]

if region != "All":
    filtered = filtered[
        filtered["region_txt"] == region
    ]

if attack != "All":
    filtered = filtered[
        filtered["attacktype1_txt"] == attack
    ]

filtered = filtered.dropna(
    subset=["latitude", "longitude"]
)

st.subheader("Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    len(filtered)
)

c2.metric(
    "Fatalities",
    int(filtered["nkill"].sum())
)

c3.metric(
    "Injured",
    int(filtered["nwound"].sum())
)

c4.metric(
    "Countries",
    filtered["country_txt"].nunique()
)

st.divider()
st.subheader("🌍 Global Incident Map")

fig = px.scatter_geo(
    filtered,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data={
        "city": True,
        "iyear": True,
        "attacktype1_txt": True,
        "gname": True,
        "nkill": True,
        "nwound": True,
        "latitude": False,
        "longitude": False
    },
    projection="natural earth",
    height=650
)

fig.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    legend_title="Attack Type"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🌍 Top 10 Most Affected Countries")

    country_chart = (
        filtered["country_txt"]
        .value_counts()
        .head(10)
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

    st.subheader("🎯 Attack Type Distribution")

    attack_chart = (
        filtered["attacktype1_txt"]
        .value_counts()
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

st.divider()
top_country = (
    filtered["country_txt"]
    .value_counts()
    .idxmax()
    if not filtered.empty else "N/A"
)

top_group = (
    filtered["gname"]
    .value_counts()
    .idxmax()
    if not filtered.empty else "N/A"
)

top_attack = (
    filtered["attacktype1_txt"]
    .value_counts()
    .idxmax()
    if not filtered.empty else "N/A"
)

top_weapon = (
    filtered["weaptype1_txt"]
    .value_counts()
    .idxmax()
    if not filtered.empty else "N/A"
)

avg_fatalities = filtered["nkill"].mean()

if avg_fatalities < 2:
    threat = "🟢 LOW"
elif avg_fatalities < 5:
    threat = "🟡 MEDIUM"
else:
    threat = "🔴 HIGH"

st.subheader("🧠 AI Threat Intelligence Summary")

st.info(f"""
### Executive Summary

🌍 Highest Risk Country: **{top_country}**

👥 Most Active Organization: **{top_group}**

🎯 Most Common Attack: **{top_attack}**

🔫 Most Common Weapon: **{top_weapon}**

🚨 Overall Threat Level: **{threat}**

The filtered dataset indicates that **{top_country}** remains the most affected region. Intelligence suggests prioritizing surveillance in vulnerable areas, strengthening inter-agency coordination, and continuously monitoring attack trends using predictive analytics.
""")

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("📌 Intelligence Highlights")

    st.success(f"""
✔ Total Incidents : {len(filtered):,}

✔ Countries Covered : {filtered['country_txt'].nunique()}

✔ Fatalities : {int(filtered['nkill'].sum()):,}

✔ Injured : {int(filtered['nwound'].sum()):,}
""")

with right:

    st.subheader("🚨 Threat Assessment")

    if "LOW" in threat:
        st.success(threat)

    elif "MEDIUM" in threat:
        st.warning(threat)

    else:
        st.error(threat)

    st.metric(
        "Average Fatalities",
        f"{avg_fatalities:.2f}"
    )

st.divider()

csv = filtered.to_csv(index=False).encode()

st.download_button(
    "📥 Download Filtered Intelligence Data",
    csv,
    file_name="Filtered_Global_Threat_Data.csv",
    mime="text/csv"
)

st.divider()

st.caption("AI Military Intelligence Dashboard • Global Threat Map • Version 2.0")