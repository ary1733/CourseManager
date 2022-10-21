from flask import Flask, jsonify, redirect, url_for, g, render_template, session, request, flash, make_response
from APP.utils import query_db, get_db, SCHEMA, query_commit_db
import os
import datetime

# from flask_cors import CORS

# Main application and configuration
app = Flask(__name__)

# For Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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

@app.route('/addstudent', methods = ['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        data = request.json
        print(data)
        query_res = query_commit_db("""
        INSERT INTO Student (Roll_no, Student_name, Dept_Name, Email_Id)
        VALUES
        (?, ?, ?, ?)
        """,
        (data.get('Roll_no'), data.get('Student_name'), data.get('Dept_Name'), data.get('Email_Id'))
        ,
        True)
        return make_response(jsonify({"message": "success" if query_res == True else query_res}), 200)
    else:
        return render_template('addstudent.html')

@app.route('/addcourse', methods = ['GET', 'POST'])
def addcourse():
    if request.method == 'POST':
        data = request.json
        print(data)
        query_res = query_commit_db("""
        INSERT INTO Course (Course_cd, Course_name, Semester, Credits, Instructor_Name)
        VALUES
        (?, ?, ?, ?, ?)
        """,
        (data.get('Course_cd'), data.get('Course_name'), data.get('Semester'), data.get('Credits'), data.get('Instructor_Name'))
        ,
        True)
        return make_response(jsonify({"message": "success" if query_res == True else query_res}), 200)
    else:
        return render_template('addcourse.html')

@app.route('/addregistration', methods = ['GET', 'POST'])
def addregistration():
    if request.method == 'POST':
        data = request.json
        print(data)
        query_res = query_commit_db("""
        INSERT INTO Course_Student (Course_cd, Roll_no)
        VALUES
        (?, ?)
        """,
        (data.get('Course_cd'), data.get('Roll_no'),)
        ,
        True)
        print (query_res)
        return make_response(jsonify({"message": "success" if query_res == True else query_res}), 200)
    else:
        return render_template('addregistration.html')

@app.route('/showstudents')
def showstudents():
    search_query = request.args.get('searchQuery') if request.args.get('searchQuery') is not None else ""
    print(search_query)
    query_res = query_db('''
        SELECT * FROM Student NATURAL LEFT JOIN Course_Student NATURAL LEFT JOIN Course where Student_name Like ?;
    ''',
    ("%"+search_query+"%",)
    )
    g.isDataAvailable = len(query_res) > 0
    if(g.isDataAvailable):
        g.tableHeaders = query_res[0].keys()
        g.rows = [[row_dict[key] if row_dict[key] is not None else "Not Registered"for key in g.tableHeaders] for row_dict in query_res]
        print(g.tableHeaders)
        print(g.rows)
    return render_template('showstudents.html')
@app.route("/map")
def get_map():
    data={}
    for rule in app.url_map.iter_rules():
        try:
            data[str(rule.endpoint)]=str(url_for(rule.endpoint))
        except:
            pass
    return data
