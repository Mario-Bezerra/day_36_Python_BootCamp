import requests
import datetime as dt
from twilio.rest import Client

today = dt.date.today()
yesterday = str(today - dt.timedelta(days=1))
yesyesterday = str(today - dt.timedelta(days=2))

#
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "XXXXXXXXXXXXXXXXX"
NEWS_API_KEY = "XXXXXXXXXXXXX"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# using API STOCK
# params for the stock
params_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : STOCK_API_KEY,
}
response_stock = requests.get(url=STOCK_ENDPOINT,params=params_stock)
response_stock.raise_for_status()
data_stock = response_stock.json()
# modulating data
data_stock_yesterday = float(data_stock["Time Series (Daily)"][yesterday]["4. close"])
data_stock_yesyesterday = float(data_stock["Time Series (Daily)"][yesyesterday]["4. close"])
variation = round(((data_stock_yesterday*100)/data_stock_yesyesterday)-100,3)
if variation>0:
    up_down = "🔺"
else:
    up_down = "🔻"

over_two = False
if variation > 2 or variation < -2:
    over_two = True
if over_two:
    params_news ={
        "qInTitle":COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }
    response_news = requests.get(url=NEWS_ENDPOINT,params=params_news)
    response_news.raise_for_status()
    data_news = response_news.json()['articles']
    three_articles = data_news[:3]

    # modulating message
    formated_message = [f"{STOCK}:{up_down}{variation}% \n " \
                        f"Headline : {data_news['title']}.\n " \
                        f"Brief : {data_news['description']}" for data_news in three_articles]

    # send SMS api
    account_sid = "xxxxxxxxx"
    auth_token = "xxxxxxxx"
    client = Client(account_sid, auth_token)
    for article in formated_message:
        message = client.messages \
            .create(
            body=f"{article}",
            from_='xxxxxx',
            to='xxxxxxxx'
        )
        print(message.status)





