"""
This python fule contains a Flaks application instances 
"""

from flask import Flask

app = Flask(__name__)

from app import routes 