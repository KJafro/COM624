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