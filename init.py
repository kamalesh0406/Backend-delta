import MySQLdb
db = MySQLdb.connect("localhost","your username","your password","CALENDAR")

curs = db.cursor()

curs.execute("CREATE TABLE USER(user_name varchar(12) NOT NULL ,password varchar(10), PRIMARY KEY(user_name))")
curs.execute("CREATE TABLE EVENTS(event_id INT NOT NULL,date_event DATE NOT NULL ,start_time TIME , end_time TIME , Title varchar(20) , Description varchar(30), PRIMARY KEY(event_id))")
curs.execute("CREATE TABLE USER_EVENTS(user varchar(12),event int ,FOREIGN KEY(user) REFERENCES USER(user_name), FOREIGN KEY(event) REFERENCES EVENTS(event_id))")
db.commit()
db.close()
