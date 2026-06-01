
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Data Visualization & Storytelling")

uploaded_file = st.file_uploader("Upload Superstore CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="latin1")

    st.sidebar.header("Filters")

    regions = st.sidebar.multiselect(
        "Region",
        options=sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique())
    )

    categories = st.sidebar.multiselect(
        "Category",
        options=sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique())
    )

    filtered = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories))
    ]

    total_sales = filtered["Sales"].sum()
    total_profit = filtered["Profit"].sum()
    total_orders = filtered["Order ID"].nunique()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Profit", f"${total_profit:,.0f}")
    c3.metric("Total Orders", f"{total_orders:,}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        sales_region = filtered.groupby("Region")["Sales"].sum().reset_index()
        fig = px.bar(
            sales_region,
            x="Region",
            y="Sales",
            title="Sales by Region"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        profit_category = filtered.groupby("Category")["Profit"].sum().reset_index()
        fig = px.pie(
            profit_category,
            names="Category",
            values="Profit",
            title="Profit by Category"
        )
        st.plotly_chart(fig, use_container_width=True)

    segment_profit = filtered.groupby("Segment")["Profit"].sum().reset_index()
    fig = px.bar(
        segment_profit,
        x="Segment",
        y="Profit",
        color="Segment",
        title="Profit by Customer Segment"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📌 Business Insights")

    best_region = filtered.groupby("Region")["Sales"].sum().idxmax()
    best_category = filtered.groupby("Category")["Profit"].sum().idxmax()

    st.write(f"• Highest sales region: **{best_region}**")
    st.write(f"• Most profitable category: **{best_category}**")
    st.write("• Focus on profitable categories and regions for growth.")
else:
    st.info("Upload samplesuperstore.csv to begin.")
