#!/usr/bin/env python

import os
import webapp2
import logging

from webapp2_extras import jinja2
from webapp2_extras import sessions
from webapp2_extras import auth


# Configured so that uri_for can be used in JINJA templates
def jinja2_factory(app):
    j = jinja2.Jinja2(app)
    j.environment.globals.update({
        'uri_for': webapp2.uri_for,
    })

    return j


class BaseHandler(webapp2.RequestHandler):
    """
        This class defines a base handler for all the request handlers
        and eases the use of jinja2 templates
    """

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(factory = jinja2_factory)

    def render_template(self, filename, **template_args):
        self.response.write(self.jinja2.render_template(filename, **template_args))


class UserSessionHandler(BaseHandler):
    """
        This class defines a user session aware base handler
    """

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def user_model(self):
        return self.auth.store.user_model

    @webapp2.cached_property
    def user_session_info(self):
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user_db_info(self):
        u = self.user_session_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(backend="datastore")

    def dispatch(self):
        # Get a session store for this request
        self.session_store = sessions.get_store(request = self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save the session
            self.session_store.save_sessions(self.response)


def login_required(handler):
    """
        Decorator that checks if there's a user associated with the current session.
        Will also fail if there's no session present.
    """
    def check_login(self, *args, **kwargs):
        if not self.auth.get_user_by_session():
            self.redirect(webapp2.uri_for('login_uri'))
        else:
            return handler(self, *args, **kwargs)

    return check_login
