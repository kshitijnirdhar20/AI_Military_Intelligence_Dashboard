import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Explorer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Global Terrorism Data Explorer")

st.markdown("""
Explore, filter, analyze and download the Global Terrorism Database.
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

st.sidebar.header("Dataset Filters")

years = sorted(df["iyear"].dropna().unique())

selected_year = st.sidebar.multiselect(
    "Year",
    years
)

countries = sorted(df["country_txt"].dropna().unique())

selected_country = st.sidebar.multiselect(
    "Country",
    countries
)

regions = sorted(df["region_txt"].dropna().unique())

selected_region = st.sidebar.multiselect(
    "Region",
    regions
)

attack_types = sorted(df["attacktype1_txt"].dropna().unique())

selected_attack = st.sidebar.multiselect(
    "Attack Type",
    attack_types
)

weapon_types = sorted(df["weaptype1_txt"].dropna().unique())

selected_weapon = st.sidebar.multiselect(
    "Weapon Type",
    weapon_types
)

groups = sorted(df["gname"].dropna().unique())

selected_group = st.sidebar.multiselect(
    "Terrorist Group",
    groups
)

filtered_df = df.copy()

if selected_year:
    filtered_df = filtered_df[
        filtered_df["iyear"].isin(selected_year)
    ]

if selected_country:
    filtered_df = filtered_df[
        filtered_df["country_txt"].isin(selected_country)
    ]

if selected_region:
    filtered_df = filtered_df[
        filtered_df["region_txt"].isin(selected_region)
    ]

if selected_attack:
    filtered_df = filtered_df[
        filtered_df["attacktype1_txt"].isin(selected_attack)
    ]

if selected_weapon:
    filtered_df = filtered_df[
        filtered_df["weaptype1_txt"].isin(selected_weapon)
    ]

if selected_group:
    filtered_df = filtered_df[
        filtered_df["gname"].isin(selected_group)
    ]

search = st.text_input(
    "🔍 Search by City or Country"
)

if search:

    filtered_df = filtered_df[
        filtered_df["city"].fillna("").str.contains(
            search,
            case=False
        )
        |
        filtered_df["country_txt"].fillna("").str.contains(
            search,
            case=False
        )
    ]

st.divider()
st.subheader("📊 Dataset Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Incidents",
    f"{len(filtered_df):,}"
)

c2.metric(
    "Countries",
    filtered_df["country_txt"].nunique()
)

c3.metric(
    "Fatalities",
    f"{int(filtered_df['nkill'].sum()):,}"
)

c4.metric(
    "Injuries",
    f"{int(filtered_df['nwound'].sum()):,}"
)

st.divider()

st.subheader("📈 Quick Statistics")

left, right = st.columns(2)

with left:

    st.success(f"""
**Records Available**

• Incidents : {len(filtered_df):,}

• Countries : {filtered_df['country_txt'].nunique()}

• Regions : {filtered_df['region_txt'].nunique()}

• Terrorist Groups : {filtered_df['gname'].nunique()}
""")

with right:

    st.info(f"""
**Casualty Summary**

• Fatalities : {int(filtered_df['nkill'].sum()):,}

• Injuries : {int(filtered_df['nwound'].sum()):,}

• Average Fatalities : {filtered_df['nkill'].mean():.2f}

• Average Injuries : {filtered_df['nwound'].mean():.2f}
""")

st.divider()

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    file_name="Filtered_GTD_Data.csv",
    mime="text/csv"
)

st.divider()
st.subheader("📈 Visual Analytics")

tab1, tab2, tab3 = st.tabs([
    "🌍 Countries",
    "🎯 Attack Types",
    "🔫 Weapon Types"
])

with tab1:

    country_chart = (
        filtered_df["country_txt"]
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
        color="Incidents",
        title="Top 10 Countries by Incidents"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    attack_chart = (
        filtered_df["attacktype1_txt"]
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
        hole=0.45,
        title="Attack Type Distribution"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab3:

    weapon_chart = (
        filtered_df["weaptype1_txt"]
        .value_counts()
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
        color="Count",
        title="Top Weapon Types"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("🌍 Global Incident Map")

map_df = filtered_df.dropna(
    subset=["latitude", "longitude"]
)

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data={
        "city": True,
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
st.subheader("📊 Missing Values Analysis")

missing = (
    filtered_df.isnull()
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

missing.columns = [
    "Column",
    "Missing Values"
]

st.dataframe(
    missing,
    use_container_width=True,
    height=450
)

st.divider()

st.subheader("📑 Dataset Information")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Rows",
    filtered_df.shape[0]
)

col2.metric(
    "Columns",
    filtered_df.shape[1]
)

memory = round(
    filtered_df.memory_usage(deep=True).sum() / 1024**2,
    2
)

col3.metric(
    "Memory Usage (MB)",
    memory
)

st.divider()

st.subheader("📋 Column Information")

info_df = pd.DataFrame({

    "Column Name": filtered_df.columns,

    "Data Type": filtered_df.dtypes.astype(str).values,

    "Missing Values": filtered_df.isnull().sum().values,

    "Unique Values": [
        filtered_df[col].nunique()
        for col in filtered_df.columns
    ]

})

st.dataframe(
    info_df,
    use_container_width=True,
    height=500
)

st.divider()

st.subheader("📌 Data Quality Summary")

left, right = st.columns(2)

with left:

    st.success(f"""
### Dataset Overview

✔ Total Records : {filtered_df.shape[0]:,}

✔ Total Columns : {filtered_df.shape[1]}

✔ Countries : {filtered_df['country_txt'].nunique()}

✔ Terrorist Groups : {filtered_df['gname'].nunique()}
""")

with right:

    st.info(f"""
### Casualty Overview

✔ Fatalities : {int(filtered_df['nkill'].sum()):,}

✔ Injuries : {int(filtered_df['nwound'].sum()):,}

✔ Average Fatalities : {filtered_df['nkill'].mean():.2f}

✔ Average Injuries : {filtered_df['nwound'].mean():.2f}
""")

st.divider()

st.caption(
    "AI-Based Military Intelligence Dashboard • Data Explorer • Version 2.0"
)