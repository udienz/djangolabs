import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .helper import env

# Create your views here.

API = env("OPENWEATHERMAP_API", default=None)
CITY = "1627253"
URL = "https://api.openweathermap.org/data/2.5/weather?id="


@login_required(login_url='/accounts/login/')
def get_home(request):
    url = URL + str(CITY) + "&units=metric&lang=id&appid=" + str(API)
    r = requests.get(url)
    data = r.json()

    name = data["name"]
    weather = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    temp = data["main"]["temp"]
    context = {
        "cityname": name,
        "cityweather": weather,
        "cityicon": icon,
        "citytemp": temp,
        "cityhumidity": humidity,
        "citywind": wind
    }

    return render(
        request,
        "pages/home.html",
        context
    )
