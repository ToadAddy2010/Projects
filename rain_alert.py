import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OMW_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "ACb79a06686b3d709e6be05a6ea2c2ffa0"
auth_token = os.environ.get("TWILLIO_AUTH_TOKEN")


weather_params = {
    "lat": 49.045827,
    "lon": 8.468155,
    "appid": api_key,
    "cnt": 4,
    "units": "metric"
}

response = requests.get(OMW_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain =True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It is going to rain today. Take an umbrella!🌧️☔",
        from_="+12564135669",
        to="+4915221754719"
    )
    print(message.status)
    print("message sent")
else:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="No rain today! Have fun ☀️",
        from_="+12564135669",
        to="+4915221754719"
    )
    print(message.status)
    print("message sent")

