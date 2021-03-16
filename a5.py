from Profile import Profile, Post
from pathlib import Path
from ds_client import send
from collections import namedtuple
import json
import os
from LastFM import LastFM
from OpenWeather import OpenWeather
from ExtraCreditAPI import ExtraCredit
from NaClProfile import NaClProfile

search_list = []

DataTuple = namedtuple(
    'DataTuple', ["entry", "timestamp"])

print(
    '''
How To Use This Program:
------------------------
Command List:
Q - Quits the program / Saves profile files.
L - List the contents of the specified directory. Format: L path extension
   - Extensions: 
       -r Output directory content recursively.
       -f Output only files, excluding directories in the results.
       -s Output only files that match a given file name.
       -e Output only files that match a give file extension. Must specify extension type. Ex. png, txt.
C - Creates a new DSU file, Format: C file_path -n filename
D - Deletes DSU files present on machine, Format: D filepath
R - Prints out a file to view in command line: Format: R filepath
O - Loads DSU profile to send messages to the DSU server, Format: O file_path
'''
)

def keyword_search(message: str) -> str:
  '''
  This function looks for keywords in the message string before it is sent to the DSU server and makes instantiates and checks class variables. 
  '''
  if "@weather" in message:
    open_weather = OpenWeather(str(input("Type in Zipcode: \n")), str(input(
        "Type in country code: \n")), "3dbc2e95e625a20ea0fa40e84dbf61de")
    if open_weather.error == False:
      message = open_weather.transclude(message)
    else:
      print("Something went wrong with the Weather API, try inputting valid Zip and Country Codes.")
      return False

  if "@lastfm" in message:
    last_fm = LastFM("34af4a7362d174fc5780583f343a1f65")
    if last_fm.error == False:
      message = last_fm.transclude(message)
    else:
      print("Something went wrong with the Last FM API, try again.")
      return False


  if "@extracredit" in message:
    extra_credit = ExtraCredit()
    if extra_credit.error == False:
      message = extra_credit.transclude(message)
    else:
      print("Something went wrong with the Extra Credit API, try again.")
      return False


  return message


def extract_json_post(json_msg: str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    entry = json_obj['post']['entry']
    timestamp = json_obj['post']['timestamp']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(entry, timestamp)


def basic_L(path, control = False, search = ''):
  file_names = []
  dir_names = []

  for o in path.iterdir():
      if o.is_file():
        file_names.append(o)
      else:
        dir_names.append(o)

  if control == 'b':
    for files in file_names:
      print(files)
    for dirs in dir_names:
      print(dirs)

  if control == '-f':
    for files in file_names:
      print(files)
    return dir_names

  if control == '-s':
    for files in file_names:
      if os.path.basename(files) == search:
        print(files)
  
  if control == '-e':
    for files in file_names:
      extension = os.path.basename(files).split(".")[1]
      if extension == search:
        print(files)


def filter_function(path, code = True):
  if code:
    print(path)
  for chain in path.iterdir():
    if chain.is_file():
      print(chain)
    else:
      filter_function(chain)
  

def recursive_files(path, control = False, search = ''):
  file_names = []
  dir_names = []
  
  for o in path.iterdir():
    if o.is_file():
      file_names.append(o)
    else:
      dir_names.append(o)
      new_path = path / o
      recursive_files(new_path, control, search)
  
  if control == 'b':
    basic_L(path, '-f')

  if control == '-f':
    print(file_names)
    for files in file_names.reverse():
      print(files)
  
  if control == '-s':
    for files in file_names:
      if os.path.basename(files) == search:
        search_list.append(files)
    return search_list

  
  if control == '-e':
    for files in file_names:
      extension = os.path.basename(files).split(".")[1]
      if extension == search:
        print(files)


def run():
  user_profile = False
  user_path = False
  
  while True:
    command_list = []
    user_command = input()

    if user_command == "Q":
      # if the user has a profile loaded and a path on deck, it should save thier profile to that selected path.
      if user_profile and user_path:
        user_profile.save_profile(user_path)
        print("successfully saved profile to DSU")
      return

    if len(user_command) < 2:
      print("ERROR CHARACTER Length")
      continue

    user_command = user_command.strip()
    user_command = user_command.split(" ")

    if len(user_command) < 2:
      print("ERROR COMMAND LENGTH")
      continue

    if user_command[0] not in ("L", "C", "D", "R", "O"):
      print("ERROR COMMAND NOT KNOWN")
      continue

    for commands in user_command:
      if commands[0] == '-':
        command_list.append(commands)

    if user_command[0] == "C":
      p = Path(user_command[1])
      if p.exists:

        if len(command_list) == 0:
          print("ERROR -n NOT PRESENT")
          pass

        if len(command_list) == 1:
          if '-n' in command_list:
            file_name = user_command[3] + ".dsu"
            user_file = p / file_name
            user_path = user_file
            w = user_file.open('w')
            w.close()
            print(user_file)

            while True:
              print(user_profile)
              user_name = str(input("What is your username? \n"))
              pass_word = str(input("What is your password? \n"))
              server_address = str(input("What is the server address you would like to connect to? \n"))
              user_profile = NaClProfile()
              user_profile.dsuserver = server_address
              user_profile.username = user_name
              user_profile.password = pass_word
              user_profile.generate_keypair()
              bio = input("Would you like to add a bio? Y / N \n")
              if bio == ('Y'):
                user_bio = str(input("Type bio: \n"))
                user_profile.bio = user_bio
              print("To save {}'s profile, quit the application using Q.".format(user_profile.username))
              break
              
      else:
        print("ERROR PATH NOT RECOGNIZED")

    if user_command[0] == "D":
      p = Path(user_command[1])
      extension = os.path.basename(p).split(".")[1]
      if p.exists() and extension == 'dsu':
        os.remove(p)
        print(p, "DELETED")
      else:
        print('ERROR PATH NOT RECOGNIZED')

    if user_command[0] == "R":
      p = Path(user_command[1])
      extension = os.path.basename(p).split(".")[1]
      if p.exists() and extension == 'dsu':
        r = p.open('r')
        contents = r.readlines()
        if len(contents) == int(0):
          print('EMPTY')
        else:
          for lines in contents:
            print(lines)
        r.close()
      else:
        print('ERROR PATH NOT RECOGNIZED')

    if user_command[0] == "O":
      '''
      O is used to load a profile onto memory then ask the user what they want to do with that profile and if they would like to send a message to the server.
      '''
      p = Path(user_command[1])
      extension = os.path.basename(p).split(".")[1]
      if p.exists() and extension == 'dsu':
        user_profile = NaClProfile()
        user_profile.load_profile(p)
        print("successfully loaded {}'s profile".format(user_profile.username))
        print('''
        Messaging the DSU server has support for keywords.
        - @lastfm: Prints a random artist from today's charts.
        - @weather: Gives weather description for a given ZIP and Country Code.
        - @extracredit: Prints a random name of the iss crew members.
        ''')

        while True:
          client_message = str(input("Type the message you would like to send to the DSU server. \n"))

          client_message = keyword_search(client_message)

          if client_message != False:
            break

        print("attempting to connect to server...")

        user_post = send(user_profile.dsuserver, 2021, user_profile.username, user_profile.password, client_message, user_profile.keypair, user_profile.bio)

        try:
          user_post = extract_json_post(user_post)
        except TypeError:
          pass
        else:
          # post_entry = user_profile.encrypt_entry(client_message, user_profile.public_key)
          # post_entry = post_entry.decode(encoding='UTF-8')
          # print(post_entry, "<--- CLient encryption")
          # print(user_post.entry, "<--- Server encryption")
          new_post = Post(client_message, user_post.timestamp)
          user_profile.add_post(new_post)
          user_profile.save_profile(p)
          print("successfully saved post to DSU")
          print("Post:", client_message)
          print("To create another post, use the O command again. If not feel free to use any other program commands.")

      else:
        print('ERROR PATH NOT RECOGNIZED')

    if user_command[0] == "L":
      p = Path(user_command[1])

      if p.exists:
        if len(command_list) == 0:
          basic_L(p, 'b')

        if len(command_list) == 1:
          if '-r' in command_list:
            dirs = basic_L(p, '-f')

            for direc in dirs:
              filter_function(direc)

          if '-f' in command_list:
            basic_L(p, '-f')
          if '-s' in command_list:
            search = user_command[3]
            basic_L(p, '-s', search)
          if '-e' in command_list:
            search = user_command[3]
            basic_L(p, '-e', search)
          
        if len(command_list) == 2:
          if '-r' and '-f' in command_list:
            dirs = basic_L(p, '-f')
            for direc in dirs:
              filter_function(direc, False)

          if '-r' and '-s' in command_list:
            search = user_command[4]
            list = recursive_files(p, '-s', search)
            for files in list[::-1]:
              print(files)
            search_list.clear()
          
          if '-r' and '-e' in command_list:
            search = user_command[4]
            recursive_files(p, '-e', search)
      else:
        print("ERROR PATH NOT RECOGNIZED")


if __name__ == "__main__":
  run()
