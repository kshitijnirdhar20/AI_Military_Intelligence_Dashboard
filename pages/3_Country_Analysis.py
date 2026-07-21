import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(
    page_title="Country Intelligence",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 Country Intelligence Analysis")

st.markdown(
    "Analyze terrorism incidents, trends and intelligence for a selected country."
)

df = load_data()

countries = sorted(df["country_txt"].dropna().unique())

country = st.sidebar.selectbox(
    "Select Country",
    countries
)

country_df = df[df["country_txt"] == country]

st.subheader(f"Military Intelligence Report : {country}")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{len(country_df):,}"
)

c2.metric(
    "Fatalities",
    f"{int(country_df['nkill'].sum()):,}"
)

c3.metric(
    "Injured",
    f"{int(country_df['nwound'].sum()):,}"
)

c4.metric(
    "Organizations",
    country_df["gname"].nunique()
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "Cities",
    country_df["city"].nunique()
)

c6.metric(
    "Attack Types",
    country_df["attacktype1_txt"].nunique()
)

c7.metric(
    "Weapon Types",
    country_df["weaptype1_txt"].nunique()
)

success_rate = (
    country_df["success"].mean() * 100
)

c8.metric(
    "Successful Attacks",
    f"{success_rate:.1f}%"
)

st.divider()

yearly = (
    country_df
    .groupby("iyear")
    .size()
    .reset_index(name="Attacks")
)

attack_chart = (
    country_df
    .groupby("attacktype1_txt")
    .size()
    .reset_index(name="Count")
)

weapon_chart = (
    country_df
    .groupby("weaptype1_txt")
    .size()
    .reset_index(name="Count")
)

group_chart = (
    country_df
    .groupby("gname")
    .size()
    .reset_index(name="Attacks")
    .sort_values(
        "Attacks",
        ascending=False
    )
    .head(10)
)

city_chart = (
    country_df
    .groupby("city")
    .size()
    .reset_index(name="Incidents")
    .sort_values(
        "Incidents",
        ascending=False
    )
    .head(10)
)
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

    st.subheader("🎯 Attack Type Distribution")

    fig = px.pie(
        attack_chart,
        names="attacktype1_txt",
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

left, right = st.columns(2)

with left:

    st.subheader("👥 Top Terrorist Organizations")

    fig = px.bar(
        group_chart,
        x="Attacks",
        y="gname",
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

with right:

    st.subheader("🔫 Weapon Type Analysis")

    fig = px.bar(
        weapon_chart,
        x="weaptype1_txt",
        y="Count",
        color="Count"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Weapon Type",
        yaxis_title="Incidents"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🏙 Top 10 Affected Cities")

    fig = px.bar(
        city_chart,
        x="Incidents",
        y="city",
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

    st.subheader("📊 Attack Trend Statistics")

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
        f"{growth:.2f}% Growth"
    )

st.divider()
map_df = country_df.dropna(
    subset=["latitude", "longitude"]
)

st.subheader("🗺 Incident Locations")

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="city",
    hover_data={
        "iyear": True,
        "gname": True,
        "attacktype1_txt": True,
        "nkill": True,
        "nwound": True,
        "latitude": False,
        "longitude": False
    },
    projection="natural earth",
    height=650
)

fig.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=40,
        b=0
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

top_city = (
    city_chart.iloc[0]["city"]
    if not city_chart.empty else "N/A"
)

top_group = (
    group_chart.iloc[0]["gname"]
    if not group_chart.empty else "N/A"
)

top_attack = (
    attack_chart.sort_values(
        "Count",
        ascending=False
    ).iloc[0]["attacktype1_txt"]
    if not attack_chart.empty else "N/A"
)

top_weapon = (
    weapon_chart.sort_values(
        "Count",
        ascending=False
    ).iloc[0]["weaptype1_txt"]
    if not weapon_chart.empty else "N/A"
)

avg_fatalities = country_df["nkill"].mean()

if avg_fatalities < 2:
    threat = "🟢 LOW"
    risk_score = 30
elif avg_fatalities < 5:
    threat = "🟡 MEDIUM"
    risk_score = 65
else:
    threat = "🔴 HIGH"
    risk_score = 95

left, right = st.columns([2,1])

with left:

    st.subheader("🧠 AI Intelligence Summary")

    st.info(f"""
### Executive Summary

Country : **{country}**

🏙 Highest Risk City : **{top_city}**

👥 Most Active Organization : **{top_group}**

🎯 Most Common Attack : **{top_attack}**

🔫 Most Common Weapon : **{top_weapon}**

🚨 Threat Level : **{threat}**

The intelligence analysis indicates that **{top_city}** has experienced the highest concentration of terrorist incidents within **{country}**. Historical records show that **{top_attack}** remains the dominant attack method while **{top_group}** appears most frequently among recorded organizations. Continued surveillance and intelligence sharing are recommended to strengthen national security.
""")

with right:

    st.subheader("🚨 Country Risk Score")

    st.metric(
        "Risk Score",
        f"{risk_score}/100"
    )

    if risk_score < 40:
        st.success("Low Risk")

    elif risk_score < 70:
        st.warning("Medium Risk")

    else:
        st.error("High Risk")

    st.metric(
        "Average Fatalities",
        f"{avg_fatalities:.2f}"
    )

st.divider()

st.subheader("📌 Strategic Recommendations")

st.success(f"""
✔ Increase surveillance across **{top_city}**

✔ Monitor activities linked to **{top_group}**

✔ Strengthen protection against **{top_attack}** attacks

✔ Improve emergency response and intelligence sharing

✔ Continue predictive threat monitoring using AI models
""")

st.divider()
st.subheader("📋 Incident Details")

search = st.text_input(
    "🔍 Search by City or Terrorist Organization"
)

display_df = country_df.copy()

if search:

    display_df = display_df[
        display_df["city"].fillna("").str.contains(
            search,
            case=False
        )
        |
        display_df["gname"].fillna("").str.contains(
            search,
            case=False
        )
    ]

columns = [
    "iyear",
    "city",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "nkill",
    "nwound"
]

st.dataframe(
    display_df[columns],
    use_container_width=True,
    height=450
)

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("📊 Dataset Statistics")

    st.write(f"**Total Records:** {len(display_df):,}")

    st.write(f"**Cities Covered:** {display_df['city'].nunique()}")

    st.write(f"**Organizations:** {display_df['gname'].nunique()}")

    st.write(f"**Attack Types:** {display_df['attacktype1_txt'].nunique()}")

    st.write(f"**Weapon Types:** {display_df['weaptype1_txt'].nunique()}")

with right:

    st.subheader("📥 Export Intelligence Data")

    csv = display_df.to_csv(
        index=False
    ).encode()

    st.download_button(
        "Download Country Report",
        csv,
        file_name=f"{country}_Intelligence_Report.csv",
        mime="text/csv"
    )

st.divider()

st.success("✅ Intelligence analysis completed successfully.")

st.caption(
    "AI Military Intelligence Dashboard • Country Intelligence Analysis • Version 2.0"
)