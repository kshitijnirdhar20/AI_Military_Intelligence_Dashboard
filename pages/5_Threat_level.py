import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="Threat Level Prediction",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 AI Threat Level Prediction System")

st.markdown(
    """
Predict the severity of a terrorist incident using Machine Learning and historical GTD records.
"""
)

df = pd.read_csv(
    "data/globalterrorism.csv",
    encoding="latin1",
    low_memory=False
)

df = df[[
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt",
    "nkill",
    "nwound"
]]

df = df.dropna()

df["impact"] = df["nkill"] + df["nwound"]

def classify_threat(x):

    if x <= 2:
        return "LOW"

    elif x <= 10:
        return "MEDIUM"

    return "HIGH"

df["threat_level"] = df["impact"].apply(classify_threat)

encoders = {}

for col in [
    "country_txt",
    "region_txt",
    "attacktype1_txt",
    "weaptype1_txt",
    "targtype1_txt"
]:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder

target_encoder = LabelEncoder()

df["threat_level"] = target_encoder.fit_transform(
    df["threat_level"]
)

X = df.drop(
    columns=[
        "impact",
        "threat_level"
    ]
)

y = df["threat_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

st.divider()

st.subheader("📋 Incident Information")

with st.form("threat_form"):

    left, right = st.columns(2)

    with left:

        country = st.selectbox(
            "Country",
            sorted(encoders["country_txt"].classes_)
        )

        region = st.selectbox(
            "Region",
            sorted(encoders["region_txt"].classes_)
        )

        attack = st.selectbox(
            "Attack Type",
            sorted(encoders["attacktype1_txt"].classes_)
        )

    with right:

        weapon = st.selectbox(
            "Weapon Type",
            sorted(encoders["weaptype1_txt"].classes_)
        )

        target = st.selectbox(
            "Target Type",
            sorted(encoders["targtype1_txt"].classes_)
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
        "🚨 Predict Threat Level"
    )
if submitted:

    country_encoded = encoders["country_txt"].transform([country])[0]
    region_encoded = encoders["region_txt"].transform([region])[0]
    attack_encoded = encoders["attacktype1_txt"].transform([attack])[0]
    weapon_encoded = encoders["weaptype1_txt"].transform([weapon])[0]
    target_encoded = encoders["targtype1_txt"].transform([target])[0]

    input_data = pd.DataFrame({
        "country_txt": [country_encoded],
        "region_txt": [region_encoded],
        "attacktype1_txt": [attack_encoded],
        "weaptype1_txt": [weapon_encoded],
        "targtype1_txt": [target_encoded],
        "nkill": [nkill],
        "nwound": [nwound]
    })

    prediction = model.predict(input_data)

    probabilities = model.predict_proba(input_data)

    threat_level = target_encoder.inverse_transform(prediction)[0]

    confidence = probabilities.max() * 100

    st.divider()

    st.subheader("🚨 Prediction Result")

    left, right = st.columns(2)

    with left:

        if threat_level == "LOW":
            st.success(f"### Threat Level\n\n🟢 **{threat_level}**")

        elif threat_level == "MEDIUM":
            st.warning(f"### Threat Level\n\n🟡 **{threat_level}**")

        else:
            st.error(f"### Threat Level\n\n🔴 **{threat_level}**")

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

    with right:

        st.subheader("📈 Probability Distribution")

        probability_df = pd.DataFrame({
            "Threat Level": target_encoder.classes_,
            "Probability (%)": probabilities[0] * 100
        })

        probability_df = probability_df.sort_values(
            "Probability (%)",
            ascending=False
        )

        st.bar_chart(
            probability_df.set_index("Threat Level")
        )

    st.divider()

    st.subheader("📊 Prediction Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Country",
        country
    )

    c2.metric(
        "Attack Type",
        attack
    )

    c3.metric(
        "Fatalities",
        nkill
    )

    c4.metric(
        "Injured",
        nwound
    )

    st.divider()
    if threat_level == "LOW":
        risk_score = 30
    elif threat_level == "MEDIUM":
        risk_score = 65
    else:
        risk_score = 95

    st.subheader("🧠 AI Intelligence Assessment")

    st.info(f"""
### Executive Summary

The AI model has classified this incident as a **{threat_level}** threat with a confidence score of **{confidence:.2f}%**.

Country : **{country}**

Region : **{region}**

Attack Type : **{attack}**

Weapon Type : **{weapon}**

Target Type : **{target}**

Estimated Fatalities : **{nkill}**

Estimated Injuries : **{nwound}**

The assessment is based on historical terrorism patterns from the Global Terrorism Database (GTD). This prediction should be used to support operational decision-making together with intelligence gathered from other reliable sources.
""")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🚨 Risk Assessment")

        if threat_level == "LOW":
            st.success("🟢 Low Operational Risk")

        elif threat_level == "MEDIUM":
            st.warning("🟡 Moderate Operational Risk")

        else:
            st.error("🔴 High Operational Risk")

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )

        st.metric(
            "Prediction Confidence",
            f"{confidence:.2f}%"
        )

    with right:

        st.subheader("📌 Strategic Recommendations")

        if threat_level == "LOW":

            st.success(f"""
Continue routine surveillance

Monitor activities within **{country}**

Protect potential **{target}** locations

Maintain intelligence sharing
""")

        elif threat_level == "MEDIUM":

            st.warning(f"""
Increase surveillance operations

Strengthen security around **{target}**

Monitor **{weapon}** related threats

Deploy additional intelligence resources
""")

        else:

            st.error(f"""
Immediate intelligence monitoring required

Deploy rapid response teams

Secure critical infrastructure

Increase surveillance across **{country}**

Coordinate with national security agencies
""")

    st.divider()

    st.subheader("📊 Operational Insights")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Threat Level",
        threat_level
    )

    c2.metric(
        "Risk Score",
        f"{risk_score}/100"
    )

    c3.metric(
        "Confidence",
        f"{confidence:.2f}%"
    )

    st.divider()
    st.subheader("📄 Threat Assessment Report")

    report = f"""
========================================

AI THREAT LEVEL ASSESSMENT REPORT

========================================

Country : {country}

Region : {region}

Attack Type : {attack}

Weapon Type : {weapon}

Target Type : {target}

Estimated Fatalities : {nkill}

Estimated Injuries : {nwound}

Predicted Threat Level : {threat_level}

Confidence Score : {confidence:.2f}%

Risk Score : {risk_score}/100

----------------------------------------

AI Intelligence Summary

The incident has been classified as a {threat_level} threat based on historical GTD patterns. The prediction confidence is {confidence:.2f}% with an operational risk score of {risk_score}/100.

----------------------------------------

Strategic Recommendations

• Increase monitoring in high-risk regions.

• Protect vulnerable targets.

• Strengthen intelligence sharing.

• Improve surveillance against similar attack patterns.

• Continue AI-assisted threat monitoring.

----------------------------------------

Generated By

AI Military Intelligence Dashboard
Version 2.0
"""

    st.download_button(
        "📥 Download Threat Assessment Report",
        report,
        file_name="Threat_Assessment_Report.txt",
        mime="text/plain"
    )

    st.divider()

    st.subheader("✅ AI Decision Support")

    if threat_level == "LOW":

        st.success(
            "The predicted threat is currently LOW. Continue routine monitoring and maintain preventive security measures."
        )

    elif threat_level == "MEDIUM":

        st.warning(
            "The predicted threat is MEDIUM. Increase surveillance and prepare additional security resources."
        )

    else:

        st.error(
            "The predicted threat is HIGH. Immediate operational response and intelligence coordination are recommended."
        )

    st.divider()

    st.caption(
        "AI Military Intelligence Dashboard • Threat Level Prediction System • Version 2.0"
    )