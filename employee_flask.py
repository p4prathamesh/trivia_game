from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import yaml
import datetime

app = Flask(__name__)
app.secret_key = 'something simple for now'

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']

mysql = MySQL(app)

#Global variables
today = datetime.datetime.now();

#index/home page
@app.route('/', methods=['GET','POST'])
def index():
	cur = mysql.connection.cursor()
	return render_template('index.html')

#first/getname page
@app.route('/first_page', methods=['GET','POST'])
def first_page():
	if request.method == 'POST':
		employeeForm = request.form
		name = employeeForm['name']
		session['username'] = name
		return render_template('second_page.html', employeeName=session['username'])
	return render_template('first_page.html')

#second/best_cricketer page
@app.route('/second_page', methods=['GET','POST'])
def secound_page():
	if request.method == 'POST':
		employeeForm = request.form
		session['best_cric'] = employeeForm['exampleRadios']
		return render_template('third_page.html', employeeName=session['username'], best_cric=session['best_cric'])
	return render_template('secound_page.html')

#third/coloursInFlag page
@app.route('/third_page', methods=['GET','POST'])
def third_page():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		employeeForm = request.form
		colour_selected_list=request.form.getlist('colour')
		temp=""
		for i in colour_selected_list:
			temp=temp+i+", "
		session['nationalflag_colour'] = temp[0:len(temp)-2:]
		cur.execute("INSERT INTO game values(%s,%s,%s,%s)",(today,session['username'],session['best_cric'],session['nationalflag_colour']))
		mysql.connection.commit()
		cur.close()
		return render_template('summary.html', employeeName=session['username'], best_cric=session['best_cric'], nationalflag_colour=session['nationalflag_colour'])
	return render_template('third_page.html')

#summary of input
@app.route('/summary', methods=['GET', 'POST'])
def summary():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM game")
		employeeDetails = cur.fetchall()
		render_template('history.html', employeeDetails=employeeDetails)
	return render_template('summary.html')

#history of all game
@app.route('/history', methods=['GET','POST'])
def history():
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM game")
	employeeDetails = cur.fetchall()		
	return render_template('history.html',employeeDetails=employeeDetails)

if __name__ == '__main__':
    app.run(debug=True)