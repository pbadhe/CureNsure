import logging
import bcrypt

def encrypt(inputPassword):
    return bcrypt.hashpw(inputPassword.encode('utf-8'), bcrypt.gensalt(10)) 

def checkPassword(inputPassword, hashed):
    if bcrypt.checkpw(inputPassword.encode('utf-8'), hashed):
        logging.debug("login success")
        return True
    else:
        logging.debug("incorrect password")
        return False

