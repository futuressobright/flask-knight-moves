# app/__init__.py

from flask import Flask


app = Flask(__name__)
app.jinja_env.cache = {}
app.secret_key = 'supersecretkey'

from app import routes
