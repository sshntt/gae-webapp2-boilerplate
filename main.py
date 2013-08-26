#!/usr/bin/env python

import webapp2

# Application Imports
import routes
from appglobals import AUTH_CONFIG

# Handler Imports
from handlers import error_handlers

# Define app
app = webapp2.WSGIApplication(config = AUTH_CONFIG, debug = True)

# Add defined routes
routes.add_routes(app)

# Define error handlers
app.error_handlers[404] = error_handlers.handle_404
app.error_handlers[500] = error_handlers.handle_500
