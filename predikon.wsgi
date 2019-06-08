#!/usr/bin/env python

import os
import sys

from predikonwbap import app

# Redirect output to apache logs.
sys.stdout = sys.stderr


def application(environ, start_response):
    # Set general environment variable from Apache SetEnv directive.
    os.environ['PREDIKON_DB'] = environ['PREDIKON_DB']

    return app(environ, start_response)
