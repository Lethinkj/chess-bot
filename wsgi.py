"""
WSGI configuration for PythonAnywhere deployment
Do not modify unless you know what you're doing
"""

import sys
import os

# Add the directory containing app.py to the Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
