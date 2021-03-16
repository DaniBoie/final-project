from NaClProfile import NaClProfile
from ds_client import send
import ds_protocol
import socket
import time

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None


  def send(self, message: str, recipient: str) -> bool:
    # returns true if message successfully sent, false if send failed.
    if self.token is not None:
      pass
    pass

  def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
    pass

  def retrieve_all(self) -> list:
    # returns a list of DirectMessage objects containing all messages
    pass
  

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

  user = NaClProfile()
  user.generate_keypair()
  user.dsuserver = "168.235.86.101"
  user.username = "Mango15"
  user.password = "1234"

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((user.dsuserver, 2021))

    send = client.makefile('w')
    recv = client.makefile('r')
    print("client connected to {} on {}\n".format(user.dsuserver, "2021"))

    # Send Join Message to Join the Server 
    print(user.public_key)
    send.write(ds_protocol.join(str(user.username), str(user.password), user.public_key))
    send.flush()
    srv_msg = recv.readline()
    server_response = ds_protocol.extract_json(srv_msg)
    server_token = server_response.token
    print(server_response)

    # Send Message to User using thier key, a message, and the other user's names.
    send.write(send_msg(user.public_key, "message I want to send", "Mango15"))
    send.flush()
    srv_msg = recv.readline()
    server_response = ds_protocol.extract_json(srv_msg)
    server_token = server_response.token
    print(server_response)

    # Grabs the user's new messages that came to thier account.
    send.write(retrive_msg(user.public_key, "new"))
    send.flush()
    srv_msg = recv.readline()
    server_response = ds_protocol.extract_json(srv_msg)
    server_token = server_response.token
    print(server_response)

    # Grabs all records of message history.
    send.write(retrive_msg(user.public_key, "all"))
    send.flush()
    srv_msg = recv.readline()
    server_response = ds_protocol.extract_json(srv_msg)
    server_token = server_response.token
    print(server_response)





  # messenger = DirectMessenger(ip_address, "Waldo", "1234")

  # "hey you wanna send a message to someone, go ahead."

  # messenger.send()

# what does it mean to be encrypted?


