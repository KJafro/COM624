import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime


class Analyzer:
    def __init__(self):
        self.finviz_url = r"https://finviz.com/quote.ashx?t="

        def Analysis(self, ticker):
            parsed_data = []
            news_dict = {}
            url = self.finviz_url + ticker
            req = Request(url=url, headers={'user-agent': 'COM624'})
            response = urlopen(req)
            html = BeautifulSoup(response, 'html.parser')
            news = html.find(id='news-table').findAll('tr')
            headers = [i.a.text for i in news]
            times = [i.td.text for i in news]
            for index, time in enumerate(times):
                datedata = time.split(' ')
                if (len(datedata) == 2):
                    date = datedata[0]
                    time = datedata[1]
                    news_dict[date] = []
                else:
                    time = datedata[0]
                news_dict[date].append([time, headers[index]])
                parsed_data.append([date, time, headers[index]])
            return self.Results(parsed_data)

