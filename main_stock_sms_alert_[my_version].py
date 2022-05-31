import requests
import datetime
from twilio.rest import Client

# ------------------------sites and keys------------------------------- #
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "4KU4CCJ4DLEFO11J"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "e77da260339d425a8329106431d61f64"
account_sid = "AC7754033be4d40c8b69e73b89305c376b"
auth_token = "635d686abbd902f6313e3f0d7054a411"
client = Client(account_sid, auth_token)

# ------------------------date setup------------------------------- #
today = datetime.datetime.now().day
yesterday_date = today - 1
formatted_yesterday_date = f"2021-09-{yesterday_date}"
day_before_yesterday = today - 2
formatted_day_before_yesterday = f"2021-09-0{day_before_yesterday}"

# ------------------------stock difference ------------------------------- #
today_params_stock = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": STOCK_API_KEY,
}

today_stock_data = requests.get(url=STOCK_ENDPOINT, params=today_params_stock)
yesterday_file = float(
    today_stock_data.json()["Time Series (60min)"][f"{formatted_yesterday_date} 20:00:00"]["4. close"])
print(yesterday_file)
print(type(yesterday_file))
day_before_yesterday_file = float(
    today_stock_data.json()["Time Series (60min)"][f"{formatted_day_before_yesterday} 20:00:00"]["4. close"])
print(day_before_yesterday_file)
print(type(day_before_yesterday_file))

closing_difference = (yesterday_file - day_before_yesterday_file)
absolute_closing_difference = abs(yesterday_file - day_before_yesterday_file)
percentage_difference = absolute_closing_difference / yesterday_file * 100
print(percentage_difference)

# ------------------------up and down sign ------------------------------- #
sign = ""
if closing_difference < 0:
    sign = "🔻"
elif closing_difference > 0:
    sign = "🔺"

# ------------------------getting actual news ------------------------------- #
news_params = {
    "apiKey": NEWS_API_KEY,
    "q": "Tesla Inc",
    "language": "en",

}
news = requests.get(url=NEWS_ENDPOINT, params=news_params)
news_title1 = (news.json()["articles"][0]["title"])
news_brief1 = (news.json()["articles"][0]["content"])
news_title2 = (news.json()["articles"][5]["title"])
news_brief2 = (news.json()["articles"][5]["content"])
news_title3 = (news.json()["articles"][15]["title"])
news_brief3 = (news.json()["articles"][15]["content"])

msg1 = f"TSLA: {sign}{percentage_difference}% \nHeadline: {news_title1} \nBrief: {news_brief1}"
msg2 = f"TSLA: {sign}{percentage_difference}% \nHeadline: {news_title2} \nBrief: {news_brief2}"
msg3 = f"TSLA: {sign}{percentage_difference}% \nHeadline: {news_title3} \nBrief: {news_brief3}"


# ------------------------msg function and body ------------------------------- #
def get_news1():
    message = client.messages.create(
        body=msg1,
        from_='+19493045636',
        to='+918607459865'
    )

    print(message.status)


def get_news2():
    message = client.messages.create(
        body=msg2,
        from_='+19493045636',
        to='+918607459865'
    )

    print(message.status)


def get_news3():
    message = client.messages.create(
        body=msg3,
        from_='+19493045636',
        to='+918607459865'
    )

    print(message.status)


# ------------------------sending msg ------------------------------- #
if percentage_difference > 5:
    get_news1()
    get_news2()
    get_news3()
