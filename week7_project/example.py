import os
import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

url = "https://i.pinimg.com/originals/81/93/c0/8193c0408663871faf26928c15914b0d.png"
filename = os.path.join("assets", "logo.png")
if not os.path.exists(filename):
    os.system("mkdir -p assets")
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

df = pd.read_csv("weatherAUS.csv")
# df['Date'] = pd.to_datetime(df['Date'])
# df['Date'].map(datetime.datetime.date)

# col1, col2 = st.columns(2)
# with col1:
#     start_date = st.date_input("Choose start date:", datetime.date(2008, 12, 1))
# with col2:
#     stop_date = st.date_input("Choose stop date:", datetime.date(2017, 6, 25))

# df = df[(df['Date'] >= start_date) & (df['Date'] <= stop_date)]
# st.text(df.dtypes)
# st.dataframe(df)
# fig4 = px.pie(df,
#               values = 'WindGustDir',
#               names = 'Sex',
#               hole = 0.4,
#               color_discrete_sequence = px.colors.qualitative.Safe)
# fig4.update_layout(font=dict(size=25))
# fig4.update_traces(textinfo='percent')

# fig3 = px.bar(df,
#               x = "Sum",
#               y = "Month",
#               color = "Method",
#               color_discrete_sequence = px.colors.qualitative.Set2)
# fig3.update_layout(font=dict(size=25))

# col1, col2 = st.columns(2)
# with col1:
#     st.plotly_chart(fig4, use_container_width=True)
# with col2:
#     st.plotly_chart(fig3, use_container_width=True)