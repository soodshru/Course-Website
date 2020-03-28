import sqlite3
from flask import Flask, session, redirect, url_for, escape, request, render_template, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key = 'George#1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)

@app.route('/')
def root():
    # tells Flask to render the HTML page called index.html
    return render_template('index.html')

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html')

@app.route('/signupform', methods=['GET', 'POST'])
def signup_form():
    if request.method == 'POST':
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        UtorID = str(request.form['UtorID'])
        UtorEmail = str(request.form['UtorEmail'])
        Password = str(request.form['Password'])
        Usertype = str(request.form['usertype'])
        sql = ("""INSERT INTO Accounts VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(UtorID, firstname, lastname, Password, UtorEmail, Usertype))
        db.engine.execute(text(sql))
        return render_template('signin.html')
    else:
        return render_template('index.html')

@app.route('/index.html')
def home_page():
    return render_template('index.html')

@app.route('/signin.html')
def signin_page():
    return render_template('signin.html')

@app.route('/signinform', methods=['GET', 'POST'])
def signin_form():
    if request.method == 'POST':
        UtorID = str(request.form['UtorID'])
        Password = str(request.form['Password'])
        if UtorID in session:
            session['UtorID'] = UtorID
            return render_template('Lecture.html')
        else:
            sql = ("""Select * FROM Accounts""")
            Accounts = db.engine.execute(text(sql))
            for Account in Accounts:
                if Account['UtorID'] == UtorID:
                    if Account['Password'] == Password:
                        session['user'] = UtorID
                        session['FullName'] = Account['FirstName'] + " " + Account['LastName']
                        if Account['Type'] == "INSTRUCTOR":
                            session['usertype'] = "INSTRUCTOR"
                            session['email'] = Account['Email']
                            return redirect('/instructorprofile.html')
                        else:
                            session['usertype'] = "STUDENT"
                            return redirect('/studentprofile.html')              
            else:
                return render_template('signin.html', string = "Wrong username/password!")  
    else:
        return render_template('index.html')

@app.route('/assignments.html')
def assignments_page():
    if session.get('user') == None:
        return redirect('/index.html')
    else:
        return render_template('assignments.html')

@app.route('/contacts.html')
def contacts_page():
    if session.get('user') == None:
        return redirect('/index.html')
    elif session['usertype'] == "INSTRUCTOR":
        return redirect('/profile')
    else:
        sql = """SELECT FirstName, LastName, Email from Accounts where Type='INSTRUCTOR'"""
        Instructors = db.engine.execute(text(sql))
        return render_template('contacts.html', instructors = Instructors)

@app.route('/lab.html')
def lab_page():
    if session.get('user') == None:
        return redirect('/index.html')
    else:
        return render_template('lab.html')

@app.route('/Lecture.html')
def Lecture_page():
    if session.get('user') == None:
        return redirect('/index.html')
    else:    
        return render_template('Lecture.html')

@app.route('/resources.html')
def recources_page():
    if session.get('user') == None:
        return redirect('/index.html')
    else:    
        return render_template('resources.html')

@app.route('/studentprofile.html')
def studentprofile_page():
    if session.get('user') == None:
        return redirect('/index.html')
    elif session.get('usertype') == 'INSTRUCTOR':
        return redirect('/profile')
    else:    
        sql = ("""Select * FROM StudentGrades""")
        StudentGrades = db.engine.execute(text(sql))
        Quiz1 = "Mark not available yet"
        Quiz2 = "Mark not available yet"
        Quiz3 = "Mark not available yet"
        Quiz4 = "Mark not available yet"
        Assignment1 = "Mark not available yet"
        Assignment2 = "Mark not available yet"
        Assignment3 = "Mark not available yet"
        MidtermG = "Mark not available yet"
        FinalG = "Mark not available yet"
        print (session)
        for StudentGrade in StudentGrades:
            if StudentGrade['UtorID'] == session['user']:
                if StudentGrade['Category'] == 'QUIZ1':
                    Quiz1 = StudentGrade['Grade']
                    
                elif StudentGrade['Category'] == 'QUIZ2':
                    Quiz2 = StudentGrade['Grade']
                    
                elif StudentGrade['Category'] == 'QUIZ3':
                    Quiz3 = StudentGrade['Grade']
                    
                elif StudentGrade['Category'] == 'QUIZ4':
                    Quiz4 = StudentGrade['Grade']
                     
                elif StudentGrade['Category'] == 'ASSIGNMENT1':
                    Assignment1 = StudentGrade['Grade']
    
                elif StudentGrade['Category'] == 'ASSIGNMENT2':
                    Assignment2 = StudentGrade['Grade']
    
                elif StudentGrade['Category'] == 'ASSIGNMENT3':
                    Assignment3 = StudentGrade['Grade']

                elif StudentGrade['Category'] == 'MIDTERM':
                    MidtermG = StudentGrade['Grade']
                    
                elif StudentGrade['Category'] == 'FINAL':
                    FinalG = StudentGrade['Grade']
        return render_template('studentprofile.html', DisplayName = session["FullName"], Quiz1Grade = Quiz1, Quiz2Grade = Quiz2, Quiz3Grade = Quiz3, Quiz4Grade = Quiz4, Assignment1Grade = Assignment1,
                                Assignment2Grade = Assignment2, Assignment3Grade = Assignment3, MidtermGrade = MidtermG, FinalGrade = FinalG)

@app.route('/remarkform', methods=['GET', 'POST'])
def remark_form():
    if session.get('user') == None:
        return redirect('/index.html')
    else:    
        if request.method == 'POST':
            UtorID = str(request.form['UtorID'])
            Remark_Category = str(request.form['Remark_Category'])
            Remark_Info = str(request.form['Remark_Info'])
            sql = """INSERT INTO RemarkRequests Values ('{}', '{}', '{}')""".format(UtorID, Remark_Category, Remark_Info)
            db.engine.execute(text(sql))
        return redirect('/profile')

@app.route('/instructorprofile.html')
def instructorprofile_page():
    if session.get('user') == None:
        return redirect('index.html')
    elif session.get('usertype') == 'STUDENT':
        return redirect('/profile')
    else:
        sql = """Select Count(UtorID) as Count from Accounts where Type='STUDENT'"""
        student_count = db.engine.execute(text(sql))
        return render_template('instructorprofile.html', DisplayName = session["FullName"], student_count = student_count)

@app.route('/feedback.html')
def feedback_page():
    if session.get('user') == None:
        return redirect('index.html')
    elif session.get('usertype') == 'STUDENT':
        return redirect('/profile')
    else:
        sql = """Select * FROM Feedbacks where Contact_Instructor = '{}'""".format(session['email'])
        Feedbacks = db.engine.execute(text(sql))
        Feedbacks1 = db.engine.execute(text(sql))
        Feedbacks2 = db.engine.execute(text(sql))
        Feedbacks3 = db.engine.execute(text(sql))
        return render_template('feedback.html', Feedbacks = Feedbacks, Feedbacks1 = Feedbacks1, Feedbacks2 = Feedbacks2, Feedbacks3 = Feedbacks3)

@app.route('/profile')
def view_profile():
    if session.get('user') == None:
        return redirect('/index.html')
    else:        
        if session['usertype'] == "INSTRUCTOR":
            return redirect('/instructorprofile.html')
        elif session['usertype'] == "STUDENT":
            return redirect('/studentprofile.html')
        else:
            return redirect('/index.html')
    
    
@app.route('/logout')
def logout_user():
    if session.get('user') == None:
        return redirect('index.html')
    else:
        session.pop('user', None)
        session.pop('FullName', None)
        session.pop('usertype', None)
        return redirect('/index.html')

@app.route('/instructorGrades.html')
def instructor_grades_page():
    if session.get('user') == None:
        return redirect('index.html')
    elif session.get('usertype') == 'STUDENT':
        return redirect('/profile')
    else:    
        sql = ("""SELECT * FROM StudentGrades where Category = 'QUIZ1' or Category = 'QUIZ2' or Category = 'QUIZ3' or Category = 'QUIZ4'""")
        quizgrades = db.engine.execute(text(sql))
    
        sql = ("""Select * FROM StudentGrades where Category = 'ASSIGNMENT1' or Category = 'ASSIGNMENT2' or Category = 'ASSIGNMENT3'""")
        assigngrades = db.engine.execute(text(sql))
        
        sql = ("""Select * FROM StudentGrades where Category = 'MIDTERM'""")
        midtermgrades = db.engine.execute(text(sql))
        
        sql = ("""Select * FROM StudentGrades where Category = 'FINAL'""")
        finalgrades = db.engine.execute(text(sql))
        
        sql = """Select * FROM RemarkRequests"""
        Remarks = db.engine.execute(text(sql))
        
        return render_template('instructorGrades.html', quizgrades = quizgrades, assigngrades = assigngrades, 
                               midtermgrades = midtermgrades, finalgrades = finalgrades, remarks = Remarks)

@app.route('/newentryform', methods=['GET', 'POST'])
def new_entry_form():
    if session.get('user') == None:
        return redirect('/index.html')
    else:        
        if request.method == 'POST':
            UtorID = str(request.form['UtorID'])
            NewEntry_Category = str(request.form['NewEntry_Category'])
            Date = str(request.form['Date'])
            Mark = str(request.form['Mark'])
            sql = """INSERT INTO StudentGrades Values ('{}', '{}', '{}', '{}')""".format(UtorID, NewEntry_Category, Date, Mark)
            db.engine.execute(text(sql))
        return redirect('/instructorGrades.html')

@app.route('/changegradeform', methods=['GET', 'POST'])
def change_grade_form():
    if session.get('user') == None:
        return redirect('/index.html')
    else:        
        if request.method == 'POST':
            UtorID = str(request.form['UtorID'])
            Entry_Category = str(request.form['Entry_Category'])
            NewDate = str(request.form['NewDate'])
            NewMark = str(request.form['NewMark'])
            sql = """UPDATE StudentGrades SET Date = '{}', Grade = '{}' where (UtorID = '{}' and Category = '{}')""".format(NewDate, NewMark, UtorID, Entry_Category)
            db.engine.execute(text(sql))
        return redirect('/instructorGrades.html')

@app.route('/FeedbackForm', methods=['GET', 'POST'])
def feedback_form():
    if session.get('user') == None:
        return redirect('/index.html')
    else:        
        if request.method == 'POST':
            Contact_Instructor = str(request.form['Contact_Instructor'])
            Q1 = str(request.form['Q1'])
            Q2 = str(request.form['Q2'])
            Q3 = str(request.form['Q3'])
            Q4 = str(request.form['Q4'])
            sql = """INSERT INTO Feedbacks Values ('{}', '{}', '{}', '{}', '{}')""".format(Contact_Instructor, Q1, Q2, Q3, Q4)
            db.engine.execute(text(sql))
        return redirect('/contacts.html')

@app.route('/signIn_Index.html')
def signIn_Index_page():
    if session.get('user') == None:
        return redirect('/index.html')
    else:    
        return render_template('signIn_Index.html')


# run the app when app.py is run
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=7000)