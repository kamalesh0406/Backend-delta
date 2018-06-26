from flask import Flask ,request ,render_template ,redirect , url_for , session , flash
import MySQLdb
from datetime import datetime
from datetime import timedelta

date_value=0;


db = MySQLdb.connect("localhost","your username","password","CALENDAR")

curs = db.cursor() 

app = Flask(__name__)
app.secret_key = 'GHESGFHFH'

@app.before_request
def make_session_permanent():
    session.permanent = False

@app.route("/")
def welcome():
	return render_template('homepage.html')
@app.route("/calendar/add",methods=["GET","POST"])
def addevent():
	error = None
	if 'username' in session:	
		if request.method == "GET":
			error = None
			return render_template('addevent.html',error = error)
		if request.method == "POST":
			newevent = request.form.to_dict()
			username = session.get('username')
			sql ="SELECT * FROM EVENTS"
			curs.execute(sql)
			data = curs.fetchall()
			if len(data) == 0:
				event_id = 1
				newevent['event_id']=event_id
			else:
				event_id = len(data)+1
				newevent['event_id'] = event_id
			try:

				today_date = datetime.strftime(datetime.now(),"%Y-%m-%d")
				print (today_date)
				print(newevent['date'],newevent['start'],newevent['end'])
				if today_date<newevent['date']:
					if newevent['start']<newevent['end']:
						sql = "INSERT INTO EVENTS(event_id,date_event,start_time,end_time,Title,Description) VALUES(%(event_id)d,'%(date)s', '%(start)s','%(end)s' ,'%(title)s' ,'%(description)s')"%(newevent)

						sql2 = "INSERT INTO USER_EVENTS(user,event) VALUES('%s',%d)"%(username,newevent['event_id'])

						curs.execute(sql)
						curs.execute(sql2)

						db.commit()
						return (redirect(url_for('calendar')))
					else:
						raise ValueError
				else:
					raise ValueError
			except ValueError:
				error = "Enter the time/date properly"
				return render_template('addevent.html',error=error)

@app.route("/calendar",methods=["GET","POST"])
def calendar():
	if 'username' in session:
		cal=[]
		temp=[]
		username=session['username']

		sql="SELECT * FROM USER_EVENTS WHERE user='%s'"%(username)

		curs.execute(sql)

		data = curs.fetchall()
		if len(data)!=0:
			for row in data:
				sql1 = "SELECT * FROM EVENTS WHERE event_id=%d"%(row[1])
				curs.execute(sql1)
				event_data = curs.fetchall()
				for values in event_data:
					temp.append(values[1:])
		count = -1
		for i in range(0,30):
			date = datetime.strftime(datetime.now()+timedelta(**{'days':i}),"%Y-%m-%d")
			for events in temp:
				event_date = datetime.strftime(events[0],"%Y-%m-%d")
				if event_date==date:
					count+=1
					cal.append(temp[count])
					break
			else:
				val = (date,"None")
				cal.append(val)
		if count==-1:
			for i in range(0,len(temp)):
				cal.append(temp[i])
		return render_template('normalpage.html',calendar = cal)
	else:
		return redirect(url_for('login'))
@app.route("/login",methods=['GET','POST'])
def login():
	error = None	
	if request.method =="GET":
		return render_template('loginpage.html',error = error)
	if request.method == "POST":
		values = request.form
		sql = "SELECT * FROM USER"
		try:
			curs.execute(sql)
			result = curs.fetchall()
			if len(result)!=0:
				for row in result:
					if row[0]== values['username']:
						if row[1] == values['password']:
							session['username'] = values['username'];
							flash("You have succesfully logged in")
							return redirect(url_for('calendar'))
							
				else:
					error ="Incorrect Login Credentials"
					return render_template('loginpage.html',error = error)
			else:
				error ="Create An Account"
				return render_template('loginpage.html',error = error)
		except ValueError:
			pass

@app.route("/signup",methods=['GET','POST'])
def signup():
	error =None
	if request.method == "GET":
		return render_template('signup.html',error=error)

	if request.method == "POST":
		values = request.form;
		sql ="INSERT INTO USER(user_name,password) VALUES('%s','%s')"%(values['username'],values['password'])
		
		try:
			curs.execute(sql)
			curs.execute(sql1)

			db.commit();
			return redirect(url_for('welcome'))
		except MySQLdb.IntegrityError:
			error="Username Already Taken"
			return render_template('signup.html',error=error)
			db.rollback()
	


if __name__ =="__main__":
	app.run(debug=True)
