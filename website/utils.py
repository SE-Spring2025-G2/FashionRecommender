from google_images_search import GoogleImagesSearch
import geocoder
import requests
import os

WEATHER_KEY = os.getenv("WEATHER_KEY")
if not WEATHER_KEY:
    from projectsecrets.weather_secret import WEATHER_KEY

class GeolocationAPI:
    def __init__(self) -> None:
        pass

    """
    Function to fetch current location using IP address
    """

    def getCurrentLocation(self):
        g = geocoder.ip("me")
        return g.city

class WeatherAPI:
    def __init__(self) -> None:
        pass

    """
    Function to fetch current weather forecast using city from external weather API
    """

    def getCurrentWeather(self, latitude=None, longitude=None, city=None):
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={city}&aqi=no"

        print("url: ", url, flush=True)

        try:
            response = requests.request("GET", url, headers={}, data={})
            if response.status_code != 200:
                raise Exception(
                    "Weather API failed : response code : {code}".format(
                        code=response.status_code
                    )
                )
            jsonResponse = response.json()
            if "condition" in jsonResponse["current"]:
                return jsonResponse["current"]["temp_f"], jsonResponse["current"]["condition"]["text"]
            return (None, None)
        except Exception as e:
            print("Error fetching weather: ", str(e), flush=True)
            return (None, None)

    """
    Function to fetch weather forecast for future from external weather API
    """

    def getFutureWeather(self, date=None, city=None, time=None):
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{Date}?key={API_KEY2}".format(
            city=city, Date=date, API_KEY2=self.config.API_KEY
        )
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code != 200:
            raise Exception(
                "Weather API failed : response code : {code}".format(
                    code=response.status_code
                )
            )
        jsonResponse = response.json()
        hours = jsonResponse["days"]["hours"]
        x = (time.split[":"])[0]
        index = 0

        # hours=24
        for t in hours:
            if x == ((hours[0].split[":"])[0]):
                index = t
        return hours[index]["conditions"]


class ImageConfig:
    def __init__(self) -> None:
        self.API_KEY = os.environ.get("GOOGLE_IMAGES_API_KEY")
        self.PROJ_CX = os.environ.get("GOOGLE_IMAGES_PROJ_CX")

class SearchImages:
    def __init__(self) -> None:
        self.config = ImageConfig()
        self.gis = GoogleImagesSearch(self.config.API_KEY, self.config.PROJ_CX)
        self.default_num_of_records = 10

    # gives the list of urls for a search
    def image_search(self, query, num_of_records=None):
        if not num_of_records:
            num_of_records = self.default_num_of_records
        
        print("Searching: ", query, flush=True)
        _search_params = {"q": query, "num": num_of_records}
        self.gis.search(search_params=_search_params)

        image_urls = []
        for image in self.gis.results():
            image_urls.append(image.url)
        return image_urls
