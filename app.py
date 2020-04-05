# required imports
# the sqlite3 library allows us to communicate with the sqlite databaseimport sqlite3
# we are adding the import 'g' which will be used for the database
from flask import Flask, render_template, request, g,session, redirect, url_for, escape
# the database file we are going to communicate with
DATABASE = './assignment3.db'
# connects to the database
def get_db():
	# if there is a database, use it
	db = getattr(g, '_database', None)
	if db is None:
		# otherwise, create a database to use
		db = g._database = sqlite3.connect(DATABASE)
	return db

# converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value)
					for idx, value in enumerate(row))

# given a query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
    	# close the database if we are connected to it
    	db.close()

@app.route('/')
def root():
	db = get_db()
	db.row_factory = make_dicts

	feedback = []
	for rows in query_db('select * from Feedback'):
		feedback.append(rows)
	db.close()
	return render_template('feedback_i.html', instructor_feedback = feedback)


if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')







