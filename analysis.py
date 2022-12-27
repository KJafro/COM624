import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Web Scraping

class Analyzer:
    def __init__(self):
        self.finviz_url = r"https://finviz.com/quote.ashx?t="

    def Analysis(self,ticker):
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
            if( len(datedata) == 2):
                date = datedata[0]
                time = datedata[1]
                news_dict[date] = []
            else :
                time = datedata[0]
            news_dict[date].append([time, headers[index]])
            parsed_data.append([date, time, headers[index]])
        return self.Results(parsed_data)

        # Sentiment Results

    def Results(self,table):
        df = pd.DataFrame(table, columns=['Date', 'Time', 'Headline'])
        vader = SentimentIntensityAnalyzer()
        p_scores = []
        for i in df['Headline']:
                p_scores.append(vader.polarity_scores(i)['compound'])
        import statistics
        mn = statistics.mean(p_scores)
        if mn == 0.0:
            return '🟠 Uncertain'
        elif mn > 0 and mn <= 0.4 :
            return '🟢 We suggest you buy the stock 😀'
        elif mn > 0.4 :
            return '🟢 We highly suggest you buy the stock 🤑'
        elif mn < 0 and mn >= -0.4 :
            return '🔻 We suggest you dont buy the stock 🙁'
        else :
            return '🔻 We highly suggest you dont buy the stock ☹'

