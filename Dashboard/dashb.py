# dashb.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os

# ----------------------
# ✅ Page Configuration
# ----------------------
st.set_page_config(page_title="Food Affordability", layout="wide")
st.title("📊 Food Affordability in Ireland (2014–2024)")

st.markdown("---")

# -----------------------------------------------
# 📂 Load Data
# -----------------------------------------------

# Get the current directory of the script (i.e., Dashboard/)
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

# Use safe paths for all CSV files
afford = pd.read_csv(os.path.join(DATA_DIR, 'affordability_final.csv'), parse_dates=["Date"])
food = pd.read_csv(os.path.join(DATA_DIR, 'food_afford.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'item_summary.csv'))
tags = pd.read_csv(os.path.join(DATA_DIR, 'tag_summary.csv'))


# ----------------------
# ✅ Sidebar or Main Menu Selection
# ----------------------
with st.sidebar:
    st.header("🧭 Navigation")
    view = st.selectbox("Choose Analysis Level", [
        "Project Overview", "Affordability Overview", "Item-Level Analysis",
        "Category-Level Analysis"])
    
# ----------------------
# ✅ Definition of Content Based on View - 4 different "pages" for the sidebar menu
# ----------------------

# ----- HOME DASHBOARD SECTION

def render_home():
    st.header("📘 About This Project")
    st.markdown("""
    Welcome to the **Food Affordability Dashboard** for Ireland (2014–2024).  
    This interactive dashboard allows you to explore how the cost of maintaining a healthy diet has changed over time — and how it compares to household income levels.

    ### 🎯 Goals of the Project
    - Understand food price trends at **item** and **category** levels.
    - Track how **affordability** has shifted monthly and annually.
    - Compare trends across **Healthy**, **Unhealthy**, and **Neutral** food groups.
    - Provide data-driven **insights for policy**, budgeting, and personal health decisions.

    ### 📈 Data Sources
    - Central Statistics Office (CSO).
    - The Food and Agriculture Organization Guidelines (FAO).
    - SafeFood & HSE dietary guidelines.

    ---
    Use the **sidebar** to explore different views and explore more.
    """)

# ----- ITEM-LEVEL DASHBOARD SECTION

def render_item_level():
    st.header("🧾 Item-Level Cost Drivers")
    st.title("📊 Food Prices – Item Level Analysis")

    # Dropdown to select item
    item_selected = st.selectbox("Select a Food Item", sorted(food['Item'].unique()))

    # Filter for selected item
    item_data = food[food['Item'] == item_selected]

    # Line chart: Price trend over time
    fig = px.line(item_data, x="Date", y="Price_per_kg_or_litre", title=f"{item_selected} Price Over Time (€/kg or €/litre)")
    fig.update_layout(title={'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'},
        xaxis_title="Date", yaxis_title="Price (€/kg or L)")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🧠 Price trend reveals how external factors (e.g. inflation, supply chain disruptions) may have impacted this item.")

    # Volatility: std deviation per item
    volatility = food.groupby('Item')['Price_per_kg_or_litre'].std().sort_values(ascending=False)
    top5_most_vol = volatility.head(5).reset_index().rename(columns={"Price_per_kg_or_litre": "Std Dev"})
    top5_least_vol = volatility.tail(5).reset_index().rename(columns={"Price_per_kg_or_litre": "Std Dev"})

    # Display volatility tables
    st.markdown("#### 📉 Price Volatility Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 5 Most Volatile Items")
        st.table(top5_most_vol.style.format({"Std Dev": "{:.2f}"}))
    with col2:
        st.subheader("Top 5 Least Volatile Items")
        st.table(top5_least_vol.style.format({"Std Dev": "{:.2f}"}))

    st.caption("🔍 Volatility highlights which foods fluctuate most — helpful indicator for budgeting or subsidies.")

    # Calculate average price per item
    avg_price = food.groupby("Item")["Price_per_kg_or_litre"].mean().sort_values(ascending=False)
    # Top and bottom 5 items
    top5_expensive = avg_price.head(5).reset_index().rename(columns={"Price_per_kg_or_litre": "Avg Price (€)"})
    top5_cheap = avg_price.tail(5).reset_index().rename(columns={"Price_per_kg_or_litre": "Avg Price (€)"})

    # Layout in 2 columns
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Top 5 Most Expensive Items")
        st.table(top5_expensive.style.format({"Avg Price (€)": "€{:.2f}"}))

    with col4:
        st.subheader("Top 5 Least Expensive Items")
        st.table(top5_cheap.style.format({"Avg Price (€)": "€{:.2f}"}))

    st.caption("💡 Consistently expensive items tend to be lean proteins or premium items like smoked salmon.")

    # -------------------
    # Insights
    # -------------------
    st.markdown("### 🧠 Key Insights")
    st.info(f"""
    - The most **price-volatile items** were **the meats**, showing significant fluctuations over time.
    - In contrast, staple items like **flour and milk** had the most stable pricing.
    - The **most expensive item on average** was the **smoked salmon per kg**, while **Full Fat Milk** was the cheapest.
    - Price volatility could be related to imported or seasonal products, while staples remain steady.
    - Understanding volatility helps policymakers and consumers plan for **price shocks**.
    """)

# ----- CATEGORY-LEVEL DASHBOARD SECTION

def render_Category_level_Analysis():
    st.header("🥦 Healthy-Related Category Food Trends")
    st.markdown("**Healthy foods** have become more expensive faster than processed foods.")

    # -------------------
    # 1. Metric Selection
    # -------------------
    metric_selected = st.radio("Select price metric:", ["Mean", "Median"], horizontal=True)

    # -------------------
    # 2. Monthly Aggregation
    # -------------------
    monthly_stats = (
        food.groupby(['Date', 'Tag'])['Price_per_kg_or_litre']
        .agg(['mean', 'median'])
        .reset_index()
        .rename(columns={'mean': 'Monthly_Mean', 'median': 'Monthly_Median'}))

    # Filter to selected metric
    metric_col = f'Monthly_{metric_selected}'
    monthly_filtered = monthly_stats[['Date', 'Tag', metric_col]].rename(columns={metric_col: 'Price'})

    # -------------------
    # 3. YoY % Change Calculation
    # -------------------
    pivot = monthly_stats.pivot(index='Date', columns='Tag', values=metric_col)
    yoy = pivot.pct_change(periods=12) * 100
    yoy_long = yoy.reset_index().melt(id_vars='Date', var_name='Tag', value_name='YoY_Change')

    # -------------------
    # 4. Color Map
    # -------------------
    color_map = {
        'Healthy': 'green',
        'Neutral': 'blue',
        'Unhealthy': 'red'}

    # -------------------
    # 5. Plot Monthly Prices
    # -------------------
    fig_price = px.line(
        monthly_filtered,
        x='Date',
        y='Price',
        color='Tag',
        title=f"📈 Monthly Prices by Category ({metric_selected})",
        color_discrete_map=color_map)
    fig_price.update_layout(
        title={'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'},
        yaxis_title="Price (€/kg or L)",
        xaxis_title="Date",
        hovermode="x unified",
        template="plotly_white")
    st.plotly_chart(fig_price, use_container_width=True)

    st.caption(f"📌 Healthy food prices ({metric_selected}) have trended higher than others.")

    # -------------------
    # 6. Plot YoY % Change
    # -------------------
    fig_yoy = px.line(
        yoy_long,
        x='Date',
        y='YoY_Change',
        color='Tag',
        title=f"📉 Year-over-Year % Change in Prices ({metric_selected})",
        color_discrete_map=color_map)
    fig_yoy.update_layout(
        title={'font': {'size': 24}, 'x': 0.5, 'xanchor': 'center'},
        yaxis_title="% Change",
        xaxis_title="Date",
        hovermode="x unified",
        template="plotly_white")
    st.plotly_chart(fig_yoy, use_container_width=True)

    st.caption("⚠️ Year-over-year price shifts show volatility, it highlights the magnitude of the increase between 2022 and 2024.")

    # -------------------
    # 7. Summary Table
    # -------------------
    st.markdown("### 📊 Nutrition Category Summary")
    summary_data = {
        "Category": ["Healthy", "Neutral", "Unhealthy"],
        "Mean Price": ["€7.52", "€6.53", "€6.45"],
        "Median Price (50%)": ["€3.65", "€2.20", "€5.27"],
        "Skew (Mean > Median?)": ["High", "Very High", "Low"],
        "Price Stability (std)": ["Medium (7.01)", "High (9.64)", "Stable (5.40)"]}
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df.set_index("Category"))

    st.caption("📋 A large gap between mean and median (e.g. Healthy: €7.52 vs €3.65) suggests a few expensive items (mainly proteins) drive up the average — indicating price inequality within that category.")

    # -------------------
    # 8. Insights
    # -------------------
    st.markdown("### 🧠 Key Insights")
    st.info("""
    - Among categories:
        - **Healthy** foods had the **highest average price** (€7.52), but a **low median** (€3.65), indicating price skew due to high number of proteins in the category.
        - **Neutral** foods were the most **volatile** (std = 9.64), showing inconsistent pricing across time.
        - **Unhealthy** foods were **more stable and affordable**, with a lower std (5.40) and a small gap between mean (€6.45) and median (€5.27).
    - These patterns suggest that maintaining a healthy diet may be **less predictable and more expensive**, potentially impacting food equity and public health.
""")

# ----- AFFORDABILITY DASHBOARD SECTION

def render_affordability():
    st.header("💶 Affordability Analysis (2014–2024)")
    st.markdown("This section shows how affordable a healthy food basket is relative to household income in Ireland.")

    # --- View Toggle ---
    view_type = st.radio("Select time granularity:", ["Monthly", "Annual"], horizontal=True)

    # ===============================
    # Monthly View
    # ===============================
    if view_type == "Monthly":
        # 1A. Monthly Basket Cost
        st.subheader("📅 Monthly Basket Cost (€)")
        fig_monthly = px.line(
            afford,
            x="Date",
            y="Basket_Cost_Euro",
            title="Monthly Basket Cost (€)",
            labels={"Basket_Cost_Euro": "€"})
        fig_monthly.update_layout(title={'x': 0.5})
        st.plotly_chart(fig_monthly, use_container_width=True)

        st.caption("📌 Basket costs rose steadily across the decade, with post-2021 showing the steepest increases.")

        # 2A. Monthly YoY % Change
        st.subheader("📉 Monthly Year-over-Year % Change")
        monthly_yoy = afford.copy()
        monthly_yoy["Monthly_YoY_%"] = monthly_yoy["Basket_Cost_Euro"].pct_change(periods=12) * 100
        fig_monthly_yoy = px.line(
            monthly_yoy.dropna(),
            x="Date",
            y="Monthly_YoY_%",
            title="Monthly YoY % Change in Basket Cost",
            labels={"Monthly_YoY_%": "% Change"})
        fig_monthly_yoy.update_layout(title={'x': 0.5}, yaxis_title="% Change")
        st.plotly_chart(fig_monthly_yoy, use_container_width=True)

        st.caption("📌 The largest YoY spike occurred in **Jan 2023**, with a **13.87%** increase — likely reflecting inflation shocks.")

    # ===============================
    # Annual View
    # ===============================
    else:
        # 1B. Average Basket Cost by Year
        st.subheader("📊 Average Annual Basket Cost (Per Month Average × 12)")
        yearly_avg = afford.groupby(afford['Date'].dt.year)["Basket_Cost_Euro"].mean().reset_index()
        yearly_avg.columns = ["Year", "Avg_Basket_Cost"]
        fig_basket = px.bar(
            yearly_avg,
            x="Year",
            y="Avg_Basket_Cost",
            labels={"Avg_Basket_Cost": "€"},
            title="Average Monthly Basket Cost (Annual View)")
        fig_basket.update_layout(title={'x': 0.5})
        st.plotly_chart(fig_basket, use_container_width=True)

        st.caption("📋 Although this shows monthly averages, the annual trend reveals steady cost increases — indicating a sustained rise in essential food prices.")

        # 2B. Annual YoY % Change (from average)
        st.subheader("📈 Year-over-Year % Change (Based on Avg Monthly)")
        yearly_avg["YoY Change (%)"] = yearly_avg["Avg_Basket_Cost"].pct_change() * 100
        fig_yoy = px.bar(
            yearly_avg.dropna(),
            x="Year",
            y="YoY Change (%)",
            title="Year-over-Year % Change in Avg Basket Cost",)
        fig_yoy.update_layout(title={'x': 0.5})
        st.plotly_chart(fig_yoy, use_container_width=True)

        st.caption("📈 Sharp jumps (e.g. 2022–2023) highlight how had inflationary spikes hit household food budgets in recent years.")

        #  Total Annual Cost (Summed over months)
        st.subheader("🧾 Total Annual Basket Cost (€ per Year)")
        yearly_total = afford.groupby(afford['Date'].dt.year)["Basket_Cost_Euro"].sum().reset_index()
        yearly_total.columns = ["Year", "Total_Basket_Cost"]
        fig_total = px.bar(
            yearly_total,
            x="Year",
            y="Total_Basket_Cost",
            title="Total Basket Cost Spent per Year (€)",
            labels={"Total_Basket_Cost": "€"})
        fig_total.update_layout(title={'x': 0.5}, yaxis_title="€")
        st.plotly_chart(fig_total, use_container_width=True)

        st.caption("💸 Total yearly food spending climbed from €3,265.41 in 2014 to €3,688.87 in 2024 — widening the affordability gap, especially for low-income families.")

    # 3 A/B. Affordability Ratio
    st.subheader("📉 % of Income Spent on Food Basket")
    fig_ratio = px.line(
        afford,
        x="Date",
        y="Affordability_Ratio",
        title="Affordability Ratio Over Time",
        labels={"Affordability_Ratio": "% of Income"},)
    fig_ratio.update_layout(title={'x': 0.5}, yaxis_title="% of Income")
    st.plotly_chart(fig_ratio, use_container_width=True)
    st.caption(f"📌 In 2024, households spent an average of just **7.3%** of income on food — a drop from 9% in 2014.")

    # 4 A/B. Affordability Index (Monthly or Annual)
    st.subheader("📈 Affordability Index (2014 = 100)")

    if view_type == "Monthly":
        fig_index_monthly = px.line(
            afford,
            x="Date",
            y="Affordability_Index",
            title="Affordability Index (Monthly)",
            labels={"Affordability_Index": "Index"})
        fig_index_monthly.update_layout(title={'x': 0.5}, yaxis_title="Index")
        st.plotly_chart(fig_index_monthly, use_container_width=True)
        st.caption("📌 The Affordability Index peaked in **Jan 2014 (102.38)**, but has since dropped to an average of **79.17** in 2024 — indicating food is less affordable relative to income.")

    else:
        annual_index = afford.groupby(afford["Date"].dt.year)["Affordability_Index"].mean().reset_index()
        annual_index.columns = ["Year", "Avg_Index"]
        fig_index_annual = px.bar(
            annual_index,
            x="Year",
            y="Avg_Index",
            title="Affordability Index (Annual Avg)",
            labels={"Avg_Index": "Index"})
        fig_index_annual.update_layout(title={'x': 0.5}, yaxis_title="Index")
        st.plotly_chart(fig_index_annual, use_container_width=True)
        


    # ===============================
    # Insights Section
    # ===============================
    st.markdown("### 🧠 Summary Insights")
    st.info(f"""
    - Over the past 10 years, the cost of a healthy food basket increased by **13%**, but affordability has improved due to stronger income growth.
    - The **Affordability Ratio** has declined from ~9% to **7.3%**, signaling reduced financial pressure from food costs.
    - Despite improved ratios, the **Affordability Index** fell by ~23 points — showing that while food is a smaller share of income, it's still harder to buy the same basket.
    - YoY volatility highlights economic stress points like **2023**.
    - These insights support further research or **policy** targeting affordability gaps, especially for lower-income households.
    """)



# ----------------------
# ✅ Render Selected View
# ----------------------

if view == "Project Overview":
    render_home()

elif view == "Item-Level Analysis":
    render_item_level()

elif view == "Category-Level Analysis":
    render_Category_level_Analysis()

elif view == "Affordability Overview":
    render_affordability()

# ----------------------
# ✅ 7. Footer
# ----------------------
st.markdown("---")
st.caption("Created using Streamlit & Plotly | Data: CSO, FAO, SafeFood, HSE")

