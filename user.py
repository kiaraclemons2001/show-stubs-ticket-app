class User:
  # attributes (nouns)
  userFirstName = "blankFirstName"
  userLastName = "blankLastName"
  userID = 0
  username = "defaultUserName"
  userPassword = "defaultPassword"
  userPoints = 100
  loginFlag = False
  addedPoints=5

  # constructor
  def __init__(self, username, password):
      self.username = username
      self.userPassword = password

  # * methods (verbs)

  def get_full_name(self):
      return self.userLastName + ", " + self.userFirstName

  def subtract_points(self, debit):
      self.userPoints -= debit

  def add_points(self, credit):
      self.userPoints += credit

  def view_user(self):
      user_summary = (
          "User Full Name: ", self.get_full_name(), "\n",
          "Username: ", self.username, "\n",
          "User ID: ", self.userID, "\n",
          "User Points: ", self.userPoints, "\n"
      )
      return user_summary

  # def addUser():
  #
  # def delete_user():
  #
  # def generate_userID():
  #
  # def view_transactions():
  #
  # def view_tickets():
