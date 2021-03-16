import socket
import json
import ds_protocol
from ds_protocol import extract_json
from NaClProfile import NaClProfile


def send(server: str, port: int, username: str, password: str, message: str, keypair: str, bio: str = None,):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  public_key = keypair[:44]
  private_key = keypair[44:]
  keypair = keypair
  # Try statements to work out the possible errors in the port and host variables.
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      try:
        client.connect((str(server), int(port)))
      except socket.gaierror:
        print("Host name invalid")
      except ConnectionRefusedError:
        print("Connection to host machine was refused.")
      except ValueError:
        print("Server or server port was given wrong data value")
      except TypeError:
        print("Server or server port was given wrong datatype")
        # If the connection is made and there is no errors in datatypes or values, the code will continue to run.
      else:
        send = client.makefile('w')
        recv = client.makefile('r')

        print("client connected to {} on {}\n".format(server, port))

        # Attempts to join the server with the username, password, and server address
        send.write(ds_protocol.join(str(username), str(password), public_key))
        send.flush()
        srv_msg = recv.readline()
        server_response = extract_json(srv_msg)
        print(server_response.server_message)
        # If there is an error the protocol will print the error and let the user know that the join command was the one causing issues.
        if ds_protocol.response(srv_msg) == "error":
          print("Something went wrong joining server.")
        else:
          server_key = ds_protocol.response(srv_msg)
          # Attemps to post the user's message to the site
          encoder = NaClProfile()
          encoder.import_keypair(keypair)
          message = encoder.encrypt_entry(message, server_key)
          if message != False:
            encrypted_message = message.decode(encoding='UTF-8')
            user_post = ds_protocol.post(str(public_key), encrypted_message)
            send.write(user_post)
            send.flush()
            srv_msg = recv.readline()
            if ds_protocol.response(srv_msg) == "error":
              print("Something went wrong posting message.")

          # If the bio exists in the parameters then overwrite what is set for bio on the website.
          if bio not in ("", None):
            bio = encoder.encrypt_entry(bio, server_key)
            if bio != False:
              encrypted_bio = bio.decode(encoding='UTF-8')
              send.write(ds_protocol.bio(str(public_key), encrypted_bio))
              send.flush()

              srv_msg = recv.readline()
              if ds_protocol.response(srv_msg) == "error":
                print("Something went wrong updating bio.")
        try:
          return user_post
        except UnboundLocalError:
          print("Message could not be sent to server.")
  except TimeoutError:
    print("Could not connect to the server, see server info for errors.")
