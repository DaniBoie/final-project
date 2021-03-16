import urllib
import json
import re
from urllib import request, error


class OpenWeather:
  def __init__(self, zipcode: str, country_code: str, apikey: str):
    weather_obj = None
    self.error = False
    self.error_code = None

    # A set of try except statements to make sure the variables are of type string.
    try:
        assert isinstance(zipcode, str)
    except AssertionError:
        print("Invalid Zipcode: Must be of type string")
        self.error = True
    else: 
        self.zipcode = zipcode.replace(' ', '')
    
    try:
        assert isinstance(country_code, str)
    except AssertionError:
        print("Invalid Country code: Must be of type string")
        self.error = True
    else:
        self.ccode = country_code.replace(' ', '')

    try:
        assert isinstance(apikey, str)
    except AssertionError:
        print("Invalid API key: Must be of type string")
        self.error = True
    else:
        self.apikey = apikey.replace(" ", '')

    # If there is no error yet present in the program, continue and connect to API.
    if self.error == False:
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"
        weather_obj = self._download_url(url)

    if weather_obj is not None:
        self.temperature = weather_obj['main']['temp']
        self.high_temperature = weather_obj['main']['temp_max']
        self.low_temperature = weather_obj['main']['temp_min']
        self.longitude = weather_obj['coord']['lon']
        self.latitude = weather_obj['coord']['lat']
        self.description = weather_obj['weather'][0]['description']
        self.humidity = weather_obj['main']['humidity']
        self.sunset = weather_obj['sys']['sunset']
        self.city = weather_obj['name']


  def _download_url(self, url_to_download: str) -> dict:
    '''
    Function definition to take the request string and attempt to connect with the API to gather data.
    '''
    response = None
    r_obj = None

    # Taking the URL and calling the API for the data.
    try:
        response = urllib.request.urlopen(url_to_download)
        json_results = response.read()
        r_obj = json.loads(json_results)

    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        self.error_code = e.code
        self.error_msg = e
        self.error = True
    except urllib.error.URLError as e:
        print('Loss of connection to Weather API')
        self.error_msg = e
        self.error = True
    finally:
        if response != None:
            response.close()

    return r_obj


  def set_apikey(self, apikey: str) -> None:
    '''
    Sets the apikey required to make requests to a web API.
    :param apikey: The apikey supplied by the API service
    
    '''
    self.apikey = apikey


  def transclude(self, message: str) -> str:
    '''
    Replaces keywords in a message with associated API data.
    :param message: The message to transclude
    
    :returns: The transcluded message
    '''

    if self.error == False:
        new_message = message.replace("@weather", f'{self.temperature} and {self.description} in {self.city}')
        return new_message
    else:
        if self.error_code == 403:
            return "Error Code 403: Invalid API Key."
        elif self.error_code == 404:
            return "Error Code 404: Invalid request."
        elif self.error_code == 503:
            return "Error Code 503: Server Down."
        return "Error in object, reinstantiate."
    return new_message
