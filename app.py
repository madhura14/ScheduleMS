from flask import Flask, jsonify, request
import numpy as np
from sklearn.externals import joblib
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib
from bs4 import BeautifulSoup
import re
import sqlite3


# https://www.tutorialspoint.com/flask
import flask
app = flask.Flask(__name__)


conn = sqlite3.connect('schedule_DB.db')
print("Opened Databse successfully")
c = conn.cursor()

c.execute(''' CREATE TABLE IF NOT EXISTS SCHEDULING
             (room_date DATE, time INTEGER, room TEXT,
             time_period INTEGER, formate TEXT)  ''')
print("Table created")
c.close()

@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/index')
def index():
    return flask.render_template('index.html')


@app.route('/schedule', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            A = request.form['room_date']
            B = request.form['time']
            C = request.form['rooms']
            D = request.form['time_period']
            E = request.form['formate']

            with sqlite3.connect("schedule_DB.db") as conn:
                c = conn.cursor()
                
                if A and B and C and D and E:
                    c.execute('''SELECT room_date, time, room, time_period, formate
                                FROM SCHEDULING
                                WHERE room_date == ? AND time == ? AND room == ?''', (A, B, C))
                    data = c.fetchall()

                    if len(data) == 0:
                        c.execute(''' INSERT INTO SCHEDULING 
                                (room_date, time, room, time_period, formate) 
                                VALUES
                                (?, ?, ?, ?, ?)''', (A, B, C, D, E))
                        conn.commit()
                        msg = "Meeting has been scheduled"
                    else:
                        msg = "This slot has been booked already for {} {}, try again.".format(D, E)
                else:
                    raise Exception
        except:
            conn.rollback()
            msg = "Insert all values."

        finally:
            return flask.render_template("result.html", msg = msg)
            conn.close()


@app.route('/list')
def list():
   conn = sqlite3.connect("schedule_DB.db")
   conn.row_factory = sqlite3.Row
   
   c = conn.cursor()
   c.execute("select * from scheduling")
   
   rows = c.fetchall(); 
   return flask.render_template("list.html",rows = rows)

if __name__ == '__main__':
    app.run(debug = True)
