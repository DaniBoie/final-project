import urllib
import json
from urllib import request, error
from random import randint


class ExtraCredit:
  def __init__(self):
    url = "http://api.open-notify.org/astros.json"
    self.error = False
    self.error_code = None
    self.crew_names = []


    # If there is an error in the instantiated object, do not try and get the API data.
    if self.error == False:
      try:
        iss_obj = self._download_url(url)
      except:
        self.error = True
      else:
        for crew in iss_obj['people']:
          self.crew_names.append(crew['name'])


  def _download_url(self, request_str: str) -> dict:
    '''
    Function definition to take the request string and attempt to connect with the API to gather data.
    '''
    response = None
    r_obj = None

    # Try pinging the response to the API and if there are any errors make note of them.
    try:
      response = urllib.request.urlopen(request_str)
      json_results = response.read()
      text = json_results.decode(encoding='utf-8')
      r_obj = json.loads(text)
    except urllib.error.HTTPError as e:
      print('Failed to download contents of URL')
      print('Status code: {}'.format(e.code))
      self.error_code = e.code
      self.error = True
      r_obj = None
    except urllib.error.URLError:
      print("Connection could not be made to ISS API server.")
      r_obj = None
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
    # If there is an error in the present object, do not transclude as there will be errors in the data gathering. Instead return text of the error. (Does not send this to server only is used for professor code check.)
    if self.error == False:
        new_message = message.replace(
            "@extracredit", self.crew_names[randint(0, len(self.crew_names) - 1)])
        return new_message
    else:
      if self.error_code == 403:
        return "Error Code 403: Invalid API Key."
      elif self.error_code == 404:
        return "Error Code 404: Invalid request."
      return "Error in object, reinstantiate."
    return new_message
