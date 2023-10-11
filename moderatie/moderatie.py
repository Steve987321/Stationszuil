import psycopg2
from tkinter import * 

con = psycopg2.connect(
                    database="StationZuil", 
                    user="postgres",
                    password="pass",
                    host="localhost",
                    port="5433"
                    )

cursor = con.cursor()

cursor.execute("select * from station_service;")
print(cursor.fetchall())

if not con.closed:
    con.close()
