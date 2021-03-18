from NaClProfile import NaClProfile
from ds_client import send
import ds_protocol
import socket
import time

class CustomError(Exception):
    pass



class TCPClient():

    def __init__(self, host, port, retryAttempts=10):
        #this is the constructor that takes in host and port. retryAttempts is given
        # a default value but can also be fed in.
        self.host = host
        self.port = port
        self.retryAttempts = retryAttempts
        self.socket = None

    def connect(self, attempt=0):
      try:
        self.socket = socket.socket()
        self.socket.connect((self.port, self.host))
      except:
        print("err")

    def diconnectSocket(self):
        #perform all breakdown operations
        self.socket.close()
        self.socket = None
        pass

    def sendDataToDB(self, data):
      send = self.socket.makefile('w')
      recv = self.socket.makefile('r')
      send.write(data)
      send.flush()
      srv_msg = recv.readline()
      server_response = ds_protocol.extract_json(srv_msg)
      return server_response

    def readData(self, data):
        #read data here
        if data.type == "error":
          print("error")
        elif data.type == "ok":
          if data.server_message == "Direct message sent":
            print("MESSAGE SUCCESSFULLY SENT!")
            return True
          if type(data.server_message) == list:
            print("LIST SUCCESSFULLY RETRIEVED!")
            return data.server_message


class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None

    self.user = NaClProfile()
    self.user.generate_keypair()
    self.token = self.user.public_key
    self.user.dsuserver = dsuserver
    if dsuserver == None:
      self.user.dsuserver = "168.235.86.101"
    self.user.username = username
    self.user.password = password
    

  def send(self, message: str, recipient: str) -> bool:
    # returns true if message successfully sent, false if send failed.
    if self.token is not None:

      client = TCPClient(2021, self.user.dsuserver)
      client.connect()

      response = client.sendDataToDB(ds_protocol.join(str(self.user.username), str(self.user.password), self.token))
      client.readData(response)

      response = client.sendDataToDB(send_msg(self.token, message, recipient))
      server_data = client.readData(response)

      if server_data == True:
        client.diconnectSocket()
        return server_data
      else:
        #handle errors
        pass

      client.diconnectSocket()


  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    client = TCPClient(2021, self.user.dsuserver)
    client.connect()

    response = client.sendDataToDB(ds_protocol.join(str(self.user.username), str(self.user.password), self.token))
    client.readData(response)

    response = client.sendDataToDB(retrive_msg(self.token, "new"))
    server_data = client.readData(response)
    # change to direct_message

    if type(server_data) == list:
      client.diconnectSocket()
      return server_data
    client.diconnectSocket()


  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    client = TCPClient(2021, self.user.dsuserver)
    client.connect()

    response = client.sendDataToDB(ds_protocol.join(str(self.user.username), str(self.user.password), self.token))
    client.readData(response)

    response = client.sendDataToDB(retrive_msg(self.token, "all"))
    server_data = client.readData(response)

    print('DEBUG', server_data)
    expected_ = ['message','from','timestamp']
    direct_message_list = []

    # check if server_data exists before creating direct messages
    if server_data != None:
        for dict_ in server_data:
            if list(dict_.keys()) == expected_:
                message_creator = DirectMessage()
                message_creator.recipient = dict_['from']
                message_creator.message = dict_['message']
                message_creator.timestamp = dict_['timestamp']

                direct_message_list.append(message_creator)
            else:
                pass
                # maybe exception? idk if its possible to get wrong key values from server
        print('DEBUG', direct_message_list.__str__)
    
        if type(direct_message_list) == list:
          client.diconnectSocket()
          return direct_message_list
  
    client.diconnectSocket()
  

def send_msg(user_token: str, entry: str, recipient :str) -> str:
  '''
  Change the username and password into a json format to connect to server.
  '''
  direct_msg = '{"token":"'+ user_token +'", "directmessage": {"entry": "'+ entry +'","recipient": "'+ recipient +'", "timestamp": "' + str(time.time()) + '"}}'

  return direct_msg

def retrive_msg(user_token: str, pull_type: str) -> str:
  '''
  Change the username and password into a json format to connect to server.
  '''
  if pull_type in ("new", "all"):
    retrieve_msg = '{"token":"'+ user_token +'", "directmessage": "'+ pull_type +'"}'
    return retrieve_msg
  else:
    return None


if __name__ == "__main__":

  messenger = DirectMessenger(dsuserver=None, username="hegel", password="xxx@")
  messenger1 = DirectMessenger(dsuserver=None, username="hegelhater", password="xxxB")

  print(messenger.send("no ur not", "unique username"), "<--- Send function @ self 1")
  print(messenger.retrieve_new(), "<---- Retrievecould New Function mango")

  print(messenger1.send("whats konpeko | hegels my bitch u cant have him", "Team No Name"), "<--- Send function @ Team No Name 2")
  print(messenger1.send("shut ur encrypted ass up", "Rosie"), "<--- Send function @ Rosie 3")
  
  print(messenger.send("name2r", "thisismyusername25"), "<--- Send function @ thisismyusername25 1")
  print(messenger.send("u are <but a position vector>", "thisismyusername25"), "<--- Send function @ thisismyusername25 2")

  print(messenger.retrieve_new(), "<---- Retrievecould New Function mango")
  print(messenger.retrieve_all(), "<---- Retrieve All Function")

  print(messenger1.retrieve_new(), "<---- Retrievecould New Function grog")
  print(messenger1.retrieve_all(), "<---- Retrieve All Function")


  # try:
  #   data = client.readData(response)
  # except CustomError:
  #   do something in GUI
