import requests
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim


@csrf_exempt
@cache_page(60 * 30)
def get_weather(request, city_name):
    geolocator = Nominatim(user_agent="WeatherApp")
    location = geolocator.geocode(city_name)

    if not location:
        return JsonResponse({'ошибка': 'нет такого города'}, status=400)

    lat, lon = location.latitude, location.longitude

    api_key = 'c3c83c1f-99f1-4940-bc40-1702b21eaacf'
    url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&extra=true'
    headers = {'X-Yandex-API-Key': api_key}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    try:
        temp = data['fact']['temp']
        pressure = data['fact']['pressure_mm']
        wind_speed = data['fact']['wind_speed']
    except KeyError:
        return JsonResponse({'error': 'Invalid response from Yandex'}, status=500)

    return JsonResponse({
        'temp': temp,
        'pressure': pressure,
        'wind speed': wind_speed
    })
