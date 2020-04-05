import sqlite3
import requests
from flask import Flask, session, redirect, url_for, escape, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key = 'Sood1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)

@app.route('/')
def root():
    # tells Flask to render the HTML page called login.html
	return render_template('login.html')

@app.route('/login.html')
def login():
    # tells Flask to render the HTML page called login.html
	return render_template('login.html')

@app.route('/login_i.html')
def login_i():
    # tells Flask to render the HTML page called login_i.html
	return render_template('login_i.html')

@app.route('/loginforminstructor', methods=['GET','POST'])
def check_data_instructor():
    if request.method == 'POST':
        utorid = str(request.form['LoginID'])
        pw = str(request.form['Password'])
        if utorid in session:
            session['utorid'] = utorid
            return render_template('index_i.html')
        else:
            sql = """ SELECT * FROM  accounts WHERE type = 'instructor' """
            accs = db.engine.execute(text(sql))
            for acc in accs:
                if acc['UtorID'] == utorid and acc['Password'] == pw:
                    session['user'] = utorid
                    session['name'] = acc['Name']
                    return render_template('index_i.html')
            else:
                flash("Unidentified Username or Password for Instructor!")
                return render_template('login_i.html')


@app.route('/login_s.html')
def login_s():
    # tells Flask to render the HTML page called login_s.html
	return render_template('login_s.html')

@app.route('/loginformstudent', methods=['GET','POST'])
def check_data_student():
    if request.method == 'POST':
        utorid = str(request.form['LoginID'])
        pw = str(request.form['Password'])
        if utorid in session:
            session['utorid'] = utorid
            return render_template('index_s.html')
        else:
            sql = """ SELECT * FROM  accounts WHERE type = 'student' """
            accs = db.engine.execute(text(sql))
            for acc in accs:
                if acc['UtorID'] == utorid and acc['Password'] == pw:
                    session['user'] = utorid
                    session['name'] = acc['Name']
                    return render_template('index_s.html')
            else:
                flash ("Unidentified Username or Password for Student!")
                return render_template('login_s.html')

@app.route('/logout')
def logout():
     session.pop('user', None)
     session.pop('name', None)
     return redirect('/login.html')

@app.route('/signup.html')
def signup():
    # tells Flask to render the HTML page called signup.html
	return render_template('signup.html')

@app.route('/announcements_i.html')
def announcements_i():
    # tells Flask to render the HTML page called /announcements_i.html
	return render_template('/announcements_i.html')

@app.route('/announcements_s.html')
def announcements_s():
    # tells Flask to render the HTML page called /announcements_s.html
	return render_template('/announcements_s.html')

@app.route('/evaluations_i.html')
def evaluations_i():
    # tells Flask to render the HTML page called /evaluations_i.html
	return render_template('/evaluations_i.html')

@app.route('/evaluations_s.html')
def evaluations_s():
    # tells Flask to render the HTML page called /evaluations_s.html
	return render_template('/evaluations_s.html')

@app.route('/index_i.html')
def index_i():
    # tells Flask to render the HTML page called /index_i.html
	return render_template('/index_i.html')

@app.route('/index_s.html')
def index_s():
    # tells Flask to render the HTML page called /index_s.html
	return render_template('/index_s.html')

@app.route('/labs_i.html')
def labs_i():
    # tells Flask to render the HTML page called /labs_i.html
	return render_template('/labs_i.html')

@app.route('/labs_s.html')
def labs_s():
    # tells Flask to render the HTML page called /labs_s.html
	return render_template('/labs_s.html')

@app.route('/lectures_i.html')
def lectures_i():
    # tells Flask to render the HTML page called /lectures_i.html
	return render_template('/lectures_i.html')

@app.route('/lectures_s.html')
def lectures_s():
    # tells Flask to render the HTML page called /lectures_s.html
	return render_template('/lectures_s.html')

@app.route('/feedback_i.html')
def feedback_i():
    # tells Flask to render the HTML page called /feedback_i.html
	return render_template('/feedback_i.html')

@app.route('/feedback_s.html')
def feedback_s():
    # tells Flask to render the HTML page called /feedback_s.html
	return render_template('/feedback_s.html')

@app.route('/resources_i.html')
def resources_i():
    # tells Flask to render the HTML page called /resources_i.html
	return render_template('/resources_i.html')

@app.route('/resources_s.html')
def resources_s():
    # tells Flask to render the HTML page called /resources_s.html
	return render_template('/resources_s.html')

@app.route('/grades_i.html')
def grades_i():
    # tells Flask to render the HTML page called /grades_i.html
	return render_template('/grades_i.html')

@app.route('/grades_s.html')
def grades_s():
    # tells Flask to render the HTML page called /grades_s.html
	return render_template('/grades_s.html')

@app.route('/regrades_i.html')
def regrades_i():
    # tells Flask to render the HTML page called regrades_i.html
	return render_template('regrades_i.html')

if __name__ == '__main__':
	app.run(debug ="true")