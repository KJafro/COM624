import datetime
import pandas as pd
import base64
import streamlit as st
import yfinance as yf
from urllib import request

@st.cache
def load_stocks():
    url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = request.urlopen(url)
    html = response.read()
    data = pd.read_html(html,header = None)
    df = data[0]
    return df

@st.cache(allow_output_mutation=True)
def load_data(ticker):
    data = yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    stock_data = yf.Ticker(ticker)
    return (data, stock_data)

st.markdown(
    """<p style="text-align: center;"><span style="color: rgb(44, 130, 201); font-size: 50px;"><strong>Stock Predictor COM624</strong></span></p>""",
    unsafe_allow_html=True)
st.markdown(
    """<p style="text-align: center; font-size: 22px;">Instructions:</p>""", unsafe_allow_html=True)
st.markdown(
"""<p style="text-align: center; font-size: 18px;">
1) Select the Sector of the Stock you wish to view
<br>
2) Enter the start date you wish to view the stock from
<br>
3) Select Stock from the dropdown list
<br>
4) Scroll to the bottom and click the 'Predict' button</p>""", unsafe_allow_html=True)

st.write('---')
st.sidebar.markdown(
    """<p style="
     text-align: center;
     font-family: Helvetica;
     font-weight: 500; 
     padding: 130px;
     color: rgb(44, 130, 201); 
     font-size: 34px;
     "></p>""", unsafe_allow_html=True)

df = load_stocks()
sector = df.groupby('GICS Sector')
sorted_sector = sorted(df['GICS Sector'].unique())
selected_multi = st.sidebar.multiselect('**Sector**',sorted_sector)
df_selected_multi = df[df['GICS Sector'].isin(selected_multi)]

START = st.sidebar.date_input(label="**Enter Start Date**",value=datetime.date(2018,1,1))
TODAY = datetime.date.today().strftime("%Y-%m-%d")