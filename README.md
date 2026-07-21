# AI Military Intelligence Dashboard

An AI-powered Military Intelligence Dashboard developed using **Python**, **Streamlit**, and **Machine Learning** to analyze historical terrorism data from the **Global Terrorism Database (GTD)**. The dashboard provides interactive visualizations, attack prediction, threat assessment, forecasting, and AI-generated intelligence reports.

---

## Project Overview

This project was developed as an academic/internship project to demonstrate how Machine Learning and Data Analytics can be used for intelligence analysis and decision support.

The dashboard allows users to:

- Analyze historical terrorism incidents
- Explore country-wise attack statistics
- Predict probable attack types using Machine Learning
- Forecast future attack trends
- Generate AI-assisted intelligence reports
- Explore and visualize GTD data interactively

---

## Features

- Interactive Home Dashboard
- Global Threat Map
- Country-wise Analysis
- Attack Type Prediction (Random Forest)
- Threat Level Assessment
- Terrorism Forecasting (Linear Regression)
- AI Intelligence Report Generator
- Data Explorer
- Dashboard Settings

---

## Technologies Used
- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Joblib

---

## Dataset

The project uses the **Global Terrorism Database (GTD)**.

---

## Project Structure

```text
AI-Military-Intelligence-Dashboard/
│
├── app.py
├── train_attack_model.py
├── requirements.txt
├── README.md
│
├── data/
│   └── globalterrorism.csv
│
├── models/
│   ├── attack_prediction_model.pkl
│   ├── feature_encoders.pkl
│   ├── target_encoder.pkl
│   └── feature_importance.csv
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Global_Threat_Map.py
│   ├── 3_Country_Analysis.py
│   ├── 4_Attack_Prediction.py
│   ├── 5_Threat_Level_Prediction.py
│   ├── 6_Forecasting.py
│   ├── 7_AI_Intelligence_Report.py
│   ├── 8_Data_Explorer.py
│   └── 9_Settings.py
│
└── utils/
    └── data_loader.py
```

---


## Machine Learning

### Attack Prediction

- Algorithm: Random Forest Classifier
- Encoded categorical features using LabelEncoder
- Predicts the most probable attack type

### Forecasting

- Algorithm: Linear Regression
- Forecasts future attack trends using historical data

---

## Dashboard Modules

1. Home Dashboard
2. Global Threat Map
3. Country Analysis
4. Attack Prediction
5. Threat Level Prediction
6. Forecasting
7. AI Intelligence Report
8. Data Explorer
9. Settings

---

## Future Improvements

- Deep Learning based prediction models
- Real-time data integration
- Natural Language Processing for intelligence reports
- Interactive geospatial analytics
- User authentication and role-based access

---

## License

This project is developed for educational and academic purposes.

---

## Author

**Kshitij**

Academic / Internship Project

AI Military Intelligence Dashboard
