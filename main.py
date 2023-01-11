import datetime
import pandas as pd
import base64
import streamlit as st
import yfinance as yf
from urllib import request
from plotly import graph_objs as ts
from streamlit_extras.colored_header import colored_header
from analysis import Analyzer
from group import Group
from prediction import Prediction


# Page config with CSS styles

st.set_page_config(
    page_title="COM624 Stock Predictor",
    page_icon="💰",
    layout="wide",
)
m = st.markdown("""
<style>
div.stButton {
    display: flex;
    justify-content: center;
    }

div.stButton > button:first-child {
    background-color: green;
    color: white;
    box-shadow: 1px 1px 1px 1px black;
    width: 150px;
    padding: 4px;
    margin-bottom: 0px;
}

div.stButton > button:first-child:hover {
    background-color: rgb(50, 144, 50);
    font-weight: bold;
    color: white;
    border: 1px solid rgb(50, 144, 50);
}

div.stMarkdown {
text-align: center;
}

css-163ttbj.e1fqkh3o11 {
background-color: rgb(182, 179, 179);
}

.css-163ttbj.e1fqkh3o11 {
border-radius: 4px;
}

.css-6qob1r.e1fqkh3o3 {
text-align: center;
}

.css-1vq4p4l.e1fqkh3o4 {
display: flex;
justify-content 
text-align: center;
}

.css-qri22k.egzxvld0 {
text-align: center;
}

.css-18ni7ap.e8zbici2 {
background-color: rgb(234, 229, 229);
}

.stApp.streamlit-wide.css-fg4pbf.eczokvf1 {
background: linear-gradient(rgb(234, 229, 229), rgb(159, 162, 164));
}

.css-keje6w.e1tzin5v2 {
margin-bottom: 20px;
}

.css-1a32fsj.e19lei0e0 {
display: flex;
justify-content: center;
text-align: center;
margin-top: 20px;
}
</style>""", unsafe_allow_html=True)

analyzer = Analyzer()
groups = Group()
prediction = Prediction(groups)

# Web Scraping

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

colored_header(label=" ", description=" ", color_name="blue-70")

st.sidebar.markdown(
    """<p style="
     text-align: center;
     font-family: Helvetica;
     font-weight: 500; 
     padding: 130px;
     color: rgb(44, 130, 201); 
     font-size: 34px;
     "></p>""", unsafe_allow_html=True)

# Sidebar

df = load_stocks()
sector = df.groupby('GICS Sector')
sorted_sector = sorted(df['GICS Sector'].unique())
selected_multi = st.sidebar.multiselect('**Sector**',sorted_sector)
df_selected_multi = df[df['GICS Sector'].isin(selected_multi)]

START = st.sidebar.date_input(label="**Enter Start Date**",value=datetime.date(2018,1,1))
TODAY = datetime.date.today().strftime("%Y-%m-%d")

if len(selected_multi) != 0:
    stocks = df_selected_multi.Symbol.values
else:
    stocks = df.Symbol.values
chosen_stock = st.sidebar.selectbox("**Select a Stock**",stocks)

data = pd.DataFrame()
processed_data = pd.DataFrame()

# Downloadable CSV file

def downloadcsv(data, message):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    if message == "Raw":
        href = f'<a href="data:file/csv;base64,{b64}" download="{chosen_stock}_RAW.csv">Download Stock History</a>'
    return href

# Showing Earliest/Latest data of stock

if chosen_stock != None:
    data, stock_details = load_data(chosen_stock)
    container = st.container()
    col1, col2 = container.columns([5, 5])

    col2.subheader(f"Latest Data")
    col2.write(data.tail(20))
    col2.markdown(downloadcsv(data, "Raw"), unsafe_allow_html=True)

    col1.subheader(f"Earliest Data")
    col1.write(data.head(20))
    col1.markdown(downloadcsv(data, "Raw"), unsafe_allow_html=True)

# Plotting Time Series graph

    def plot_time():
        fig = ts.Figure()
        fig.add_trace(ts.Line(x=data['Date'], y=data['Close'], name="Stock Close"))
        fig.add_trace(ts.Line(x=data['Date'], y=data['Open'], name="Stock Open"))
        fig.layout.update(xaxis_rangeslider_visible=True, yaxis_title="£")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    plot_time()

else:

    def plot_histo():
        fig = ts.Figure()
        fig.add_trace(ts.Histogram(x=data['Date'], y=data['Close'], name="Stock Close"))
        fig.add_trace(ts.Histogram(x=data['Date'], y=data['Open'], name="Stock Open"))
        fig.update_layout(xaxis_rangeslider_visible=True, yaxis_title="£")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")
    plot_histo()
colored_header(label=" ", description=" ", color_name="blue-70")

st.markdown(
    """<p style="text-align: center; margin-top: 20px; font-size: 28px; font-weight: bold;">Predict Stock</p>""",
    unsafe_allow_html=True)
st.markdown(
    """<p style="text-align: center; font-size: 22px;">Click the button below to predict</p>""", unsafe_allow_html=True)

def predict(chosen_stock, data):
    analysis_result = analyzer.Analysis(chosen_stock)
    tomo_price, today_pred_price, today_actual_price = prediction.predict(data, chosen_stock)
    return tomo_price, today_pred_price, today_actual_price, analysis_result

if st.button("Predict"):
    loading_message = st.success("Please wait... This process can take around 10 seconds!")

    if chosen_stock != None:
        tomo_price, today_pred_price, today_actual_price, analysis_result = predict(chosen_stock,data)
    loading_message.success("Success!")
    st.markdown(f"""<p style="text-align:center; font-size: 20px;">
    <strong>Tomorrow </strong>  {(datetime.date.today() + datetime.timedelta(days=1)).strftime("(<strong>%Y-%m-%d</strong>)")}
    <br>
    <strong>Predicted Price = {tomo_price} USD</strong>
    <br>
    <br>
    <strong>Analysis: {analysis_result}</p>
    """, unsafe_allow_html=True)
    st.write(data.describe())