import re
import sqlite3
import random
conn = sqlite3.connect('tbs.db')
c = conn.cursor()


# SQL Queries
c.execute("""CREATE TABLE IF NOT EXISTS customers(customerid integer(10) NOT NULL PRIMARY KEY
,title VARCHAR(10) NOT NULL
,firstname VARCHAR(20) NOT NULL
,lastname VARCHAR(30) NOT NULL
,email VARCHAR(50) UNIQUE 
,telno VARCHAR(20) NOT NULL
,password VARCHAR(30)NOT NULL , address1 VARCHAR(30) NOT NULL , town VARCHAR(30) NOT NULL
,county VARCHAR(30) NOT NULL
, postcode VARCHAR(15) NOT NULL
,paymentmethod VARCHAR(20) NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS drivers(driverid integer(10) NOT NULL PRIMARY KEY
,title VARCHAR(10) NOT NULL
,firstname VARCHAR(20) NOT NULL
,lastname VARCHAR(30) NOT NULL
,email VARCHAR(50) UNIQUE
,password VARCHAR(30) NOT NULL
,regno VARCHAR(10) NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS admins(adminid integer(10) NOT NULL PRIMARY KEY
,firstname VARCHAR(20) NOT NULL
,lastname VARCHAR(30) NOT NULL
,email VARCHAR(50) UNIQUE
,password VARCHAR(30) NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS bookings(bookingid integer(10) PRIMARY KEY NOT NULL
,customerid integer(10) NOT NULL
,driverid integer(10) NOT NULL
,startaddress VARCHAR(100) NOT NULL
,destinationaddress VARCHAR(100) NOT NULL
,date TEXT NOT NULL,time TEXT NOT NULL
,status VARCHAR(10)NOT NULL,paid VARCHAR(3) NOT NULL
,FOREIGN KEY (customerid) REFERENCES customers(customerid)
,FOREIGN KEY (driverid) REFERENCES drivers(driverid))""")

c.execute("SELECT * FROM bookings WHERE status='confirmed'")
print(c.fetchall())

conn.commit()
conn.close()
