# 🍽️ Food Affordability in Ireland (2014–2024)

This project explores how the **cost of eating healthy** has changed in Ireland over the last decade — and whether rising food prices are making nutritious diets harder to afford.

## 📌 Project Objective

- Analyze **price trends** across common grocery items.
- Measure **affordability** by comparing food basket costs to household income.
- Compare trends by **nutritional category**: Healthy, Neutral, Unhealthy.
- Provide a **Streamlit dashboard** and key insights for policymakers and citizens.

---

## 📊 Dataset Overview

| Source | Description |
|--------|-------------|
| CSO (Ireland) | Monthly food prices for >40 items (2014–2024) |
| HSE & SafeFood | Guidelines and portions for a healthy diet |
| FAO | Guidelines and portions of healthy diet framework |
| CSO | Annual median household income (2014–2024) |

---

## 🧪 Project Workflow

1. **Data Cleaning** (`Food Data Cleaning.ipynb`)
   - Data understanding.   
   - Handled missing values.
   - Standardizes prices (€/kg or €/L).
   - Data quality check.

2. **Exploratory Data Analysis** (`EDA - Food Prices.ipynb`)
   - Tagged items as Healthy, Neutral and Unhealthy.
   - Visualizes price trends, volatility, nutritional categories.
   - Checked and Flagged Outliers.
   - Time-series overview of random items.
   - Exploration at different levels.  

3. **Affordability Modeling** (`Affordability Analysis.ipynb`)
   **Basket Construction**:
   - Modeled a realistic monthly food basket.
   - Quantities based on FAO and HSE dietary recommendations.
    **Affordability Analysis**
   - Compared against median income → **Affordability Ratio**.
   - Created an **Affordability Index (2014 baseline = 100)**.

4. **Dashboard** (`dashb.py`)
   - Interactive dashboard with basket cost, trends, and affordability insights.

---

## 💡 Key Findings

- 📈 Food basket cost increased by **>20%** since 2022.
- 🥦 Healthy foods became the **most expensive and volatile**.
- 💸 Overall Affordability Index dropped, however recently years have damaged the improvements made in the last decade.
- 🧾 Households now spend ~**€35/month more** for the same basket.
- ⚠️ Policy actions are needed to protect access to healthy diets.

---

## 🛠️ Tools & Libraries

- **Languages**: Python, Markdown
- **Libraries**: pandas, numpy, matplotlib, seaborn, plotly, streamlit, openpyxl
- **Tools**: Jupyter Notebooks, Excel, Git/GitHub

---

## 🚀 Try the Dashboard

> 📍 [Launch Food Affordability Dashboard](ADD the LINK after the files are uploaded)

Explore item-level, category-level, and affordability trends over time.
