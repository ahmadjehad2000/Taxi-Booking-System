from os import stat
import tkinter
from tkinter import Button, Entry, Label, Listbox, Scrollbar, Tk, messagebox
import sqlite3
from tkinter.constants import END


class Driver(Tk):
    def __init__(self):
        super().__init__()
        # =====CONNECTDB
        self.conn = sqlite3.connect('tbs.db')
        self.c = self.conn.cursor()
        # END

        # TK WINDOW ATTRIBUTES
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Driver Dashboard")
        self["bg"] = ["yellow"]
        # END

    def viewBooking(self):
        infowindow = Tk()
        infowindow.geometry("800x500+470+100")
        infowindow.resizable(False, False)
        infowindow.title("Show Bookings")
        infowindow["bg"] = ["yellow"]
        scrollbar = Scrollbar(infowindow)
        mylist = Listbox(infowindow, yscrollcommand=scrollbar.set)
        with self.conn:
            self.c.execute(
                "SELECT bookingid,customerid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE status='confirmed' OR status='completed'")
            result = self.c.fetchall()
            for bookingid, customerid, startaddress, destinationaddress, date, time, status, paid in result:
                bookingid, customerid, startaddress, destinationaddress, date, time, status, paid
                with self.conn:
                    self.c.execute("SELECT firstname,lastname FROM customers WHERE customerid=:customerid", {
                                   'customerid': customerid})
                    result = self.c.fetchall()
                    for firstname, lastname in result:
                        mylist.insert(END, "Booking id: "+str(bookingid)+" /Customer name:"+firstname+" "+lastname
                                      + " /start: "+startaddress+" /dest. :"+destinationaddress+" /date: "+date+" "+time+" /status: "+status+" /paid: "+paid)
        mylist.place(x=20, y=20, width=700, height=400)
        scrollbar.config(command=mylist.yview)

        def entryBooking():
            bookingidentry = Entry(infowindow, highlightthickness=0,
                                   bg='white', font='Courier 10', borderwidth=0)
            bookingidentry.insert(0, 'insert trip booking ID')
            bookingidentry.place(x=350, y=430, width=200, height=25)

            def paidBooking():
                with self.conn:
                    self.c.execute(
                        "SELECT * FROM bookings WHERE bookingid=:bookingid", {'bookingid': bookingidentry.get()})
                    if not self.c.fetchone():
                        message = messagebox.showerror(
                            "Error", "Booking id dont exist")
                        infowindow.lift()
                    else:
                        with self.conn:
                            self.c.execute("UPDATE bookings SET status='completed',paid='yes' WHERE bookingid=:bookingid", {
                                           'bookingid': bookingidentry.get()})
            submitbtn = Button(infowindow, text='submit', command=paidBooking)
            submitbtn.place(x=560, y=430)
        paybtn = Button(infowindow, text="completed \ntrip",
                        command=entryBooking)
        paybtn.place(x=90, y=430)

        def refreshList():
            mylist.delete(0, END)
            with self.conn:
                self.c.execute(
                    "SELECT bookingid,customerid,startaddress,destinationaddress,date,time,status,paid FROM bookings WHERE status='confirmed' OR status='completed'")
                result = self.c.fetchall()
                for bookingid, customerid, startaddress, destinationaddress, date, time, status, paid in result:
                    bookingid, customerid, startaddress, destinationaddress, date, time, status, paid
                    with self.conn:
                        self.c.execute("SELECT firstname,lastname FROM customers WHERE customerid=:customerid", {
                            'customerid': customerid})
                    result = self.c.fetchall()
                    for firstname, lastname in result:
                        mylist.insert(END, "Booking id: "+str(bookingid)+" /Customer name:"+firstname+" "+lastname
                                      + " /start: "+startaddress+" /dest. :"+destinationaddress+" /date: "+date+" "+time+" /status: "+status+" /paid: "+paid)
        mylist.place(x=20, y=20, width=700, height=400)
        scrollbar.config(command=mylist.yview)
        refreshbtn = Button(infowindow, text='Refresh \nList',
                            command=refreshList)
        refreshbtn.place(x=200, y=430)

    def logout(self):
        self.destroy()

    def label(self):
        self.toplabel = Label(
            self, text="Welcome to Driver Dashboard", bg="yellow", font="Courier 30")
        self.toplabel.place(x=70, y=50)

    def button(self):
        self.bookingbtn = Button(
            self, text='View all \nbookings', font='Courier 15', bg='yellow', command=self.viewBooking)
        self.bookingbtn.place(x=220, y=150, height=120, width=120)
        self.logoutbtn = Button(
            self, text='Log \nout', font='Courier 15', bg='yellow', command=self.logout)
        self.logoutbtn.place(x=370, y=150, height=120, width=120)

    def entry(self):
        pass


if __name__ == "__main__":
    driver = Driver()
    driver.label()
    driver.button()
    driver.entry()
    driver.mainloop()
