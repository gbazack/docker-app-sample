import os
import mysql.connector as connector
import json
from flask import Flask

app= Flask(__name__)
#app.config.from_envvar()

@app.route('/')
def hello_world():
    return "Hello, Docker!"

@app.route('/widgets')
def get_widgets():
	db_host= os.environ.get("DB_SERVER")
	db_user= os.environ.get("DB_USER")
	db_pass= os.environ.get("DB_PASSWD")
	db_name= os.environ.get("DB_NAME")
	#
	mydb= connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor= mydb.cursor()
	cursor.execute("SELECT * FROM widgets")
	#This code will extract row headers
	row_headers= [x[0] for x in cursor.description]
	results= cursor.fetchall()
	json_data= []
	#
	for result in results:
		json_data.append(dict(zip(row_headers, result)))
	cursor.close()
	
	return json.dumps(json_data)


@app.route('/initdb')
def db_init():
	db_host= os.environ.get("DB_SERVER")
	db_user= os.environ.get("DB_USER")
	db_pass= os.environ.get("DB_PASSWD")
	db_name= os.environ.get("DB_NAME")
	#
	mydb= connector.connect(host=db_host, user=db_user, password=db_pass)
	cursor= mydb.cursor()
	cursor.execute("DROP DATABASE IF EXISTS inventory")
	cursor.execute("CREATE DABABASE inventory")
	cursor.close()
	#
	mydb= connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	#
	cursor= mydb.cursor()
	cursor.execute("DROP TABLE IF EXISTS widgets")
	cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
	cursor.close()
	
	return 'init database'

if __name__=="__main__":
	app.run()
	
	
		
