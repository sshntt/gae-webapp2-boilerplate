#!/usr/bin/env python

# Python Imports
import time
import webapp2

# Google Imports
from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from webapp2_extras import security

# Application Imports
from models.base import BaseNDBExpando

class MyDefinedUser(User):
    """
        This models defines the custom User entity
    """
    
    # Unique Properties
    email = ndb.StringProperty(required = True)
    # auth_id = 'auth:email'

    name = ndb.StringProperty(required = True)
    activated = ndb.BooleanProperty(required = True)
    activation_token = ndb.StringProperty()
    
    # Authorization Properties
    is_admin = ndb.BooleanProperty(required = True)

    # Authentication Properties
    password = ndb.StringProperty(required = True)
    reset_token = ndb.StringProperty()

    create_ts = ndb.DateTimeProperty(auto_now_add = True)
    change_ts = ndb.DateTimeProperty(auto_now = True)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject = 'auth'):
        """
            Returns a MyDefinedUser object based on user_id and a token
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

    @classmethod
    def get_by_email_query(cls, email):
        return cls.query(cls.email == email)

    def set_password(self, raw_password):
        """
            Sets the password for current user
        """
        self.password = security.generate_password_hash(raw_password, length = 12)
    

