import pprint
import requests

API_KEY_YAN_WEATHER = '7df82de8-c6f1-4b05-8e3b-4c9b064ddcfa'
API_KEY_YAN_GEO = '5e521ec3-ff98-40f5-ab93-af04011b09cf'


class YandexWeatherApi:

    @staticmethod
    def get(position):
        url = f"https://api.weather.yandex.ru/v2/forecast?/lon={position[0]}&lat={position[1]}"
        headers = {'X-Yandex-API-Key': API_KEY_YAN_WEATHER}
        data = requests.get(url, headers=headers).json()
        forecast = {
            "Температура": data["fact"]["temp"],
            "Место": data["info"]["tzinfo"]["abbr"]
        }  # остановился тут
        return forecast


class YandexGeoApi:

    @staticmethod
    def get_point(city):
        url = f"https://geocode-maps.yandex.ru/1.x/?format=json&apikey={API_KEY_YAN_GEO}&geocode={city}"
        data = requests.get(url).json()
        point = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        return point.split()


class CityInfo:

    def __init__(self, city, weather_forecast=None, geo_location=None):
        self.city = city
        self._weather_forecast = weather_forecast or YandexWeatherApi()
        self._geo_location = geo_location or YandexGeoApi()

    def weather_forecast(self):
        geo = self._geo_location.get_point(self.city)
        return self._weather_forecast.get(geo)


def _main():
    city_info = CityInfo("Moscow")
    forecast = city_info.weather_forecast()
    pprint.pprint(forecast)


if __name__ == "__main__":
    _main()
