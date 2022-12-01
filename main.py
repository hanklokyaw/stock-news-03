import requests
from twilio.rest import Client
import os

STOCK = "NYSE:C"
COMPANY_NAME = "Citigroup Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_API_KEY = "0LTINMCWPT0UN1QR"
NEWS_API_KEY = "7b4b23c8002845f0bebcc7e72dda900b"

TWILIO_SID = "AC8a8368ee4ec090be2997b742587f5f45"
TWILIO_AUTH_TOKEN = "1e9493b4680ea9891a6994e94a790e4f"

stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : STOCK_API_KEY
}

arrow_sign = None

stock_data_raw = requests.get(url=STOCK_ENDPOINT, params=stock_params)
print(stock_data_raw.status_code)
stock_data_raw = stock_data_raw.json()['Time Series (Daily)']
print(stock_data_raw)

date = []
for i in stock_data_raw:
    date.append(i)

stock_data_list = [value for (key,value) in stock_data_raw.items()]
print(stock_data_list)
yesterday_close = float(stock_data_list[0]["4. close"])
before_yesterday_close = float(stock_data_list[1]["4. close"])
yesterday_date = date[0]
before_yesterday_date = [1]
print(yesterday_close)
print(before_yesterday_close)


difference = round(yesterday_close - before_yesterday_close,2)
print(difference)

if difference > 0:
    arrow_sign = "🔺"
else:
    arrow_sign = "🔻"

diff_percentage = round(difference / yesterday_close, 2) * 100
print(diff_percentage)

news_api = {
    "apiKey" : NEWS_API_KEY,
    "q" : COMPANY_NAME,
    "from" : before_yesterday_date,
    "to" : yesterday_date,
    "language" : "en",
}

news_dict = requests.get(url=NEWS_ENDPOINT, params=news_api)
print(news_dict.status_code)
news_dict = news_dict.json()
articles = news_dict['articles']
print(news_dict)
print(articles)


for article in range(0,3):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"{STOCK} {arrow_sign}{difference}%\n Headline: {articles[article]['title']}.\nDescription: {articles[article]['description']}",
        from_ = "+17695532769",
        to = "+9592032611"
    )





