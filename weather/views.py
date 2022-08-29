import requests
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm



def index(request):
    appid = 'a6fabe6c31b2920c3dfbce32bad24e56'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'feels_like': res['main']['feels_like'],
            'pressure': res['main']['pressure'],
            'humidity': res['main']['humidity'],
            'wind_speed': res['wind']['speed'],
            'clouds': res['clouds']['all'],
            'icon': res['weather'][0]['icon']
        }

        if city_info not in all_cities:
            all_cities.append(city_info)

        if len(all_cities) > 5:
            all_cities.pop(0)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


