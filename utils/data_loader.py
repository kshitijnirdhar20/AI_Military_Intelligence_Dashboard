import pandas as pd
import streamlit as st

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


def dashboard_stats(df):

    return {
        "incidents": len(df),
        "fatalities": int(df["nkill"].sum()),
        "injured": int(df["nwound"].sum()),
        "countries": df["country_txt"].nunique()
    }


def yearly_attacks(df):

    yearly = (
        df.groupby("iyear")
        .size()
        .reset_index(name="Attacks")
        .sort_values("iyear")
    )

    return yearly


def top_countries(df, n=10):

    country_data = (
        df["country_txt"]
        .value_counts()
        .head(n)
        .reset_index()
    )

    country_data.columns = [
        "Country",
        "Incidents"
    ]

    return country_data


def top_groups(df, n=10):

    group_data = (
        df["gname"]
        .value_counts()
        .head(n)
        .reset_index()
    )

    group_data.columns = [
        "Group",
        "Attacks"
    ]

    return group_data


def attack_distribution(df):

    attack_data = (
        df["attacktype1_txt"]
        .value_counts()
        .reset_index()
    )

    attack_data.columns = [
        "Attack Type",
        "Count"
    ]

    return attack_data


def top_weapons(df, n=10):

    weapon_data = (
        df["weaptype1_txt"]
        .value_counts()
        .head(n)
        .reset_index()
    )

    weapon_data.columns = [
        "Weapon",
        "Count"
    ]

    return weapon_data


def calculate_threat(df):

    avg = df["nkill"].mean()

    if avg < 2:
        return "🟢 LOW"

    elif avg < 5:
        return "🟡 MEDIUM"

    else:
        return "🔴 HIGH"