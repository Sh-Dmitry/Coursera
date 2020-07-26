
import requests

API_KEY_YAN_WEATHER = ''
API_KEY_YAN_GEO = ''


class YandexWeatherApi:

    @staticmethod
    def get_weather(position):

        url = f"https://api.weather.yandex.ru/v2/forecast?lat={position[1]}&lon={position[0]}&extra=true"
        headers = {'X-Yandex-API-Key': API_KEY_YAN_WEATHER}
        data = requests.get(url, headers=headers).json()
        forecast = {
            "Температура": data["fact"]["temp"],
            "Часовой пояс": data["info"]["tzinfo"]["name"],
            "Дата": data["forecasts"][0]["date"]
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
        return self._weather_forecast.get_weather(geo)


def _main(city):
    city_info = CityInfo(city)
    forecast = city_info.weather_forecast()
    print(forecast)


if __name__ == "__main__":
    city = input()
    _main(city)
