#!/usr/bin/env python

# This file contains global variables for the project. 
# All variables names must be in UPPER CASE

# Session, User, Auth config
from models.user import MyDefinedUser

AUTH_CONFIG = {
    'webapp2_extras.sessions': {'secret_key': 'somethingreallysecret'},
    'webapp2_extras.auth': {'user_model': MyDefinedUser, 
                    'user_attributes': ['name',
                                        'email',
                                        'activated',
                                        'is_admin'
                                    ]
                }
}

## ENVIRONMENT DETAILS
IS_PROD_ENV = True
