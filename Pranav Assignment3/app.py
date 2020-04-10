from flask import Flask,render_template, request, redirect, session, url_for
import sqlite3 
app = Flask(__name__)

app.secret_key = "Dhruv"

@app.route('/')
@app.route('/choice')
def give_choice(): 
	return render_template('choice.html')

@app.route('/logout')
def logout():
	session.pop("user",None)
	return render_template("notloggedin.html")


#PAGE SHOWS A TEMPLATE TO CREATE A NEW ACCOUNT 
@app.route('/newAccount.html')
def newAcc():
	return render_template('createAccount.html')   

#INSERT A NEW USER INTO THE LOGIN TABLE, AND SHOWS THE OUTPUT, WHETHER SUCCESSFUL OR NOT 
@app.route('/addrec', methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		try:
			user = request.form['user']
			passw = request.form['password']
			usertype = request.form['usertype']

			con = sqlite3.connect("assignment3.db")
			cur = con.cursor()
			cur.execute("INSERT into login_table (user,password,usertype) VALUES (?,?,?)", (user,passw,usertype) )

			con.commit()

			msg = "You were Successfully Added. Navigate Back "
			success_flag = 1
			
		except:
			con.rollback()
			success_flag = 0
			msg = "Error Inserting Either Field(s) left blank or Account Already Exists. Please Try Again. Try Agian by Navigating Back"
			
		finally: 
			if usertype == "Student" and success_flag==1:
				cur.execute("INSERT INTO marks (utorid,labs,assignment1,assignment2,assignment3,midterm,finalmark) VALUES (?,?,?,?,?,?,?)", (user,0,0,0,0,0,0) )
				con.commit()
				con.close();
			con.close();
			return render_template('result.html', success = success_flag, user = usertype)
			
		
#PAGE SHOWS A TEMPLATE FOR EXISTING USER TO LOG IN 
@app.route('/login.html')
def login():
	return render_template('login.html')

#QUERY FOR EXISTING USER TO LOG IN, DEPEDING ON USER TYPE OPENS THE CORRECT PAGE
@app.route('/logmein', methods = ['POST','GET'])
def logmein():
	if request.method == 'POST':
			user = request.form['user']
			session['user'] = user
			passw = request.form['password']
			usertype = request.form['usertype']

			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row
			cur = con.cursor()
			cur.execute("SELECT * from login_table WHERE user=?", [user])

			rows = cur.fetchall();
			con.close();
#failedlogin not yet made
			if len(rows)==0:
				return render_template('failedlogin.html')
			else:
				if usertype == 'Instructor':
					return redirect(url_for("instructorlogin"))
				else:
					return redirect(url_for("studentlogin"))
	else:
		return render_template('login.html')

@app.route('/stuu')
def studentlogin():
	if "user" in session:
		return render_template('studentLogin.html')
	else:
		return render_template('login.html')

	

@app.route("/instr")
def instructorlogin():
	if "user" in session:
		return render_template('instructorlogin.html')
	else:
		return render_template('login.html')


#FOR STUDENT USER, SHOWS THE COURSE MARKS FROM MARKS TABLE IN DB 
@app.route('/studentlogin', methods = ['POST','GET'])
def showmarks():
	if (request.method == 'POST' and "user" in session):
			utorid = request.form['utorid']
			con = sqlite3.connect("assignment3.db")

			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("SELECT labs,assignment1,assignment2,assignment3,midterm,finalmark FROM marks WHERE utorid=?",[utorid] )

			rows = cur.fetchall();
			return render_template('showmarks.html', rows=rows, utorid=utorid)		
	elif "user" in session:
		utorid = session["user"]
		con = sqlite3.connect("assignment3.db")

		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT labs,assignment1,assignment2,assignment3,midterm,finalmark FROM marks WHERE utorid=?",[utorid] )

		rows = cur.fetchall();
		return render_template('showmarks.html', rows=rows, utorid=utorid)		
	else:
		return render_template("login.html")


#EXECUTES QUERY FOR SENDING REMARK REQUEST FOR A STUDENT, SHOWS THE OUTPUT IN A NEW PAGE. 
@app.route('/remarkrequest', methods=['POST','GET'])
def remarkrequest():
	if request.method == 'POST' and "user" in session:
		try: 
			utorid = request.form['utorid']
			remark = request.form['remark']
			reason = request.form['reason']

			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("INSERT INTO remarkRequest (utorid,remark,comment) VALUES (?,?,?)", (utorid,remark,reason) ) 

			con.commit()
			msg = "Your Remark Request Was Complete"
			success_flag = 1

		except:
			con.rollback()
			success_flag = 0
			msg = "Error InsertinPlease Try Again. Try Agian by Navigating Back"
			
         
		finally: 
			return render_template("resultRemark.html", msg = msg, success = success_flag)
			con.close()
	elif "user" in session:
		return '''
				<h3>Logged In, Please Select a Proper Remarking Request.</h3>
				To Do So Click <a href="/studentlogin">Here</a>
				'''
	else:
		return render_template("login.html")



#EXECUTES QUERY FOR SHOWING INSTRUCTORS ON THE PAGE WHERE STUDENT GIVES ANONYMOUS FEEDBACK
@app.route('/studentlogin2', methods = ['POST','GET'])
def givefeedback():
	if request.method == 'POST' and "user" in session:
			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("SELECT DISTINCT instructor from feedback")

			rows = cur.fetchall();

			if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
				return render_template('failedlogin.html')
				con.close()
			else:
				return render_template('givefeedback.html', rows=rows)
				con.close()
	elif "user" in session:
			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("SELECT DISTINCT instructor from feedback")

			rows = cur.fetchall();

			if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
				return render_template('failedlogin.html')
				con.close()
			else:
				return render_template('givefeedback.html', rows=rows)
				con.close()
	else:
		return render_template('login.html')



#EXEXUTES QUERY FOR INSERTING STUDENT FEEDBACK IN THE DATABASE. 
@app.route('/sendfeedback2', methods=['POST','GET'])
def sendfeedback2():
	if request.method == 'POST' and "user" in session:
		try: 
			instructor = request.form['instructor']
			q1 = request.form['q1']
			q2 = request.form['q2']
			q3 = request.form['q3']
			q4 = request.form['q4']
			q5= request.form['q5']

			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("INSERT INTO feedback (instructor,q1,q2,q3,q4,q5) VALUES (?,?,?,?,?,?)", (instructor,q1,q2,q3,q4,q5) ) 

			con.commit()
			msg = "Your Feedback was submitted"
			success_flag = 1 

		except:
			con.rollback()
			success_flag = 0
			msg = "Error inserting feedback"
         
		finally: 
			return render_template("resultfeedback.html", msg = msg, success = success_flag)
			con.close()
	elif "user" in session:
		return '''
				<h3>Logged In, Please Select a Proper Feedback Submit Request.</h3>
				To Do So Click <a href="/studentlogin2">Here</a>
				'''
	else:
		return render_template('login.html')

			


@app.route('/showclassgrades', methods=["POST","GET"])
def showclassgrades():
	if request.method == 'POST' and "user" in session:
		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM marks")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showclassgradesoutput.html', rows=rows)
	elif "user" in session:
		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM marks")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showclassgradesoutput.html', rows=rows)
	else:
		return render_template('login.html')




@app.route('/showfeedback', methods=['POST','GET'])
def showfeedback(): 
	if request.method == 'POST' and "user" in session:
		utorid = request.form['utorid']
		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM feedback WHERE instructor=?",[utorid])

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showfeedbackoutput.html', rows=rows)
	
	elif "user" in session:
		return '''
				<h3>Logged In, But You Did Not Input Your UtorID.</h3>
				To Do So Click <a href="/instructorlogin.html">Here</a>
				'''
	else:
		return render_template("login.html")




@app.route('/showremarkrequests', methods=['POST','GET'])
def showremarkrequests(): 
	if request.method == 'POST' and "user" in session:
		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM remarkRequest")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showremarkrequestsoutput.html', rows=rows)
	elif "user" in session:
		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM remarkRequest")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showremarkrequestsoutput.html', rows=rows)
	else:
		return render_template('login.html')

'''
@app.route('/inputmarks3', methods=['POST','GET'])
def inputmarks():
	if request.method == 'POST':

		con = sqlite3.connect("assignment3.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM requestRemark")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showremarkrequestsoutput.html', rows=rows)'''


@app.route('/inputmarks.html')
def inputmarks22():
	if "user" in session:
		return render_template('inputmarksoutput.html')
	else:
		return render_template("login.html")
	

@app.route('/inputmarks2',methods=['POST','GET'])
def inputmarks2():
	if request.method == 'POST' and "user" in session:
		try: 
			utorid = request.form['utorid']
			labs = request.form['labs']
			a1 = request.form['a1']
			a2 = request.form['a2']
			a3 = request.form['a3']
			midterm = request.form['midterm']
			final= request.form['finalmarks']

			con = sqlite3.connect("assignment3.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("INSERT INTO marks (utorid,labs,assignment1,assignment2,assignment3,midterm,finalmark) VALUES (?,?,?,?,?,?,?)", (utorid,labs,a1,a2,a3,midterm,final) ) 

			con.commit()
			msg = "Marks were submitted"
			success_flag = 1 

		except:
			con.rollback()
			success_flag = 0
			msg = "Error inserting Marks. Marks already exist in database."
         
		finally: 
			return render_template("resultfeedback.html", msg = msg, success = success_flag)
			con.close()
	elif "user" in session:
		return '''
				<h3>Logged In, But You Did Not Submit Correct Form To Input Marks.</h3>
				To Do So Click <a href="/inputmarks.html">Here</a>
			   '''
	else:
		return render_template('login.html')

			

@app.route("/instructorlogin.html")
def inst():
	if "user" in session:
		return render_template('instructorlogin.html')
	else:
		return render_template('login.html')
	

@app.route("/studentlogin.html")
def student():
	if "user" in session:
		return render_template('studentlogin.html')
	else:
		return render_template('login.html')
	

@app.route("/index.html")
def index():
	if "user" in session:
		return render_template('index.html')
	else:
		return render_template('login.html')
	
	

@app.route("/Calender.html")
def cal():
	if "user" in session: 
		return render_template('Calender.html')
	else:
		return render_template('login.html')


@app.route("/Announcements.html")
def announce():
	if "user" in session:
		return render_template('Announcements.html')
	else:
		return render_template('login.html')



@app.route("/lecture.html")
def lectures():
	if "user" in session:
		return render_template('lecture.html')
	else:
		return render_template('login.html')

	

@app.route("/tutorials.html")
def tutorials():
	if "user" in session:
		return render_template('tutorials.html')
	else:
		return render_template('login.html')
	

@app.route("/assignments.html")
def assignments():
	if "user" in session:
		return render_template('assignments.html')
	else:
		return render_template('login.html')


@app.route("/test_info.html")
def test():
	if "user" in session:
		return render_template('test_info.html')
	else:
		return render_template('login.html')

@app.route("/resources.html")
def resources():
	if "user" in session:
		return render_template('resources.html')
	else:
		return render_template('login.html')


if __name__=='__main__':
	app.run(port=5000,debug = True)





