from flask import Flask, jsonify, redirect, url_for, g, render_template, session, request, flash, make_response
from APP.utils import query_db, get_db, SCHEMA, query_commit_db
import os
import datetime

# from flask_cors import CORS

# Main application and configuration
app = Flask(__name__)

# For Session
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = "SomethingReallySecret"
app.config['SESSION_TYPE'] = 'memcached'

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    value = datetime.datetime.fromisoformat(value)
    return value.strftime(format)

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index(queryInfo = None):
    return render_template('index.html')

@app.route("/map")
def get_map():
    data={}
    for rule in app.url_map.iter_rules():
        try:
            data[str(rule.endpoint)]=str(url_for(rule.endpoint))
        except:
            pass
    return data
