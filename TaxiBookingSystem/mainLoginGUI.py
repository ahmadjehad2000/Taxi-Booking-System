

from contextlib import closing
from sqlite3.dbapi2 import connect, register_adapter
from tkinter import *
from tkinter import font
from tkinter.font import BOLD
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import re
from adminGUI import Admin
from customerGUI import Customer
from driverGUI import Driver

# ================================:CLASS:=======MAIN====LOGIN=====PAGE=====


class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("TBS Login")
    # labels and canvas

    def Label(self):
        self.bgimage = PhotoImage(file='mainloginimages/bground1.png')
        self.backGroundImageLabel = Label(self, image=self.bgimage)
        self.backGroundImageLabel.place(x=0, y=0)

        self.textTaxi = Label(
            self, text="TAXI BOOKING SYSTEM", font="Courier 29", bg='yellow')
        self.textTaxi.place(x=0, y=400)

        self.canvas = Canvas(self, width=500, height=300,
                             relief=GROOVE, bg='yellow')
        self.canvas.place(x=150, y=50)

    # end

    # textboxes and entry
    def Entry(self):
        self.emailentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 20', borderwidth=0)
        self.emailentry.insert(0, 'Email')
        self.emailentry.place(x=220, y=100, width=320, height=30)
        self.passwordentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 20', borderwidth=0, show="*")
        self.passwordentry.insert(0, 'Password')
        self.passwordentry.place(x=220, y=150, width=320, height=30)

    # end
    def typeoflogin(self):
        selectedtype = StringVar()
        self.typechosen = ttk.Combobox(
            self, width=10, textvariable=selectedtype)
        self.typechosen['values'] = ('admin', 'customer', 'driver')
        self.typechosen.place(x=250, y=250)

        self.typelabel = Label(
            self, text="Choose type :", bg='yellow')
        self.typelabel.place(x=200, y=220)
    # verify login

    def verifyLogin(self):

        self.email = self.emailentry.get()
        self.password = self.passwordentry.get()
        conn = sqlite3.connect('tbs.db')
        c = conn.cursor()
        if self.typechosen.get() == "customer":
            with conn:
                c.execute("SELECT email FROM customers WHERE email=:email AND password=:password", {
                    'email': self.email, 'password': self.password})
            if not c.fetchone():
                message = messagebox.showerror(
                    "Customer Login", f"Login failed! email or password is wrong")
            else:
                with conn:
                    c.execute("SELECT customerid FROM customers where email=:email", {
                              'email': self.email})
                    for value in c.fetchone():
                        value
                message = messagebox.showinfo(
                    "Customer Login", f"Your ID is {value}")
                # Start CUSTOMERGUI
                customer = Customer()
                customer.label()
                customer.button()
                customer.entry()
                customer.mainloop()
                # Start CUSTOMERGUI
        elif self.typechosen.get() == "driver":
            with conn:
                c.execute("SELECT email FROM drivers WHERE email=:email AND password=:password", {
                          'email':  self.email, 'password': self.password})
            if not c.fetchone():
                message = messagebox.showerror(
                    "Driver Login", f"Login failed! email or password is wrong")
            else:

                message = messagebox.showinfo(
                    "Driver Login", f"Login Succeeded!")
                driver = Driver()
                driver.label()
                driver.entry()
                driver.button()
                driver.mainloop()
        elif self.typechosen.get() == "admin":
            with conn:
                c.execute("SELECT email FROM admins WHERE email=:email AND password=:password", {
                          'email':  self.email, 'password': self.password})
            if not c.fetchone():
                message = messagebox.showerror(
                    "Admin Login", f"Login failed! email or password is wrong")
            else:
                message = messagebox.showinfo(
                    "Admin Login", f"Login Succeeded!")
                admin = Admin()
                admin.label()
                admin.entry()
                admin.button()
                admin.mainloop()

        else:
            message = messagebox.showerror(
                "Login Error", "Please choose the type of login")
            #   end

    def typeWindow(self):
        if self.typechosen.get() == "customer":
            register = CustomerRegister()
            register.LabelFirstPage()
            register["bg"] = ["yellow"]
            register.ButtonFirstPage()
            register.mainloop()
        elif self.typechosen.get() == "driver":
            driver = driverRegister()
            driver.Label()
            driver.Entry()
            driver.Button()
            driver.mainloop()
        elif self.typechosen.get() == "admin":
            admin = adminRegister()
            admin.Label()
            admin.Entry()
            admin.Button()
            admin.mainloop()
        else:
            message = messagebox.showinfo("Type", 'choose a type')

    def Button(self):

        self.loginimage = PhotoImage(file='mainloginimages/login.png')
        self.loginButton = Button(
            self, image=self.loginimage, command=self.verifyLogin, border=0, relief=GROOVE)
        self.loginButton.place(x=420, y=200)

        self.registerimage = PhotoImage(file='mainloginimages/register.png')
        self.registerButton = Button(
            self, image=self.registerimage, command=self.typeWindow, border=0, relief=GROOVE)

        self.registerButton.place(x=420, y=270)
    # end

    # def getCurrentCustomerId(self):
    #     conn = sqlite3.connect('tbs.db')
    #     c = conn.cursor()
    #     with conn:
    #         c.execute(
    #             "SELECT customerid FROM customers WHERE email=:email AND password=:password", {'email': self.emailentry.get(), 'password': self.passwordentry.get()})

    #         ("SELECT customerid FROM customers WHERE email=:email AND password=:password", {
    #          'email': email, 'password': password})
        # return int("SELECT customerid FROM customers WHERE email=:email AND password=:password", {'email': email, 'password': password)

# ================================:CLASS:=======CUSTOMER====REGISTER=====PAGE=====


class CustomerRegister(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Customer Register 1")

    def LabelFirstPage(self):
        self.toplabel = Label(
            self, text="   Customer Register in TBS ", font='Courier 20', bg='yellow')
        self.toplabel.place(x=100, y=10)

        self.customerid = Entry(
            self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.customerid.insert(0, 'Customer ID')
        self.customerid.place(x=220, y=50, width=290, height=30)
        self.firstnameentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.firstnameentry.insert(0, 'First Name')
        self.firstnameentry.place(x=220, y=100, width=290, height=30)

        self.lastnameentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.lastnameentry.insert(0, 'Last Name')
        self.lastnameentry.place(x=220, y=150, width=290, height=30)

        # self.usernameentry = Entry(
        #     self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        # self.usernameentry.insert(0, 'Username')
        # self.usernameentry.place(x=220, y=200, width=290, height=30)

        self.emailentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.emailentry.insert(0, 'Email')
        self.emailentry.place(x=220, y=250, width=290, height=30)

        self.telentry = Entry(self, highlightthickness=0,
                              bg='white', font='Courier 10', borderwidth=0)
        self.telentry.insert(0, 'Telephone No.')
        self.telentry.place(x=220, y=300, width=290, height=30)

        self.passwordentry = Entry(
            self, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.passwordentry.insert(0, 'Password')

        self.passwordentry.place(x=220, y=350, width=290, height=30)

    def NextWindow(self):

        registerwindow2 = Toplevel()
        registerwindow2.geometry("800x500+470+100")
        registerwindow2.title("Register 2")
        registerwindow2.resizable(False, False)
        registerwindow2["bg"] = ["yellow"]

        # ===============REGEX CHECK
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, self.emailentry.get())):
            pass
        else:
            error = messagebox.showwarning(
                'error', 'email is not valid')
            self.lift()
        # ===============REGEX CHECK

        town = ['Town1', 'Town2', 'Town3', 'Town4']
        county = ['County1', 'County2', 'County3', 'County4']

        self.selectedTown = StringVar()
        self.selectedTown.set('Town1')
        self.selectedpayment = StringVar()
        self.selectedpayment.set("Cash")
        self.selectedCounty = StringVar()
        self.selectedCounty.set('County1')

        self.townlabel = Label(
            registerwindow2, text="Choose Your Town :", font='Courier 15', bg='yellow')
        self.townlabel.place(x=180, y=100)

        self.countylabel = Label(
            registerwindow2, text="Choose Your County :", font='Courier 15', bg='yellow')
        self.countylabel.place(x=155, y=150)

        self.dropTown = OptionMenu(
            registerwindow2, self.selectedTown, *town)
        self.dropTown.place(x=410, y=95)

        self.dropCounty = OptionMenu(
            registerwindow2, self.selectedCounty, *county)
        self.dropCounty.place(x=410, y=140)

        self.postcodelabel = Label(
            registerwindow2, text="Enter PostCode:", font='Courier 15', bg='yellow')
        self.postcodelabel.place(x=155, y=200)
        self.postcodeentry = Entry(
            registerwindow2, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.postcodeentry.insert(0, 'Post Code')
        self.postcodeentry.place(x=345, y=200, height=20, width=200)

        self.addresslabel = Label(
            registerwindow2, text="Enter your address:", font='Courier 15', bg='yellow')
        self.addresslabel.place(x=100, y=230)
        self.addressentry = Entry(
            registerwindow2, highlightthickness=0, bg='white', font='Courier 10', borderwidth=0)
        self.addressentry.insert(0, 'Address')
        self.addressentry.place(x=345, y=230, height=20, width=280)

        self.checkpaymentlabel = Label(
            registerwindow2, text="Check your payment method: ", bg='yellow', font='Courier 20')
        self.checkpaymentlabel.place(x=140, y=280)

        self.checkCash = Checkbutton(
            registerwindow2, text="Cash", variable=self.selectedpayment, onvalue="Cash", bg='yellow')
        self.checkCash.place(x=200, y=320)

        self.checkCredit = Checkbutton(
            registerwindow2, text="Credit", variable=self.selectedpayment, onvalue="Credit", bg='yellow')
        self.checkCredit.place(x=260, y=320)

        def insertCustomer():
            conn = sqlite3.connect('tbs.db')
            c = conn.cursor()
            with conn:
                c.execute("""INSERT INTO customers VALUES(:customerid,:title,:firstname,:lastname
                    ,:email,:telno,:password,:address1,:town,:county,:postcode,:paymentmethod)""", {'customerid': int(self.customerid.get()), 'title': 'customer', 'firstname': self.firstnameentry.get(), 'lastname': self.lastnameentry.get(), 'email': self.emailentry.get(), 'telno': self.telentry.get(), 'password': self.passwordentry.get(), 'address1': self.addressentry.get(), 'town': self.selectedTown.get(), 'county': self.selectedCounty.get(), 'postcode': self.postcodeentry.get(), 'paymentmethod': self.selectedpayment.get()})

        def Details():
            infoWindow = Tk()
            infoWindow.geometry("800x300+470+200")
            infoWindow.resizable(False, False)
            infoWindow.title("Info")
            infoWindow['bg'] = ['yellow']
            # self.showusername = Label(
            #     infoWindow, text="Username:"+self.usernameentry.get(), bg='yellow').grid(row=0, column=1)
            self.showemail = Label(
                infoWindow, text="Email:"+self.emailentry.get(), bg='yellow').grid(row=1, column=1)
            self.showaddress = Label(
                infoWindow, text="Address:"+self.addressentry.get(), bg='yellow').grid(row=2, column=1)
            self.showtown = Label(
                infoWindow, text="Town:"+self.selectedTown.get(), bg='yellow').grid(row=3, column=1)
            self.showcounty = Label(
                infoWindow, text="County:"+self.selectedCounty.get(), bg='yellow').grid(row=4, column=1)
            self.showfirst = Label(
                infoWindow, text="First name:"+self.firstnameentry.get(), bg='yellow').grid(row=5, column=1)
            self.showlast = Label(
                infoWindow, text="Last name:"+self.lastnameentry.get(), bg='yellow').grid(row=6, column=1)
            self.showtel = Label(
                infoWindow, text="Tel No.:"+self.telentry.get(), bg='yellow').grid(row=7, column=1)
            self.showpass = Label(
                infoWindow, text="Password:"+self.passwordentry.get(), bg='yellow').grid(row=8, column=1)
            self.showpost = Label(
                infoWindow, text="Post:"+self.postcodeentry.get(), bg='yellow').grid(row=9, column=1)
            self.showpayment = Label(
                infoWindow, text="Payment:"+self.selectedpayment.get(), bg='yellow').grid(row=10, column=1)
            self.showid = Label(
                infoWindow, text="ID:"+self.customerid.get(), bg='yellow').grid(row=11, column=1)

            self.labeldisc = Label(
                infoWindow, text='is this information Valid?', font='Courier 10', bg='yellow')
            self.labeldisc.place(x=20, y=250)
            self.yesbutton = Button(
                infoWindow, text="Yes", command=lambda: [infoWindow.destroy(), insertCustomer(), registerwindow2.destroy(), self.destroy()])
            self.yesbutton.place(x=250, y=250)

            self.nobutton = Button(infoWindow, text="No",
                                   command=lambda: [infoWindow.destroy(), self.lift()])
            self.nobutton.place(x=300, y=250)

        self.confirmbutton = Button(
            registerwindow2, text="Confirm Registration", command=Details)
        self.confirmbutton.place(
            x=550, y=350, height=50, width=150, anchor=E)

    def ButtonFirstPage(self):
        self.nextpage = Button(self, text="Next Page",
                               command=self.NextWindow)
        self.nextpage.place(x=220, y=400)
# ================================:CLASS:=======CUSTOMER====REGISTER=====PAGE=====


# ================================:CLASS:=======DRIVER====REGISTER=====PAGE=======
class driverRegister(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Driver")
        self["bg"] = ["yellow"]

    def Label(self):
        self.toplabel = Label(
            self, text="Driver registration in TBS", font="Courier 25", bg='yellow')
        self.toplabel.place(x=120, y=20)

    def Entry(self):
        self.id = Entry(self, highlightthickness=0,
                        bg='white', font='Courier 10', borderwidth=0)
        self.id.insert(0, "Driver id")
        self.id.place(x=200, y=80, height=30, width=300)

        # self.username = Entry(self, highlightthickness=0,
        #                       bg='white', font='Courier 10', borderwidth=0)
        # self.username.insert(0, "Username")
        # self.username.place(x=200, y=120, height=30, width=300)

        self.firstname = Entry(self, highlightthickness=0,
                               bg='white', font='Courier 10', borderwidth=0)
        self.firstname.insert(0, "First name")
        self.firstname.place(x=200, y=160, height=30, width=300)

        self.lastname = Entry(self, highlightthickness=0,
                              bg='white', font='Courier 10', borderwidth=0)
        self.lastname.insert(0, "Last name")
        self.lastname.place(x=200, y=200, height=30, width=300)

        self.email = Entry(self, highlightthickness=0,
                           bg='white', font='Courier 10', borderwidth=0)
        self.email.insert(0, "Email")
        self.email.place(x=200, y=240, height=30, width=300)

        self.password = Entry(self, highlightthickness=0,
                              bg='white', font='Courier 10', borderwidth=0)
        self.password.insert(0, "Password")
        self.password.place(x=200, y=280, height=30, width=300)

        self.regno = Entry(self, highlightthickness=0,
                           bg='white', font='Courier 10', borderwidth=0)
        self.regno.insert(0, "RegNo")
        self.regno.place(x=200, y=320, height=30, width=300)

    def check(self):
        # regex
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, self.email.get())):
            self.showDetails()
        else:
            error = messagebox.showwarning(
                'error', 'email is not valid')
        self.lift()
        # regex

    def insertDriver(self):
        conn = sqlite3.connect('tbs.db')
        c = conn.cursor()
        with conn:
            c.execute("""INSERT INTO drivers VALUES(:driverid, :title, :firstname
            , :lastname, :email, :password, :regno)""", {'driverid': int(self.id.get()), 'title': 'driver',  'firstname': self.firstname.get(), 'lastname': self.lastname.get(), 'email': self.email.get(), 'password': self.password.get(), 'regno': self.regno.get()})

    def showDetails(self):
        # NEW WINDOW
        infoWindow = Tk()
        infoWindow.geometry("800x300+470+200")
        infoWindow.resizable(False, False)
        infoWindow.title("Info")
        infoWindow['bg'] = ['yellow']
        # NEW WINDOW

        # =======DISPLAYS YOUR INPUT TO CHECK IT
        self.idlabel = Label(infoWindow, text="ID: "+self.id.get(), bg='yellow'
                             ).grid(row=1, column=1)
        # self.userlabel = Label(
        #     infoWindow, text="username: "+self.username.get(), bg='yellow').grid(row=2, column=1)
        self.fnamelabel = Label(
            infoWindow, text="firstname: "+self.firstname.get(), bg='yellow').grid(row=3, column=1)
        self.lnamelabel = Label(
            infoWindow, text="lastname: "+self.lastname.get(), bg='yellow').grid(row=4, column=1)
        self.emaillabel = Label(
            infoWindow, text="email: "+self.email.get(), bg='yellow').grid(row=5, column=1)
        self.passwordlabel = Label(
            infoWindow, text="password: "+self.password.get(), bg='yellow').grid(row=6, column=1)
        self.regnolabel = Label(
            infoWindow, text="regno: "+self.regno.get(), bg='yellow').grid(row=7, column=1)
        self.ask = Label(
            infoWindow, text="Is this information valid? ", bg='yellow', font="Courier 10")
        self.ask.place(x=90, y=200)
        # =======DISPLAYS YOUR INPUT TO CHECK IT

        # =============BUTTONS TO ASK ABOUT INFO
        self.buttonYes = Button(infoWindow, text="Yes", command=lambda: [
            infoWindow.destroy(), self.insertDriver(), self.destroy()]).place(x=320, y=200)
        self.buttonNo = Button(infoWindow, text="No",
                               command=infoWindow.destroy).place(x=380, y=200)
        # =============BUTTON TO ASK ABOUT INFO

    def Button(self):
        self.registerbutton = Button(
            self, text='Confirm Registration', command=self.check)
        self.registerbutton.place(x=200, y=380)

# ================================:CLASS:=======DRIVER====REGISTER=====PAGE=======

# ================================:CLASS:=======ADMIN====REGISTER=====PAGE=======


class adminRegister(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500+470+100")
        self.resizable(False, False)
        self.title("Admin")
        self["bg"] = ["yellow"]

    def Label(self):
        self.toplabel = Label(
            self, text="Admin registration in TBS", font="Courier 25", bg='yellow')
        self.toplabel.place(x=120, y=20)

    def Entry(self):
        self.id = Entry(self, highlightthickness=0,
                        bg='white', font='Courier 10', borderwidth=0)
        self.id.insert(0, "Admin id")
        self.id.place(x=200, y=80, height=30, width=300)

        # self.username = Entry(self, highlightthickness=0,
        #                       bg='white', font='Courier 10', borderwidth=0)
        # self.username.insert(0, "Username")
        # self.username.place(x=200, y=120, height=30, width=300)

        self.firstname = Entry(self, highlightthickness=0,
                               bg='white', font='Courier 10', borderwidth=0)
        self.firstname.insert(0, "First name")
        self.firstname.place(x=200, y=160, height=30, width=300)

        self.lastname = Entry(self, highlightthickness=0,
                              bg='white', font='Courier 10', borderwidth=0)
        self.lastname.insert(0, "Last name")
        self.lastname.place(x=200, y=200, height=30, width=300)

        self.email = Entry(self, highlightthickness=0,
                           bg='white', font='Courier 10', borderwidth=0)
        self.email.insert(0, "Email")
        self.email.place(x=200, y=240, height=30, width=300)

        self.password = Entry(self, highlightthickness=0,
                              bg='white', font='Courier 10', borderwidth=0)
        self.password.insert(0, "Password")
        self.password.place(x=200, y=280, height=30, width=300)

    def check(self):
        # regex
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, self.email.get())):
            self.showDetails()
        else:
            error = messagebox.showwarning(
                'error', 'email is not valid')
        self.lift()
        # regex

    def insertAdmin(self):
        conn = sqlite3.connect('tbs.db')
        c = conn.cursor()
        with conn:
            c.execute("""INSERT INTO admins VALUES(:adminid,:firstname,:lastname,:email,:password)""", {'adminid': int(self.id.get()),
                                                                                                        'firstname': self.firstname.get(), 'lastname': self.lastname.get(), 'email': self.email.get(), 'password': self.password.get()})
            # with conn:
            #     c.execute("""SELECT adminid FROM admins""")
            #     if c.fetchone():
            #         error = messagebox.showwarning(
            #             'error', 'username is not taken')
            #     else:
            #         pass

    def showDetails(self):
        # NEW WINDOW
        infoWindow = Tk()
        infoWindow.geometry("800x300+470+200")
        infoWindow.resizable(False, False)
        infoWindow.title("Info")
        infoWindow['bg'] = ['yellow']
        # NEW WINDOW

        # =======DISPLAYS YOUR INPUT TO CHECK IT
        self.idlabel = Label(infoWindow, text="ID: "+self.id.get(), bg='yellow'
                             ).grid(row=1, column=1)
        # self.userlabel = Label(
        #     infoWindow, text="username: "+self.username.get(), bg='yellow').grid(row=2, column=1)
        self.fnamelabel = Label(
            infoWindow, text="firstname: "+self.firstname.get(), bg='yellow').grid(row=3, column=1)
        self.lnamelabel = Label(
            infoWindow, text="lastname: "+self.lastname.get(), bg='yellow').grid(row=4, column=1)
        self.emaillabel = Label(
            infoWindow, text="email: "+self.email.get(), bg='yellow').grid(row=5, column=1)
        self.passwordlabel = Label(
            infoWindow, text="password: "+self.password.get(), bg='yellow').grid(row=6, column=1)

        self.ask = Label(
            infoWindow, text="Is this information valid? ", bg='yellow', font="Courier 10")
        self.ask.place(x=90, y=200)
        # =============BUTTONS TO ASK ABOUT INFO
        self.buttonYes = Button(infoWindow, text="Yes", command=lambda: [
            infoWindow.destroy(), self.insertAdmin(), self.destroy()]).place(x=320, y=200)
        self.buttonNo = Button(infoWindow, text="No",
                               command=infoWindow.destroy).place(x=380, y=200)
        # =============BUTTON TO ASK ABOUT INFO

    def Button(self):
        self.registerbutton = Button(
            self, text='Confirm Registration', command=self.check)
        self.registerbutton.place(x=200, y=380)


# ================================:CLASS:=======ADMIN====REGISTER=====PAGE=======
if __name__ == "__main__":
    login = Login()
    login.Label()
    login.Button()
    login.Entry()
    login.typeoflogin()
    login.mainloop()
