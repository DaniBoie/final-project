from NaClProfile import NaClProfile
from ds_client import send
import ds_protocol
import socket
import time


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

    if type(server_data) == list:
      client.diconnectSocket()
      return server_data
  
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

  messenger = DirectMessenger(dsuserver=None, username="Marco55", password="1234")

  print(messenger.send("You are siccx", "Mango15"), "<--- Send function")

  print(messenger.retrieve_new(), "<---- Retrieve New Function")

  print(messenger.retrieve_all(), "<---- Retrieve All Function")

  # try:
  #   data = client.readData(response)
  # except CustomError:
  #   do something in GUI

