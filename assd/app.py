from flask import Flask,render_template, request
import sqlite3 
app = Flask(__name__)


@app.route('/')
@app.route('/choice')
def give_choice(): 
	return render_template('choice.html')

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

			con = sqlite3.connect("assignment3db.db")
			cur = con.cursor()
			cur.execute("INSERT into login_table (user,password,usertype) VALUES (?,?,?)", (user,passw,usertype) )

			con.commit()
			con.close()
			msg = "You were Successfully Added. Navigate Back "
			success_flag = 1
			
		except:
			con.rollback()
			success_flag = 0
			msg = "Error Inserting Either Field(s) left blank or Account Already Exists. Please Try Again. Try Agian by Navigating Back"
			
		finally: 
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
			passw = request.form['password']
			usertype = request.form['usertype']

			con = sqlite3.connect("assignment3db.db")
			con.row_factory=sqlite3.Row
			cur = con.cursor()
			cur.execute("SELECT * from login_table WHERE user=? AND password=? AND usertype=?",(user,passw,usertype) )

			rows = cur.fetchall();
			con.close();
#failedlogin not yet made
			if len(rows)==0:
				return render_template('failedlogin.html')
			else:
				if usertype == 'Instructor':
					return render_template('instructorLogin.html', user=user)
				else:
					return render_template('studentLogin.html', user = user)

#FOR STUDENT USER, SHOWS THE COURSE MARKS FROM MARKS TABLE IN DB 
@app.route('/studentlogin', methods = ['POST','GET'])
def showmarks():
	if request.method == 'POST':
			utorid = request.form['utorid']
			con = sqlite3.connect("assignment3db.db")

			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("SELECT labs,assignment1,assignment2,assignment3,midterm,finalmark FROM marks WHERE utorid=?",[utorid] )

			rows = cur.fetchall();
			return render_template('showmarks.html', rows=rows, utorid=utorid)		


#EXECUTES QUERY FOR SENDING REMARK REQUEST FOR A STUDENT, SHOWS THE OUTPUT IN A NEW PAGE. 
@app.route('/remarkrequest', methods=['POST','GET'])
def remarkrequest():
	if request.method == 'POST':
		try: 
			utorid = request.form['utorid']
			remark = request.form['remark']
			reason = request.form['reason']

			con = sqlite3.connect("assignment3db.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("INSERT INTO remarkRequest (utorid,remark,comment) VALUES (?,?,?)", (utorid,remark,reason) ) 

			con.commit()
			msg = "Your Remark Request Was Complete"
			success_flag = 1

		except:
			con.rollback()
			success_flag = 0
			msg = "Error Inserting Please Try Again. Try Agian by Navigating Back"
			
         
		finally: 
			return render_template("resultRemark.html", msg = msg, success = success_flag)
			con.close()
			


#EXECUTES QUERY FOR SHOWING INSTRUCTORS ON THE PAGE WHERE STUDENT GIVES ANONYMOUS FEEDBACK
@app.route('/studentlogin2', methods = ['POST','GET'])
def givefeedback():
	if request.method == 'POST':

		#	utorid = request.form['utorid']
			con = sqlite3.connect("assignment3db.db")
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


#EXEXUTES QUERY FOR INSERTING STUDENT FEEDBACK IN THE DATABASE. 
@app.route('/sendfeedback2', methods=['POST','GET'])
def sendfeedback2():
	if request.method == 'POST':
		try: 
			instructor = request.form['instructor']
			q1 = request.form['q1']
			q2 = request.form['q2']
			q3 = request.form['q3']
			q4 = request.form['q4']
			q5= request.form['q5']

			con = sqlite3.connect("assignment3db.db")
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
			


@app.route('/showclassgrades', methods=["POST","GET"])
def showclassgrades():
	if request.method == 'POST':

		con = sqlite3.connect("assignment3db.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM marks")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showclassgradesoutput.html', rows=rows)


@app.route('/showfeedback', methods=['POST','GET'])
def showfeedback(): 
	if request.method == 'POST':

		con = sqlite3.connect("assignment3db.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM feedback")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showfeedbackoutput.html', rows=rows)


@app.route('/showremarkrequests', methods=['POST','GET'])
def showremarkrequests(): 
	if request.method == 'POST':

		con = sqlite3.connect("assignment3db.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM remarkRequest")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showremarkrequestsoutput.html', rows=rows)

@app.route('/inputmarks3', methods=['POST','GET'])
def inputmarks():
	if request.method == 'POST':

		con = sqlite3.connect("assignment3db.db")
		con.row_factory=sqlite3.Row

		cur = con.cursor()
		cur.execute("SELECT * FROM requestRemark")

		rows = cur.fetchall();
		con.close();

		if len(rows)==0:  #SEND A PAGE SAYING INCORRECT UTORID SINCE THE SELECT QURY DID NOT WORK
			return render_template('failedlogin.html')
		else:
			return render_template('showremarkrequestsoutput.html', rows=rows)

@app.route('/inputmarks.html')
def inputmarks22():
	return render_template('inputmarksoutput.html')

@app.route('/inputmarks2',methods=['POST','GET'])
def inputmarks2():
	if request.method == 'POST':
		try: 
			utorid = request.form['utorid']
			labs = request.form['labs']
			a1 = request.form['a1']
			a2 = request.form['a2']
			a3 = request.form['a3']
			midterm = request.form['midterm']
			final= request.form['finalmarks']

			con = sqlite3.connect("assignment3db.db")
			con.row_factory=sqlite3.Row

			cur = con.cursor()
			cur.execute("INSERT INTO marks (utorid,labs,assignment1,assignment2,assignment3,midterm,finalmark) VALUES (?,?,?,?,?,?,?)", (utorid,labs,a1,a2,a3,midterm,final) ) 

			con.commit()
			msg = "Your Feedback was submitted"
			success_flag = 1 

		except:
			con.rollback()
			success_flag = 0
			msg = "Error inserting Marks. Marks already exist in database."
         
		finally: 
			return render_template("resultfeedback.html", msg = msg, success = success_flag)
			con.close()
			




if __name__=='__main__':
	app.run(debug = True)





