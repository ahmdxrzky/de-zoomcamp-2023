import os
import pathlib
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

url = "https://i.pinimg.com/originals/81/93/c0/8193c0408663871faf26928c15914b0d.png"
pardir = pathlib.Path(__file__).absolute().parent
filename = os.path.join(pardir, "assets", "logo.png")
if not os.path.exists(filename):
    os.system(f"mkdir -p {pardir}/assets")
    os.system(f"wget {url} -O {filename}")

st.set_page_config(page_title="Rain in Australia", layout="wide", initial_sidebar_state="auto", page_icon=filename)
st.markdown(
    f"""
    <style>
    .appview-container .main .block-container{{
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;}}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'> Rain in Australia </h1>", unsafe_allow_html=True)

df = pd.read_csv(os.path.join(pardir, "weatherAUS.csv"))
df['Date'] = pd.to_datetime(df['Date']).dt.date

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Choose start date:", datetime.datetime(2008, 12, 1))
with col2:
    stop_date = st.date_input("Choose stop date:", datetime.datetime(2017, 6, 25))

df = df[(df['Date'] >= start_date) & (df['Date'] <= stop_date)]
df = df.dropna()

col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3 style='text-align: center;'> Total Rainy Day per City </h3>", unsafe_allow_html=True)

    first_df = df[['Location', 'RainToday']].copy()
    first_df = pd.DataFrame(first_df.value_counts())
    first_df.reset_index(inplace=True)
    first_df['Count'] = first_df[0]
    first_df.drop(0, axis=1, inplace=True)

    fig1 = px.bar(
        first_df,
        x = "Location",
        y = "Count",
        color = "RainToday",
        color_discrete_sequence = px.colors.qualitative.Set1,
        height = 510
    )
    fig1.update_layout(font=dict(size=25))
    fig1.update_xaxes(tickangle=45)

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("<h3 style='text-align: center;'> Rainfall per City per Day </h3>", unsafe_allow_html=True)

    city = st.selectbox('City:', tuple(sorted(df['Location'].unique())))
    second_df = df[['Date', 'Location', 'Rainfall', 'RainToday']].copy()
    second_df = second_df[second_df['Location'] == city]

    fig2 = px.line(
        second_df,
        x = 'Date',
        y = 'Rainfall',
        color_discrete_sequence = px.colors.qualitative.Set1
    )
    fig2.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(step="all", label="All"),
                dict(count=1, label="1 Month", step="month", stepmode="backward"),
                dict(count=6, label="6 Month", step="month", stepmode="backward"),
                dict(count=1, label="Year-to-Date", step="year", stepmode="todate"),
                dict(count=1, label="1 Year", step="year", stepmode="backward")
            ])
        )
    )
    fig2.update_layout(
        font=dict(size=20),
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)