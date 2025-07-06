import requests
from twilio.rest import Client

OMW_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "7f977d6bc445f55916bd0bb90069868e"
account_sid = "ACb79a06686b3d709e6be05a6ea2c2ffa0"
auth_token = "f5f88c12f371151dee2fc06e8caded5b"


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
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today. Take an umbrella!🌧️☔",
        from_="+12564135669",
        to="+4915221754719"
    )
    print(message.status)

