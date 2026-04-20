import pandas as pd
import plotly.express as px
import streamlit as st
import os

st.title("Stock Market Dashboard")

stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]

selected_stock = st.sidebar.selectbox("Select Stock", stocks)

file_path = f"{selected_stock}.csv"

if not os.path.exists(file_path):
    st.error(f"{file_path} not found. Make sure you have downloaded and placed it in this folder.")
else:
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    start_date = st.sidebar.date_input("Start Date", df["Date"].min())
    end_date = st.sidebar.date_input("End Date", df["Date"].max())

    filtered = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date))
    ].copy()

    filtered["Daily Return"] = filtered["Close"].pct_change()
    filtered["Cumulative Return"] = (1 + filtered["Daily Return"]).cumprod() - 1
    filtered["Volatility"] = filtered["Daily Return"].rolling(window=21).std() * (252 ** 0.5)
    filtered["Peak"] = filtered["Close"].cummax()
    filtered["Drawdown"] = (filtered["Close"] - filtered["Peak"]) / filtered["Peak"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Return", f"{filtered['Cumulative Return'].iloc[-1]*100:.2f}%")
    col2.metric("Max Drawdown", f"{filtered['Drawdown'].min()*100:.2f}%")
    col3.metric("Current Volatility", f"{filtered['Volatility'].iloc[-1]*100:.2f}%")

    st.subheader(f"{selected_stock} Price")
    fig1 = px.line(filtered, x="Date", y="Close")
    st.plotly_chart(fig1)

    st.subheader("Cumulative Return")
    fig2 = px.line(filtered, x="Date", y="Cumulative Return")
    st.plotly_chart(fig2)

    st.subheader("Rolling Volatility (Annualised)")
    fig3 = px.line(filtered, x="Date", y="Volatility")
    st.plotly_chart(fig3)

    st.subheader("Drawdown")
    fig4 = px.area(filtered, x="Date", y="Drawdown")
    st.plotly_chart(fig4)

    st.subheader("Raw Data")
    st.dataframe(filtered)