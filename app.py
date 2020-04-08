import sqlite3
import requests
from flask import Flask, session, redirect, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key = 'its_a_secret'
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
        # if user is already logged in
        if utorid in session:
            session['current_login'] = utorid
            return render_template('index_i.html')
        else:
            # only type = instructor can logged in
            sql = """ SELECT * FROM  accounts WHERE type = 'instructor' """
            # execute sql code
            accs = db.engine.execute(text(sql))
            for acc in accs:
                if acc['UtorID'] == utorid and acc['Password'] == pw:
                    session['current_login'] = utorid
                    session['name'] = acc['Name']
                    return render_template('index_i.html')
            else:
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
        # if user is already logged in
        if utorid in session:
            session['current_login'] = utorid
            return render_template('index_s.html')
        else:
            # only type = student can logged in
            sql = """ SELECT * FROM  accounts WHERE type = 'student' """
            # execute sql code
            accs = db.engine.execute(text(sql))
            for acc in accs:
                if acc['UtorID'] == utorid and acc['Password'] == pw:
                    session['current_login'] = utorid
                    session['name'] = acc['Name']
                    return render_template('index_s.html')
            else:
                flash ("Unidentified Username or Password for Student!")
                return render_template('login_s.html')

@app.route('/logout')
def logout():
    # removes user from session
    session.pop('current_login', None)
    session.pop('name', None)
    return redirect('/login.html')

@app.route('/signup.html')
def signup():
    # tells Flask to render the HTML page called signup.html
    return render_template('signup.html')

@app.route('/createaccform', methods=['GET','POST'])
def createacc():
    if request.method == 'POST':
        type = str(request.form.get('Usertype'))
        username = str(request.form.get('UserName'))
        loginid = str(request.form.get('LoginID'))
        pw = str(request.form.get('Password'))
        sql = """ INSERT INTO accounts VALUES ('{}', '{}', '{}', '{}') """.format(type,loginid,username,pw)
        db.engine.execute(text(sql))
        if type == 'student':
            sql = """ INSERT INTO Grades (UtorID)  VALUES ('{}') """.format(loginid)
            db.engine.execute(text(sql))
        return render_template('login.html')


@app.route('/announcements_i.html')
def announcements_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /announcements_i.html
        return render_template('/announcements_i.html')

@app.route('/announcements_s.html')
def announcements_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /announcements_s.html
        return render_template('/announcements_s.html')

@app.route('/evaluations_i.html')
def evaluations_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /evaluations_i.html
        return render_template('/evaluations_i.html')

@app.route('/evaluations_s.html')
def evaluations_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /evaluations_s.html
        return render_template('/evaluations_s.html')

@app.route('/index_i.html')
def index_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /index_i.html
        return render_template('/index_i.html')

@app.route('/index_s.html')
def index_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /index_s.html
        return render_template('/index_s.html')

@app.route('/labs_i.html')
def labs_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /labs_i.html
        return render_template('/labs_i.html')

@app.route('/labs_s.html')
def labs_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /labs_s.html
        return render_template('/labs_s.html')

@app.route('/lectures_i.html')
def lectures_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /lectures_i.html
        return render_template('/lectures_i.html')

@app.route('/lectures_s.html')
def lectures_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /lectures_s.html
        return render_template('/lectures_s.html')

@app.route('/feedback_i.html')
def feedback_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        sql = """ SELECT * FROM Feedback WHERE UtorID = '{}' """.format(session['current_login'])
        feedbacks = db.engine.execute(text(sql))
        # tells Flask to render the HTML page called /feedback_i.html
        return render_template('/feedback_i.html', feedbacks = feedbacks)

@app.route('/feedback_s.html')
def feedback_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        sql = """ SELECT UtorID,Name FROM accounts WHERE type = 'instructor' """
        instructors = db.engine.execute(text(sql))
        # tells Flask to render the HTML page called /feedback_s.html
        return render_template('/feedback_s.html', instructors = instructors)

@app.route('/addfeedback', methods=['GET','POST'])
def addFeedback():
    if request.method == 'POST':
        inst = str(request.form.get('instructor'))
        a1 = str(request.form.get('q1'))
        a2 = str(request.form.get('q2'))
        a3 = str(request.form.get('q3'))
        a4 = str(request.form.get('q4'))
        sql = """ INSERT INTO Feedback VALUES('{}','{}', '{}', '{}', '{}') """.format(inst, a1, a2, a3, a4)
        db.engine.execute(text(sql))
        return redirect('/feedback_s.html')

@app.route('/resources_i.html')
def resources_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /resources_i.html
        return render_template('/resources_i.html')

@app.route('/resources_s.html')
def resources_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /resources_s.html
        return render_template('/resources_s.html')

@app.route('/grades_i.html')
def grades_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /grades_i.html
        sql = """ SELECT * FROM Grades """
        class1 = db.engine.execute(text(sql))
        return render_template('/grades_i.html', class1 = class1)

@app.route('/EnterGrades', methods=['GET','POST'])
def Entergrades():
    if request.method == 'POST':
        type = str(request.form.get('assgn'))
        grade = str(request.form.get('grade'))
        stdid = str(request.form.get('StudentNumber'))
        sql = """ SELECT * FROM Grades """
        students = db.engine.execute(text(sql))
        for stud in students :
            if stud['UtorID'] == stdid :
                sql = """ UPDATE Grades SET {} = '{}' WHERE UtorID = '{}' """.format(type, grade, stdid)
                db.engine.execute(text(sql))
                return redirect('/grades_i.html')
        return redirect('/grades_i.html')

@app.route('/grades_s.html')
def grades_s():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        # tells Flask to render the HTML page called /grades_s.html
        Assgn1 = 'TBA'
        Assgn2 = 'TBA'
        Assgn3 = 'TBA'
        TT = 'TBA'
        Fin = 'TBA'
        name = 'Unknown'
        sql = """ SELECT * FROM Grades """
        grades = db.engine.execute(text(sql))
        for student in grades:
            if session['current_login'] == student['UtorID'] :
                Assgn1 = student['A1']
                Assgn2 = student['A2']
                Assgn3 = student['A3']
                TT = student['Midterm']
                Fin = student['Final']
                name = session['name']
        return render_template('grades_s.html', UserName = name, Ass1 = Assgn1, Ass2 = Assgn2, Ass3 = Assgn3, Mid = TT,
                               Fi = Fin)

@app.route('/RemarkRequest', methods=['GET','POST'])
def remarkrequest():
    if request.method == 'POST':
        Assgn = str(request.form.get('assgn'))
        reason = str(request.form.get('Message'))
        utorid = session['current_login']
        sql = """ INSERT INTO RemarkRequests VALUES ('{}', '{}', '{}') """.format(utorid, Assgn, reason)
        db.engine.execute(text(sql))
        return redirect('/grades_s.html')

@app.route('/regrades_i.html')
def regrades_i():
    if session.get('current_login') == None:
        # if user not logged in send them to the login page
        return render_template('login.html')
    else:
        sql = """ SELECT * FROM RemarkRequests """
        requests = db.engine.execute(text(sql))
        # tells Flask to render the HTML page called regrades_i.html
        return render_template('regrades_i.html', requests = requests)


if __name__ == '__main__':
    app.run(debug = 'True')