# input validation module
# determines acceptable input and manages hashing

import hashlib


# custom exception to handle password errors
class PasswordException(Exception):
    """Password validation could not be completed on the user submitted string"""
    pass


# custom exception to handle password errors
class HashingException(Exception):
    """Password hashing could not be completed on the user submitted string"""
    pass


# checks number and type of characters in username against requirements
def validate_username(username):
    count_chars = len(username)
    char_req = True if count_chars >= 7 else False
    special_char_req = True if username.isalnum() else False
    return True if char_req and special_char_req else False


# checks number and type of characters in password against minimum requirements
def validate_password(password):
    count_chars = len(password)
    count_upper = sum(1 for c in password if c.isupper())
    count_lower = sum(1 for c in password if c.islower())
    count_number = sum(1 for c in password if c.isdigit())
    char_req = True if count_chars >= 7 else False
    upper_lower_req = True if count_upper >= 1 and count_lower >= 1 else False
    number_req = True if count_number >= 1 else False
    special_char_req = True if not password.isalnum() else False
    return True if char_req and upper_lower_req and number_req and special_char_req else False


# handles the encryption of password using SHA256 and returns password hash
def hash_password(password):
    h = hashlib.new("SHA256")
    h.update(password)
    password_hash = h.hexdigest()
    return str.encode(password_hash)