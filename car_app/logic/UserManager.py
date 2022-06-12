from flask.wrappers import Request
from car_app.database.exceptions.MailError import MailError
import car_app.database.DBManager as dbm 
import car_app.database.models.User as us
from flask import request
import hashlib, binascii, os
import re

class UserManager:
    
    @staticmethod
    def find_user_for_username(username):
        with dbm.DBManager.session() as session:
            return session.query(us.User).filter(us.User.username==username).first()
    
    @staticmethod
    def find_user_for_email(email):
        with dbm.DBManager.session() as session:
            return session.query(us.User).filter(us.User.email==email).first()
        
    @staticmethod
    def create_hashed_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii') 
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        self.password = (salt + pwdhash).decode('ascii')
        
    @staticmethod
    def checking_mail(email):
        pattern = re.compile(".+@.+\..+")
        if pattern.match(email) != None:
            return True
        else:
            raise MailError()