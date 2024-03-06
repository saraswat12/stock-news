import requests
from twilio.rest import Client


OPEN_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "2CU7LH1QZRFNJ5I6"
NEWS_API = "e9a4c8d65b1b4ebc9804562beba6d4cc"
TWILIO_SID = "ACf25a017b61fa3d812c562ceed912cb49"
TWILIO_AUTH_TOKEN = "63f4941b4110ae53b6128a0698a03101"


parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": API_KEY,

}

response = requests.get(OPEN_ENDPOINT, params=parameters)
#print(response.status_code)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
#print(stock_data)
data_list = [value for (key, value) in data.items()]
#print(data_list)
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
#print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
#print(day_before_yesterday_closing_price)

difference_of_stocks = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference_of_stocks > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

#print(difference_of_stocks)

diff_percent = round((difference_of_stocks / float(yesterday_closing_price)) * 100)
#print(diff_percent)

if abs(diff_percent) > 0.4:
    news_params = {
        "apikey": NEWS_API,
        "qInTitle": "TSLA",

    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articales = news_response.json()['articles']
    three_article = articales[:3]
    #print(three_artical)

    formatted_articales = [f"{'TSLA'}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_article]
    #print(formatted_articales)


    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articales:
        message = client.messages.create(
                            body=article,
                            from_='+18593792286',
                            to='+91 9528284903'
                        )