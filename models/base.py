#!/usr/bin/env python

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel

class BaseNDBExpando(ndb.Expando):
    """
        This model defines the base of all the NDB Expando models
    """

    create_ts = ndb.DateTimeProperty(auto_now_add = True)
    change_ts = ndb.DateTimeProperty(auto_now = True)

    def to_dict(self, include = [], exclude = []):
        d = {}
        if len(exclude) != 0:
            d = super(BaseNDBExpando, self).to_dict(exclude = exclude)
        elif len(include) != 0:
            d = super(BaseNDBExpando, self).to_dict(include = include)
        elif len(include) == 0 and len(exclude) == 0:
            d = super(BaseNDBExpando, self).to_dict()
            
        # Add self object ID to the dict
        d['id']  = self.key.id()
        return d
