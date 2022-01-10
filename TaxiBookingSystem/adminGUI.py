from os import stat
from tkinter import messagebox
from tkinter import *
import re
import sqlite3
from tkinter import font
from typing import ChainMap


# =================================THIS IS DASHBOARD CLASS FOR ADMIN========
class Admin(Tk):
    def __init__(self):
        super().__init__()

        # =====CONNECTDB
        self.conn = sqlite3.connect('tbs.db')
        self.c = self.conn.cursor()
        # END

        # TK WINDOW ATTRIBUTES
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Admin Dashboard")
        self["bg"] = ["yellow"]
        # END

    def pendingBooking(self):
        infowindow = Tk()
        infowindow.geometry("800x500+470+100")
        infowindow.resizable(False, False)
        infowindow.title("Pending Booking")
        infowindow["bg"] = ["yellow"]
        scrollbar = Scrollbar(infowindow)
        mylist = Listbox(infowindow, yscrollcommand=scrollbar.set)
        scrollbar2 = Scrollbar(infowindow)
        mylist2 = Listbox(infowindow, yscrollcommand=scrollbar.set)
        with self.conn:
            self.c.execute(
                "SELECT bookingid,startaddress,destinationaddress,date,time FROM bookings WHERE status='pending'")
            result = self.c.fetchall()
            lbl = Label(mylist)
            mylist.insert(END, 'Pending Bookings :')
            for bookingid, start, dest, date, time in result:
                bookingid, start, dest, date, time
                mylist.insert(END, "Booking id: "+str(bookingid)+" /StartAddress: "+start+" /DestAddress: "+dest
                              + " /Date: "+date+" "+time)
            mylist.place(x=5, y=20, width=400, height=400)
            scrollbar.config(command=mylist.yview)

            with self.conn:
                self.c.execute(
                    "SELECT driverid,firstname,lastname,email FROM drivers")
                result = self.c.fetchall()
                lbl = Label(mylist)
                mylist2.insert(END, 'Registered Drivers :')
            for driverid, firstname, lastname, email in result:
                driverid, firstname, lastname, email
                mylist2.insert(END, "Driver id: "+str(driverid)+" /firstname : "+firstname+" /lastname: "+lastname
                               + " /Email: "+email)
            mylist2.place(x=430, y=20, width=350, height=400)
            scrollbar2.config(command=mylist.yview)

            def entryDriver():
                bookingidentry = Entry(infowindow, highlightthickness=0,
                                       bg='white', font='Courier 9', borderwidth=0)
                bookingidentry.insert(
                    0, 'insert booking id you want to allocate')
                bookingidentry.place(x=320, y=430, width=290)

                driveridentry = Entry(infowindow, highlightthickness=0,
                                      bg='white', font='Courier 9', borderwidth=0)
                driveridentry.insert(
                    0, 'insert driver id')
                driveridentry.place(x=320, y=450, width=250)

                def allocateDriver():
                    with self.conn:
                        self.c.execute(
                            "SELECT * FROM drivers WHERE driverid=:driverid", {'driverid': driveridentry.get()})
                        if not self.c.fetchone():
                            message = messagebox.showerror(
                                "Error", "Driver dont exist")
                            infowindow.lift()
                        else:
                            with self.conn:
                                self.c.execute(
                                    "SELECT * FROM bookings WHERE bookingid=:bookingid", {'bookingid': bookingidentry.get()})
                            if not self.c.fetchone():
                                message = messagebox.showerror(
                                    "Error", "Booking dont exist")
                                infowindow.lift()
                            else:
                                with self.conn:
                                    self.c.execute("UPDATE bookings SET driverid=:driverid,status='confirmed' WHERE bookingid=:bookingid", {
                                                   'driverid': int(driveridentry.get()), 'bookingid': int(bookingidentry.get())})
                submitbtn = Button(infowindow, text='submit',
                                   command=allocateDriver)
                submitbtn.place(x=630, y=435)

            def refreshList():
                mylist.delete(0, END)
                with self.conn:
                    self.c.execute(
                        "SELECT bookingid,startaddress,destinationaddress,date,time FROM bookings WHERE status='pending'")
                result = self.c.fetchall()
                lbl = Label(mylist)
                mylist.insert(END, 'Pending Bookings :')
                for bookingid, start, dest, date, time in result:
                    bookingid, start, dest, date, time
                    mylist.insert(END, "Booking id: "+str(bookingid)+" /StartAddress: "+start+" /DestAddress: "+dest
                                  + " /Date: "+date+" "+time)
                mylist.place(x=5, y=20, width=400, height=400)
                scrollbar.config(command=mylist.yview)

                with self.conn:
                    self.c.execute(
                        "SELECT driverid,firstname,lastname,email FROM drivers")
                result = self.c.fetchall()
                lbl = Label(mylist)
                mylist2.insert(END, 'Registered Drivers :')
                for driverid, firstname, lastname, email in result:
                    driverid, firstname, lastname, email
                mylist2.insert(END, "Driver id: "+str(driverid)+" /firstname : "+firstname+" /lastname: "+lastname
                               + " /Email: "+email)
                mylist2.place(x=430, y=20, width=350, height=400)
                scrollbar2.config(command=mylist.yview)

            def cancelEntry():
                identry = Entry(infowindow, highlightthickness=0,
                                bg='white', font='Courier 9', borderwidth=0)
                identry.insert(0, 'insert booking id of trip to    Cancel')
                identry.place(x=320, y=430, width=290)

                canceldentry = Entry(infowindow, highlightthickness=0,
                                     bg='yellow', font='Courier 9', borderwidth=0)
                canceldentry.place(x=320, y=450, width=250)

                def cancelBooking():
                    with self.conn:
                        self.c.execute("SELECT status FROM bookings where bookingid=:bookingid", {
                                       'bookingid': identry.get()})
                        result = self.c.fetchone()
                        for status in result:
                            if status == "cancelled" or status == "completed":
                                message = messagebox.showerror(
                                    "Error", "you cannot cancel this trip")
                                infowindow.lift()
                            else:
                                with self.conn:
                                    self.c.execute("UPDATE bookings SET status='cancelled' WHERE bookingid=:bookingid", {
                                        'bookingid': int(identry.get())})

                submitbtn = Button(infowindow, text='submit',
                                   command=cancelBooking)
                submitbtn.place(x=630, y=435)
            allocatebtn = Button(
                infowindow, text="Allocate Booking to \ndriver", command=entryDriver)
            allocatebtn.place(x=30, y=430)
            cancelbtn = Button(
                infowindow, text='Cancel \nBooking', command=cancelEntry)
            cancelbtn.place(x=160, y=430)
            refreshbtn = Button(
                infowindow, text='Refresh \nList', command=refreshList)
            refreshbtn.place(x=230, y=430)

    def showBooking(self):
        infowindow = Tk()
        infowindow.geometry("800x500+470+100")
        infowindow.resizable(False, False)
        infowindow.title("Show Bookings")
        infowindow["bg"] = ["yellow"]
        scrollbar = Scrollbar(infowindow)
        mylist = Listbox(infowindow, yscrollcommand=scrollbar.set)
        with self.conn:
            self.c.execute(
                "SELECT bookingid,driverid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE status='cancelled' OR status='confirmed' OR status='completed'")
            result = self.c.fetchall()
            for bookingid, driverid, start, dest, date, time, status, paid in result:
                bookingid, driverid, start, dest, date, time, status, paid
                mylist.insert(END, "Booking id: "+str(bookingid)+"  /StartAddress: "+start+"  /DestAddress: "+dest
                              + "  /Date: "+date+" "+time+" /status: "+status+" /booked to:"+str(driverid)+" /paid "+paid)
            mylist.place(x=20, y=20, width=900, height=400)
            scrollbar.config(command=mylist.yview)

            def refreshList():
                mylist.delete(0, END)
                with self.conn:
                    self.c.execute(
                        "SELECT bookingid,driverid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE status='cancelled' OR status='confirmed' OR status='completed'")
                    result = self.c.fetchall()
                    for bookingid, driverid, start, dest, date, time, status, paid in result:
                        bookingid, driverid, start, dest, date, time, status, paid
                        mylist.insert(END, "Booking id: "+str(bookingid)+" /StartAddress: "+start+" /DestAddress: "+dest
                                      + " /Date: "+date+" "+time+" /status: "+status+" /booked to:"+str(driverid)+" /paid "+paid)
            mylist.place(x=20, y=20, width=700, height=400)
            scrollbar.config(command=mylist.yview)

            refreshbtn = Button(
                infowindow, text='Refresh list', command=refreshList)
            refreshbtn.place(x=590, y=430)

    def logout(self):
        self.destroy()
    # STRUCTURE OF MAIN TK WINDOW

    def label(self):
        self.toplabel = Label(
            self, text="Welcome to Admin Dashboard", bg="yellow", font="Courier 30")
        self.toplabel.place(x=70, y=50)

    def button(self):
        pendingBookingBtn = Button(
            self, text='Show \nPending Bookings', font='Courier 15', bg='yellow', command=self.pendingBooking)
        pendingBookingBtn.place(x=120, y=90, height=100, width=250)

        viewBookingBtn = Button(
            self, text='Show All Bookings', font='Courier 15', bg='yellow', command=self.showBooking)
        viewBookingBtn.place(x=390, y=90, height=100, width=250)

        logoutBookingBtn = Button(
            self, text='Log out', font='Courier 15', bg='yellow', command=self.logout)
        logoutBookingBtn.place(x=120, y=210, height=100, width=250)

    def entry(self):
        pass
    # END


if __name__ == "__main__":
    admin = Admin()
    admin.label()
    admin.button()
    admin.entry()
    admin.mainloop()
