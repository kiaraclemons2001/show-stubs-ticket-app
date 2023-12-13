# Client-side program
# Authors: Kiara Clemons and Daniel Shafer

import socket
import input_validation
import getpass
import sys

# main_menu accepts input of numbers 1-7
welcome_message = "Welcome to Show Stubs\n"
menu = (
    "Please Choose from the Following Options\n"
    "1: Login\n"
    "2: Register\n"
    "3: Buy Tickets\n"
    "4: Add Points\n"
    "5: View Account\n"
    "6: View Events\n"
    "7: View Menu\n"
    "8: Logout\n"
    "9: exit\n"
)


# when called, function will establish connection to server, request input,
# send user input to server, and await response; when finished, loop for new input unless exit request
def connect_to_server():
  error_log = ""
  # user_input = ""
  # user_input_bytes = ""
  # flags set to catch special cases loop terminate and password entry
  working = True
  new_password_flag = False
  existing_password_flag = False
  server_name = "localhost"
  server_port = 12000
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.settimeout(5)
  # application will attempt to connect to the server, failure will throw a socket error exception
  try:
      client_socket.connect((server_name, server_port))
  except socket.error as err:
      error_statement = (
          "Trouble connecting to server. \nPlease ensure server is "
          "running before initiating client application.\n"
      )
      print(error_statement, "\n")
      err = str(err)
      # error will be logged and saved to an error file when connection is ended
      error_log = error_log + err + " " + error_statement + "\n"
      working = False
  while working:
      try:
          # application will accept any input to send to server, enter without input throws IO exception
          # user input is immediately converted to bytes for transmission through socket
          if new_password_flag or existing_password_flag:
              if sys.stdin.isatty():
                  user_input = getpass.getpass(prompt="--> ")
              else:
                  print("Using readline")
                  user_input = sys.stdin.readline().rstrip()
          else:
              user_input = input("--> ")


              # user_input_bytes = str.encode(user_input)
          # entry of exit option '9' sets working flag fto false, signaling app to close
          if user_input == '9':
              working = False

          # new password flag indicates that user is entering a new password, loop prints requirements
          # and calls input validation on password entry; the request loops until either requirements
          # are met or the user enters 'exit', which breaks the loop and returns the user to the menu

          elif new_password_flag:
              # app will attempt to call the password validation function, loop if the function does
              # not succeed, and throw a validation exception if the function cannot run.
              try:
                  while not input_validation.validate_password(user_input):
                      print(
                          "Password does not meet requirements "
                          "(minimum of 8 characters must include at least \n"
                          "one number, one uppercase letter, one lowercase letter, "
                          "and one special character)\n"
                          "Please input your password (type exit to return to menu)."
                      )
                      user_input = input("--> ")
                      if user_input == "exit":
                          break
              except input_validation.PasswordException as err:
                  error_statement = "Error while running function to validate password entry."
                  print(error_statement, "\n")
                  err = str(err)
                  error_log = error_log + err + " " + error_statement + "\n"
              # password must be converted to bytes before hashing
              password_input_bytes = str.encode(user_input)
              try:
                  user_input = input_validation.hash_password(password_input_bytes)
              except input_validation.HashingException as err:
                  error_statement = "Error while running function to hash password entry."
                  print(error_statement, "\n")
                  err = str(err)
                  error_log = error_log + err + " " + error_statement + "\n"
          elif existing_password_flag:
              password_input_bytes = str.encode(user_input)
              user_input = input_validation.hash_password(password_input_bytes)
          # send user input to server through defined socket
          try:
              if type(user_input) == str:
                  user_input_bytes = str.encode(user_input)
                  client_socket.send(user_input_bytes)
              else:
                  client_socket.send(user_input)
          except socket.error as err:
              error_statement = (
                  "Trouble sending message to server. \nPlease ensure server is "
                  "running before initiating client application.\n"
              )
              print(error_statement, "\n")
              err = str(err)
              # error will be logged and saved to an error file when connection is ended
              error_log = error_log + err + " " + error_statement + "\n"
          # receive response from server, convert from bytes to string for processing
          try:
              message_from_server_bytes = client_socket.recv(1024)
              message_from_server_string = bytes.decode(message_from_server_bytes)
              print(message_from_server_string)
              # if response from server is requesting a password, flag is set to loop back to input validation
              new_password_flag = True if message_from_server_string == "Please enter your new password:" else False
              existing_password_flag = True if message_from_server_string == "Please enter your password:" else False
          except socket.error as err:
              error_statement = (
                  "Trouble sending message to server. \nPlease ensure server is "
                  "running before initiating client application.\n"
              )
              print(error_statement, "\n")
              err = str(err)
              # error will be logged and saved to an error file when connection is ended
              error_log = error_log + err + " " + error_statement + "\n"
      # if the stated variable is unassigned or undefined
      except NameError as err:
          error_statement = "Name Error: variable unassigned or undefined."
          print(error_statement, "\n")
          err = str(err)
          error_log = error_log + err + " " + error_statement + "\n"
      # if the operation cannot be completed with stated value types
      except TypeError as err :
          error_statement = "Type Error: operation can't be performed with attempted types."
          print(error_statement, "\n")
          err = str(err)
          error_log = error_log + err + " " + error_statement + "\n"
      # if the user inputs a value that won't work with function
      except ValueError as err:
          error_statement = "Value Error: function unable to operate with entered value."
          print(error_statement, "\n")
          err = str(err)
          error_log = error_log + err + " " + error_statement + "\n"
      # if the user hits enter without input, will trigger IO exception
      except IOError:
          print("Input Error: you must enter a valid option to proceed.\n")
          print(menu + "\n")
  # close the socket and write errors to file before application ends
  client_socket.close()
  with open('client_errors.txt', 'w') as f:
      f.write(error_log)


# run program
print(welcome_message)
print(menu)
connect_to_server()