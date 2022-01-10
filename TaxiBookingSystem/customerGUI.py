from math import inf
from os import stat
import sqlite3
from sqlite3.dbapi2 import DatabaseError, Timestamp
from time import sleep
from tkinter import messagebox
from tkinter import *
from tkinter import font
import re
from tkinter import ttk
from typing import Protocol
from datetime import date, datetime
import random


# =================================THIS IS A DASHBOARD CLASS FOR CUSTOMER========
class Customer(Tk):
    def __init__(self):
        super().__init__()

        # =====CONNECTDB
        self.conn = sqlite3.connect('tbs.db')
        self.c = self.conn.cursor()
        # =====CONNECTDB

        # TK WINDOW ATTRIBUTES
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Customer Dashboard")
        self["bg"] = ["yellow"]
        # TK WINDOW ATTRIBUTES

    # CUSTOM METHODS

    def checkDetails(self):
        infowindow = Tk()
        infowindow.geometry("800x500+470+100")
        infowindow.resizable(False, False)
        infowindow.title("Edit Your Data")
        infowindow["bg"] = ["yellow"]
        idEntry = Entry(infowindow, highlightthickness=0,
                        bg='white', font='Courier 15', borderwidth=0)
        idEntry.insert(0, 'Enter Your ID')
        idEntry.place(x=70, y=20, width=360, height=50)

        # EDIT YOUR DETAILS FUNCTION
        def editDetails():
            with self.conn:
                self.c.execute(
                    """SELECT * FROM customers WHERE customerid=:customerid""", {'customerid':  idEntry.get()})
                if not self.c.fetchone():
                    message = messagebox.showerror(
                        'Wrong Email', 'The ID you entered is wrong or not found')
                    infowindow.destroy()
                else:
                    self.c.execute(
                        "SELECT * FROM customers WHERE customerid=:customerid", {'customerid':  idEntry.get()})
                    result = self.c.fetchone()
                    id, title, fname, lname, email, telno, password, address, town, county, postcode, payment = (
                        result)
                    emailedit = Entry(infowindow, highlightthickness=0,
                                      bg='white', font='Courier 11', borderwidth=0)
                    emailedit.insert(0, email)
                    emailedit.place(x=70, y=80, height=20, width=350)
                    emailabel = Label(
                        infowindow, text='Email', bg='yellow').place(x=20, y=80)

                    passwordedit = Entry(infowindow, highlightthickness=0,
                                         bg='white', font='Courier 11', borderwidth=0)
                    passwordedit.insert(0, password)
                    passwordedit.place(x=70, y=120, height=20, width=350)
                    passwordabel = Label(
                        infowindow, text='Password', bg='yellow').place(x=10, y=120)

                    addressedit = Entry(infowindow, highlightthickness=0,
                                        bg='white', font='Courier 11', borderwidth=0)
                    addressedit.insert(0, address)
                    addressedit.place(x=70, y=160, height=20, width=350)
                    addressabel = Label(
                        infowindow, text='Address', bg='yellow').place(x=15, y=160)

                    paymentedit = Entry(infowindow, highlightthickness=0,
                                        bg='white', font='Courier 11', borderwidth=0)
                    paymentedit.insert(0, payment)
                    paymentedit.place(x=70, y=200, height=20, width=350)

                    addressabel = Label(
                        infowindow, text='Payment', bg='yellow').place(x=15, y=200)

                    # CHECK THE VALIDITY OF ENTERED DETAILS
                    def checkDetails():
                        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                        if (re.fullmatch(regex, emailedit.get())):
                            if paymentedit.get() != "Credit":
                                if paymentedit.get() != "Cash":
                                    error = messagebox.showwarning(
                                        'error', 'Please use Cash or Credit as payment method')
                            updateDetails()

                        else:
                            error = messagebox.showwarning(
                                'error', 'email is not valid')
                        infowindow.lift()
                    # END

                # TO UPDATE CHANGED DATA INTO DATABASE
                def updateDetails():
                    with self.conn:
                        self.c.execute(
                            """UPDATE customers SET email=:email,password=:password,address1=:address1,paymentmethod=:paymentmethod WHERE customerid=:customerid""", {'email': emailedit.get(), 'password': passwordedit.get(), 'address1': addressedit.get(), 'paymentmethod': paymentedit.get(), 'customerid':  idEntry.get()})
                # END
            btnsubmit = Button(infowindow, text="Submit", bg='yellow',
                               font='Courier 10', command=editDetails, state=DISABLED)
            btnsubmit.place(x=460, y=30, height=30, width=90)

            btnconfirm = Button(infowindow, text="Confirm Changes",
                                font='Courier 10', command=checkDetails)
            btnconfirm.place(x=70, y=320, height=30, width=130)

        btnsubmit = Button(infowindow, text="Submit", bg='yellow',
                           font='Courier 10', command=editDetails)
        btnsubmit.place(x=460, y=30, height=30, width=90)
        # END

    # BOOK A TAXI FUNCTION
    def booking(self):
        infowindow = Tk()
        infowindow.geometry("800x500+470+100")
        infowindow.resizable(False, False)
        infowindow.title("Book Taxi")
        infowindow["bg"] = ["yellow"]

        emailentry = Entry(infowindow, highlightthickness=0,
                           bg='white', font='Courier 15', borderwidth=0)
        emailentry.insert(0, 'Enter your Email')
        emailentry.place(x=50, y=30, height=50, width=320)

        def checkEmail():
            conn = sqlite3.connect('tbs.db')
            c = conn.cursor()
            with conn:
                c.execute("SELECT * FROM customers WHERE email=:email", {
                    'email':  emailentry.get()})
            if not c.fetchone():
                message = Label(
                    infowindow, text='Email not valid', bg='yellow', font="Courier 10").place(x=60, y=70)

            else:
                btnsubmit = Button(infowindow, text='Submit',
                                   bg='yellow', font='Courier 10', state=DISABLED).place(x=400, y=40)
                with conn:
                    c.execute("SELECT address1 from customers WHERE email=:email", {
                              'email':  emailentry.get()})
                for value in c.fetchone():
                    value
                message = Label(
                    infowindow, text='Email    Exists', bg='yellow', font="Courier 10").place(x=60, y=70)

                startaddresslabel = Label(
                    infowindow, text='Starting Address:', font="Courier 15", bg='yellow').place(x=30, y=130)
                startaddressentry = Entry(infowindow, highlightthickness=0,
                                          bg='white', font='Courier 15', borderwidth=0)
                startaddressentry.place(x=260, y=125, height=40, width=400)
                startaddressentry.insert(0, value)

                destaddresslabel = Label(
                    infowindow, text='Dest.  Address:', font="Courier 15", bg='yellow').place(x=30, y=190)
                destaddressentry = Entry(infowindow, highlightthickness=0,
                                         bg='white', font='Courier 15', borderwidth=0)
                destaddressentry.place(x=260, y=185, height=40, width=400)
                # date
                today = date.today()
                today = today.strftime("%b-%d-%Y")
                # time
                now = datetime.now()
                now = now.strftime("%H:%M:%S")

                datelabel = Label(
                    infowindow, text=f"Date: {today}", font="Courier 15", bg='yellow').place(x=260, y=250)
                timelabel = Label(
                    infowindow, text=f"Time: {now}", font="Courier 15", bg='yellow').place(x=260, y=300)

                def confirmBooking():
                    start = str(startaddressentry.get())
                    dest = str(destaddressentry.get())
                    if not start:
                        message = messagebox.showerror(
                            'Error', 'Please Fill the Start address')
                        infowindow.lift()
                    if not dest:
                        message = messagebox.showerror(
                            'Error', 'Please Fill the Dest. address')
                        infowindow.lift()
                    else:
                        bookingid = random.randrange(100, 9000)
                        with conn:
                            c.execute("SELECT customerid FROM customers WHERE email=:email", {
                                      'email': emailentry.get()})
                            for id in c.fetchone():
                                id
                            with conn:
                                c.execute(
                                    """INSERT INTO bookings VALUES(:bookingid,:customerid,:driverid,:startaddress,:destinationaddress,:date,:time,:status,:paid)""", {'bookingid': bookingid, 'customerid': id, 'driverid': 1, 'startaddress': startaddressentry.get(), 'destinationaddress': destaddressentry.get(), 'date': today, 'time': now, 'status': 'pending', 'paid': 'no'})
                            btnbooking = Button(
                                infowindow, text='Confirm Booking', height=5, width=15, font='Courier 10', state=DISABLED)
                            btnbooking.place(x=250, y=350)
                btnbooking = Button(
                    infowindow, text='Confirm Booking', height=5, width=15, font='Courier 10', command=confirmBooking)
                btnbooking.place(x=250, y=350)
        btnsubmit = Button(infowindow, text='Submit',
                           bg='yellow', font='Courier 10', command=checkEmail).place(x=400, y=40)

    def seebooking(self):
        infowindow = Tk()
        infowindow.geometry("900x600+470+100")
        infowindow.resizable(False, False)
        infowindow.title("View Booking")
        infowindow["bg"] = ["yellow"]

        emailentry = Entry(infowindow, highlightthickness=0,
                           bg='white', font='Courier 15', borderwidth=0)
        emailentry.insert(0, 'Enter Your Email')
        emailentry.place(x=10, y=20, width=400)

        def checkBooking():
            btnsubmit = Button(infowindow, text="Submit", bg='yellow',
                               font='Courier 10', state=DISABLED)
            btnsubmit.place(x=450, y=15)
            with self.conn:
                self.c.execute("SELECT * FROM customers WHERE email=:email", {
                    'email': emailentry.get()})

            if not self.c.fetchone():
                message = messagebox.showerror("Error", "Email is not valid")
                infowindow.lift()
            else:
                scrollbar = Scrollbar(infowindow)
                mylist = Listbox(infowindow, yscrollcommand=scrollbar.set)
                with self.conn:
                    self.c.execute("SELECT customerid FROM customers WHERE email=:email", {
                                   'email': emailentry.get()})
                    for customerid in self.c.fetchone():
                        customerid
                with self.conn:
                    self.c.execute(
                        "SELECT bookingid,customerid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE customerid=:customerid", {'customerid': customerid})
                    result = self.c.fetchall()
                    for bookingid, customerid, startaddress, destinationaddress, date, time, status, paid in result:
                        bookingid, customerid, startaddress, destinationaddress, date, time, status, paid
                        mylist.insert(END, "Booking id: "+str(bookingid) + " /start: "+startaddress+" /dest. :" +
                                      destinationaddress+" /date: "+date+" "+time+" /status: "+status+" /paid: "+paid)
                    mylist.place(x=20, y=120, width=700, height=400)
                    scrollbar.config(command=mylist.yview)

                    def entryBooking():
                        bookingidentry = Entry(infowindow, highlightthickness=0,
                                               bg='white', font='Courier 15', borderwidth=0)
                        bookingidentry.place(x=200, y=530)
                        bookingidentry.insert(0, 'Enter Booking Id')

                        def cancelBooking():
                            with self.conn:
                                self.c.execute("SELECT status FROM bookings WHERE bookingid=:bookingid", {
                                               'bookingid': int(bookingidentry.get())})
                                result = self.c.fetchone()
                                for status in result:
                                    if status == "cancelled" or status == "confirmed" or status == "completed":
                                        message = messagebox.showerror(
                                            'Error', 'You cannot cancel this trip')
                                        infowindow.lift()
                                    else:
                                        with self.conn:
                                            self.c.execute("UPDATE bookings SET status='cancelled' WHERE bookingid=:bookingid", {
                                                'bookingid': int(bookingidentry.get())})

                        bookingsbmt = Button(
                            infowindow, text='Submit', command=cancelBooking).place(x=450, y=530)

                    def refreshList():
                        scrollbar = Scrollbar(infowindow)
                        mylist = Listbox(
                            infowindow, yscrollcommand=scrollbar.set)
                        with self.conn:
                            self.c.execute("SELECT customerid FROM customers WHERE email=:email", {
                                'email': emailentry.get()})
                            for customerid in self.c.fetchone():
                                customerid
                        with self.conn:
                            self.c.execute(
                                "SELECT bookingid,customerid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE customerid=:customerid", {'customerid': customerid})
                            result = self.c.fetchall()
                        for bookingid, customerid, startaddress, destinationaddress, date, time, status, paid in result:
                            bookingid, customerid, startaddress, destinationaddress, date, time, status, paid
                            mylist.insert(END, "Booking id: "+str(bookingid) + " /start: "+startaddress+" /dest. :" +
                                          destinationaddress+" /date: "+date+" "+time+" /status: "+status+" /paid: "+paid)
                        mylist.place(x=20, y=120, width=700, height=400)
                        scrollbar.config(command=mylist.yview)

            btncancel = Button(
                infowindow, text='Cancel \nbooking', command=entryBooking).place(x=20, y=530)
            btnrefresh = Button(
                infowindow, text='Refresh \nlist', command=refreshList).place(x=100, y=530)
        btnsubmit = Button(infowindow, text="Submit", bg='yellow',
                           font='Courier 10', command=checkBooking)
        btnsubmit.place(x=450, y=15)

    # LOG OUT FROM TBS FUNCTION

    def logout(self):
        self.destroy()
    # END

    # STRUCTURE OF MAIN TK WINDOW
    def label(self):
        self.toplabel = Label(
            self, text="Welcome to Customer Dashboard", bg="yellow", font="Courier 30")
        self.toplabel.place(x=70, y=50)

    def entry(self):
        return

    def button(self):

        self.bookbtn = Button(self, text="Book A Taxi",
                              font="Courier 15", bg="yellow", command=self.booking)
        self.bookbtn.place(x=200, y=100, width=150,
                           height=90)

        self.editbtn = Button(self, text="Edit Your Data",
                              font="Courier 15", bg="yellow", command=self.checkDetails)
        self.editbtn.place(x=380, y=100, width=250, height=90)

        self.seebtn = Button(self, text="View Your Bookings",
                             font="Courier 15", bg="yellow", command=self.seebooking)
        self.seebtn.place(x=380, y=230, width=220, height=90)

        self.logoutbtn = Button(self, text="Logout",
                                font="Courier 15", bg="yellow", command=self.logout)
        self.logoutbtn.place(x=200, y=230, width=150, height=90)
    # END


if __name__ == "__main__":
    customer1 = Customer()
    customer1.label()
    customer1.button()
    customer1.mainloop()
