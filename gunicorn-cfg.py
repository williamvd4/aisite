# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

bind = '127.0.0.1:5005' # Use the loopback address instead of 0.0.0.0 for better security
workers = 2 # Increase the number of workers to improve performance
accesslog = '-'
loglevel = 'info' # Set log level to info for less verbose output
capture_output = False # Disable output capture for better error reporting
# disable_stdio_inheritance = True # Uncomment this line if you're using Gunicorn with a systemd systemd service
