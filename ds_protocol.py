import json
from collections import namedtuple
from Profile import Post
import time

# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['response', 'type', "server_message", "token"])

def extract_json(json_msg: str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    try:
      token = json_obj['response']['token']
    except KeyError:
      token = ''
    response = json_obj['response']
    type = json_obj['response']['type']
    server_message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
  except KeyError:
    server_message = json_obj['response']['messages']

  return DataTuple(response, type, server_message, token)


def join(username: str, password: str, public_key:str) -> str:
  '''
  Change the username and password into a json format to connect to server.
  '''
  join_msg = '{"join": {"username": "' + username + '", "password": "' + password + '", "token": "' + public_key + '"}}'
  return join_msg


def post(user_token: str, user_message: str) -> str:
  '''
  Use user token and user message and formats into json to be used by server.
  '''
  post_msg = '{"token": "' + user_token + '", "post": {"entry": "' + user_message + '", "timestamp": "' + str(time.time()) + '"}}'
  return post_msg


def bio(user_token: str, user_bio: str) -> str:
  '''
  Takes in user token and user bio and formats into json readable by the server.
  '''
  bio_msg = '{"token": "' + user_token + '", "bio": {"entry": "' + user_bio + '", "timestamp": "' + str(time.time()) + '"}}'
  return bio_msg


def response(server_message: json) -> str:
  '''
  Takes the json response from the server, extracts it and deals with it by either letting the user know there was an error or returns the token to use for the rest of the functions.
  '''
  server_response = extract_json(server_message)
  if server_response.type == "error":
    print(server_response.server_message)
    return "error"
  elif server_response.type == "ok":
    user_token = server_response.token
    return user_token
