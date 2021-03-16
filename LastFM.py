# UTF-8
import json
import urllib
from urllib import request, error
from random import randint

class LastFM:
  def __init__(self, apikey: str):
    self.error = False
    self.error_code = None
    artist_obj = None
    self.apikey = None
    # Try exept statement making sure the API is of type String.
    try:
        assert isinstance(apikey, str)
    except AssertionError:
        print("Invalid API key: Must be of type string")
        self.error = True
    else:
        self.apikey = apikey.replace(" ", '')
    
    # Artist list to append to after data is recieved from API.
    self.artist_list = []
    url = "http://ws.audioscrobbler.com/2.0/"
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64'
    API_KEY = '34af4a7362d174fc5780583f343a1f65'
    headers = {'User-Agent': USER_AGENT}

    # If an apikey is present, create the request schema to send to API
    if apikey != None:
      payload = {
          'api_key': self.apikey,
          'method': 'chart.getTopArtists',
          'format': 'json'
      }

      data = urllib.parse.urlencode(payload)
      data = data.encode('utf-8')
      # API Request
      request = urllib.request.Request(url, data, headers)
    else:
      return

    # If there is an error in the instantiated object, do not try and get the API data.
    if self.error == False:
      artist_obj = self._download_url(request)

      if artist_obj != None:
        for artist in artist_obj['artists']['artist']:
          self.artist_list.append(artist['name'])

  def _download_url(self, request_str: str) -> dict:
    '''
    Function definition to take the request string and attempt to connect with the API to gather data.
    '''
    response = None
    data_object = None

    # Try pinging the response to the API and if there are any errors make note of them. 
    try:
      response = urllib.request.urlopen(request_str)
      data_object = json.loads(response.read())
    except urllib.error.HTTPError as e:
      print('Failed to download contents of URL')
      print('Status code: {}'.format(e.code))
      self.error_code = e.code
      self.error = True
      data_object = None
    except urllib.error.URLError:
      print("Connection could not be made to lastFM server.")
      data_object = None
      self.error = True
    finally:
      if response != None:
          response.close()

    return data_object

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
    # If there is an error in the present object, do not transclude as there will be errors in the data gathering. Instead return text of the error. (Does not send this to server only is used for professor code check.)
    if self.error == False:
        new_message = message.replace(
            "@lastfm", self.artist_list[randint(0, 50)])
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
