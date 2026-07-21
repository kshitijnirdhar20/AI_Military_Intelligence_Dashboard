import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Attack Prediction",
    page_icon="🤖",
    layout="wide"
)

model = joblib.load(
    "models/attack_prediction_model.pkl"
)

encoders = joblib.load(
    "models/feature_encoders.pkl"
)

target_encoder = joblib.load(
    "models/target_encoder.pkl"
)

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/globalterrorism.csv",
        encoding="latin1",
        low_memory=False
    )

    df = df.dropna(
        subset=[
            "country_txt",
            "region_txt",
            "weaptype1_txt",
            "targtype1_txt",
            "gname"
        ]
    )

    return df

df = load_data()

st.title("🤖 AI Attack Type Prediction")

st.markdown("""
Predict the most probable terrorist attack type using Machine Learning.
""")

st.divider()

st.subheader("📋 Incident Information")

with st.form("prediction_form"):

    left, right = st.columns(2)

    with left:

        country = st.selectbox(
            "🌍 Country",
            sorted(df["country_txt"].unique())
        )

        region = st.selectbox(
            "🌎 Region",
            sorted(df["region_txt"].unique())
        )

        weapon = st.selectbox(
            "🔫 Weapon Type",
            sorted(df["weaptype1_txt"].unique())
        )

        target = st.selectbox(
            "🎯 Target Type",
            sorted(df["targtype1_txt"].unique())
        )

    with right:

        group = st.selectbox(
            "👥 Terrorist Organization",
            sorted(df["gname"].unique())
        )

        success = st.selectbox(
            "Attack Successful",
            [0,1],
            format_func=lambda x: "Yes" if x else "No"
        )

        suicide = st.selectbox(
            "Suicide Attack",
            [0,1],
            format_func=lambda x: "Yes" if x else "No"
        )

        nkill = st.number_input(
            "Fatalities",
            min_value=0,
            value=0
        )

        nwound = st.number_input(
            "Injured",
            min_value=0,
            value=0
        )

    submitted = st.form_submit_button(
        "🚀 Predict Attack Type"
    )
if submitted:

    country_encoded = encoders["country_txt"].transform([country])[0]

    region_encoded = encoders["region_txt"].transform([region])[0]

    weapon_encoded = encoders["weaptype1_txt"].transform([weapon])[0]

    target_encoded = encoders["targtype1_txt"].transform([target])[0]

    group_encoded = encoders["gname"].transform([group])[0]

    input_df = pd.DataFrame({

        "country_txt": [country_encoded],

        "region_txt": [region_encoded],

        "weaptype1_txt": [weapon_encoded],

        "targtype1_txt": [target_encoded],

        "gname": [group_encoded],

        "success": [success],

        "suicide": [suicide],

        "nkill": [nkill],

        "nwound": [nwound]

    })

    prediction = model.predict(input_df)

    probabilities = model.predict_proba(input_df)

    attack_type = target_encoder.inverse_transform(prediction)[0]

    confidence = probabilities.max() * 100

    st.divider()

    st.subheader("🎯 Prediction Result")

    left, right = st.columns(2)

    with left:

        st.success(f"### {attack_type}")

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

    with right:

        probability_df = pd.DataFrame({

            "Attack Type": target_encoder.classes_,

            "Probability": probabilities[0] * 100

        })

        probability_df = probability_df.sort_values(
            "Probability",
            ascending=False
        )

        st.subheader("📈 Prediction Probability")

        st.bar_chart(
            probability_df.set_index("Attack Type")
        )

    st.divider()

    st.subheader("📋 Incident Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Country",
        country
    )

    c2.metric(
        "Weapon",
        weapon
    )

    c3.metric(
        "Fatalities",
        nkill
    )

    c4.metric(
        "Injured",
        nwound
    )

    if confidence >= 80:

        risk = "🟢 LOW"

    elif confidence >= 60:

        risk = "🟡 MEDIUM"

    else:

        risk = "🔴 HIGH"

    st.divider()
    st.subheader("🧠 AI Intelligence Assessment")

    st.info(f"""
### Executive Summary

The AI model predicts that the most probable attack type is **{attack_type}**.

**Prediction Confidence:** {confidence:.2f}%

**Country:** {country}

**Region:** {region}

**Weapon Type:** {weapon}

**Target Type:** {target}

**Terrorist Organization:** {group}

This prediction is generated using historical patterns from the Global Terrorism Database (GTD). It should be used for academic analysis and decision support rather than as a definitive operational prediction.
""")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🚨 Risk Assessment")

        if confidence >= 80:
            st.success(risk)
        elif confidence >= 60:
            st.warning(risk)
        else:
            st.error(risk)

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

    with right:

        st.subheader("📌 Strategic Recommendations")

        st.success(f"""
✔ Increase surveillance in **{country}**

✔ Strengthen protection for **{target}**

✔ Monitor activities related to **{group}**

✔ Improve preparedness against **{weapon}** attacks

✔ Continue AI-assisted intelligence monitoring
""")

    st.divider()

    st.subheader("📄 Prediction Report")

    report = f"""
=========================================
AI ATTACK PREDICTION REPORT
=========================================

Country                : {country}
Region                 : {region}
Organization           : {group}
Weapon Type            : {weapon}
Target Type            : {target}

Fatalities             : {nkill}
Injuries               : {nwound}

Predicted Attack Type  : {attack_type}

Prediction Confidence  : {confidence:.2f}%

Risk Level             : {risk}

Recommendation:
Increase surveillance and continue intelligence
monitoring based on the predicted attack profile.

Generated by:
AI Military Intelligence Dashboard
"""

    st.download_button(
        "📥 Download Prediction Report",
        report,
        file_name="Attack_Prediction_Report.txt",
        mime="text/plain"
    )

    st.divider()

    st.caption(
        "🛡 AI Military Intelligence Dashboard • Attack Prediction Module • Version 2.0"
    )