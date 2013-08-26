#!/usr/bin/env python

import logging

def handle_404(request, response, exception):
    logging.error(exception)
    response.write("Sorry, the princess is in another castle !")
    response.set_status(404)

def handle_500(request, response, exception):
    logging.error(exception)
    response.write("Do you want to know how I got these scars ?!?!")
    response.set_status(500)
