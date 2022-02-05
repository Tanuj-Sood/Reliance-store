import mysql.connector as con
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

db=con.connect(host='localhost',user='root',passwd='12345')
cur=db.cursor()

"""

These try and except block provides a uninterrupted workflow of the program as they create the tables and database automatically
if it does not exist on the mysql server on which the following program is running

"""
#cur.execute("drop database reliancestore")
try:
    cur.execute("create database Reliancestore")
    cur.execute("use Reliancestore")
    cur.execute("create table user(Username varchar(20),Password varchar(20))")
    cur.execute("create table reciept(Pcode varchar(5) PRIMARY KEY,Pname varchar(20),quantity varchar(10),price varchar(5))")
    cur.execute("create table customer(Pcode varchar(5) PRIMARY KEY,Pname varchar(20),quantity varchar(10),price varchar(5))")
    cur.execute("insert into user values(%s,%s)",("admin007","0075RXT"))
    db.commit()
    cur.execute("create table totalsales(Cust_Name varchar(20),Amount varchar(7))")
    cur.execute("create table stock(Pcode varchar(5) PRIMARY KEY,Pname varchar(20),quantity varchar(10),price varchar(5))")

    # Entering default 5 products in the product list

    products=["Rin","Vimbar","Butter(500g)","Fogg Perfume","Colgate"]
    Price=["175","40","220","250","142"]
    qty=10
    for i in range(0,6):
        x=products[i]
        y=Price[i]
        cur.execute("insert into stock values(%s,%s,%s,%s)",(str(i+1),x,qty,y))
        db.commit()
except:

    #using the database and tables if they already exists
    
    cur.execute("use Reliancestore")


try:
    
    """
    Deleting and recreating the customer oriented tables so that the cart remains empty over the successive runs of the program
    on the same machine
    """

    cur.execute("drop table reciept")
    cur.execute("create table reciept(Pcode varchar(5) PRIMARY KEY,Pname varchar(20),quantity varchar(10),price varchar(5))")
    cur.execute("drop table customer")
    cur.execute("create table customer(Pcode varchar(5) PRIMARY KEY,Pname varchar(20),quantity varchar(10),price varchar(5))")

except:
    pass




##############         FUNCTIONING OF THE DATABASE      ####################



"""
Documentation of the program:-
These are the functions we will be using for manipulating the data in our database which is stored in various tables according to the
need of the hour...

The project is all about what a customer/admin will come across while using an application of a shopping store.. Aim of Using Tkinter
is to provide the program a feel of using a real application

"""

def insert():
    global v1
    global v2
    global v3
    global v4


    cd=v1.get()
    nm=v2.get()
    qty=v3.get()
    pr=v4.get()

    cur.execute("select quantity from stock where Pcode={}".format(str(cd)))
 
    rec=cur.fetchall()
    sqty=rec[0]

    if(qty!=''):
        if (int(qty)>0 and int(qty)<int(sqty[0])):
            cur.execute("insert into reciept values (%s,%s,%s,%s)",(cd,nm,qty,pr))
            cur.execute("insert into customer values (%s,%s,%s,%s)",(cd,nm,qty,pr))
            db.commit()
            messagebox.showinfo("Reliance Store ","Succesful!")
        elif(int(qty)>int(sqty[0])):
            messagebox.showinfo("Reliance Store ","Sorry. We have inadequate stocks")
        else:
            messagebox.showinfo("Reliance Store ","Please set the quantity to atleast 1")
    else:
        messagebox.showinfo("Reliance Store ","Quantity is a mandatory field and cannot be left empty")
       
def search():
    global v1
    global v2
    global v3
    global v4
    
    Pcode=v1.get()
    sql="select * from stock where Pcode=%s"
    val=(Pcode,)
    cur.execute(sql,val)
    res=cur.fetchall()
    for x in res:
        v2.set(x[1])
        v4.set(x[3])
        
def search1():
    global v1
    global v2
    global v3
    global v4
    
    Pcode=v1.get()
    sql="select * from reciept where Pcode=%s"
    val=(Pcode,)
    cur.execute(sql,val)
    res=cur.fetchall()
    for x in res:
        v2.set(x[1])
        v4.set(x[3])


def update():
    global v1
    global v2
    global v3
    global v4
    
    cd=v1.get()
    nm=v2.get()
    qty=v3.get()
    pr=v4.get()
    sql1="update reciept set Pname=%s,quantity=%s,price=%s where Pcode=%s"
    sql="update customer set Pname=%s,quantity=%s,price=%s where Pcode=%s"
    val=(nm,qty,pr,cd)
    cur.execute(sql,val)
    cur.execute(sql1,val)
    db.commit()
    messagebox.showinfo("Reliance Store","Updation of records will be highlited when you again visit this section")

def delete():
    global v1
    global v2
    global v3
    global v4
    
    cd=v1.get()
    sql="delete from customer where Pcode=%s"
    sql2="delete from reciept where Pcode=%s"
    val=(cd,)
    cur.execute(sql,val)
    cur.execute(sql2,val)
    db.commit()
    messagebox.showinfo("Reliance Store","deletion of records will be highlited when you again visit this section")

def clear():
    global v1
    global v2
    global v3
    global v4
    
    v1.set('')
    v2.set('')
    v3.set('')
    v4.set('')
    
def back():
    global root1
    global root
    global P1
    global P2
    global img
    global img2

    root1.destroy()

    root=Tk()
    root.geometry("500x500+70+100")
    root.title("RELIANCE STORE")
    root.iconbitmap("ICON.ico")
    

    img = PhotoImage(file="Background.png",master=root)
    img2= PhotoImage(file="LOGO.png",master=root)
    Label(root,image=img).place(x=0,y=0)
    Label(root,image=img2).place(x=50,y=0)
    Label(root,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root,text="Hey There! Welcome To Reliance Store",font="arial 14 bold").place(x=60,y=140)
    Label(root,text="How do you wish to continue?",font="arial 14 bold").place(x=100,y=180)

    P1= PhotoImage(file="Admin.png",master=root)
    P2= PhotoImage(file="customer.png",master=root)

    Button(root,text="ADMIN",command=admin, image= P1).place(x=90,y=230)

    Label(root,text="Admin",font="arial 14 bold").place(x=104,y=333)

    Button(root,text="CUSTOMER",command=customer,image= P2).place(x=265,y=227)
    Label(root,text="Customer",font="arial 14 bold").place(x=296,y=336)

    Button(root,text="EXIT",command=exit).place(x=420,y=470)


def exit():
    global root
    
    messagebox.showinfo("EXIT","Thanks For Using Our Application")
    root.destroy()
    
def exitt():
    global root2
    global v1
    global Gt

    name= v1.get()

    if (name=="" or name==" "):
        messagebox.showinfo("Reliance Store","Mandatory (*) Fields cannot be empty")
    else:
        cur.execute("insert into totalsales values(%s,%s)",(name,Gt))
        db.commit()
        messagebox.showinfo("EXIT","Thanks For Shopping with us")
        root2.destroy()
    
    


#########################       CUSTOMER VIEW STARTS HERE      ###########################
    
"""
This is the customer view.. In this section we will be dealing with what a customer can do on/with our program.. providing features
to the customer is the sole purpose of this section... PS- please start reading from the bottom where this section ends as the views
are created backwards starting from the very first "customer" function from the bottom of this section...

"""


def Goback():
    global root2
    global root3
    global root1
    global img
    global img2
    
    try:
        root3.destroy()
        root2.destroy()
        
        root1=Tk()
        root1.geometry("500x500+70+100")
        root1.title("Customer")
        root1.iconbitmap("ICON.ico")
        
        img = PhotoImage(file="Background.png",master=root1)
        img2= PhotoImage(file="LOGO.png",master=root1)
        Label(root1,image=img).place(x=0,y=0)
        Label(root1,image=img2).place(x=50,y=0)
        Label(root1,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

        Label(root1,text="WHAT DO YOU WANT TO DO?",font="arial 14 bold").place(x=100,y=200)
        
        Button(root1,text="ADD TO CART FROM PRODUCT LIST",command=insertscr).place(x=15,y=260)
        Button(root1,text="DELETE FROM CART",command=deletescr).place(x=370,y=260)
        Button(root1,text="UPDATE FIELD OF EXISTING PRODUCT",command=updatescr).place(x=15,y=300)
        Button(root1,text="SHOW CART",command=showscr).place(x=370,y=300)
        Button(root1,text="Proceed for billing",command=billing).place(x=200,y=370)
        Button(root1,text="Go Back",command=back).place(x=420,y=470)

    except:
        root2.destroy()
        
        root1=Tk()
        root1.geometry("500x500+70+100")
        root1.title("Customer")
        root1.iconbitmap("ICON.ico")
        
        img = PhotoImage(file="Background.png",master=root1)
        img2= PhotoImage(file="LOGO.png",master=root1)
        Label(root1,image=img).place(x=0,y=0)
        Label(root1,image=img2).place(x=50,y=0)
        Label(root1,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

        Label(root1,text="WHAT DO YOU WANT TO DO?",font="arial 14 bold").place(x=100,y=200)
        
        Button(root1,text="ADD TO CART FROM PRODUCT LIST",command=insertscr).place(x=15,y=260)
        Button(root1,text="DELETE FROM CART",command=deletescr).place(x=370,y=260)
        Button(root1,text="UPDATE FIELD OF EXISTING PRODUCT",command=updatescr).place(x=15,y=300)
        Button(root1,text="SHOW CART",command=showscr).place(x=370,y=300)
        Button(root1,text="Proceed for billing",command=billing).place(x=200,y=370)
        Button(root1,text="Go Back",command=back).place(x=420,y=470)


        
def insertscr():
    global root1
    global root3
    global root2
    global v1
    global v2
    global v3
    global v4
    global img
    global img2
    global imag
    global imag2    

    root1.destroy()
    
    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("RELIANCE STORE")
    root2.iconbitmap("ICON.ico")
    
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    L1=Label(root2,image=img)
    L1.place(x=0,y=0)
    L2=Label(root2,image=img2)
    L2.place(x=50,y=0)

    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    v1=StringVar(root2)
    v2=StringVar(root2)
    v3=StringVar(root2)
    v4=StringVar(root2)

    Label(root2,text="Cart Generator",font="arial 14 bold").place(x=170,y=150)
    Label(root2,text="Note:- Please enter the exact product details from the List",font="arial 14").place(x=6,y=200)
    Label(root2,text="Product Code",font="arial 12 bold").place(x=50,y=250)
    Label(root2,text="Product Name",font="arial 12 bold").place(x=50,y=300)
    Label(root2,text="Quantity",font="arial 12 bold").place(x=50,y=350)
    Label(root2,text="Price",font="arial 12 bold").place(x=50,y=400)


        
    e1=Entry(root2,textvariable=v1).place(x=200,y=250)
    e2=Entry(root2,textvariable=v2).place(x=200,y=300)
    e3=Entry(root2,textvariable=v3).place(x=200,y=350)
    e4=Entry(root2,textvariable=v4).place(x=200,y=400)

    Button(root2,text="Search",command=search).place(x=350,y=250)
    Button(root2,text="Add",command=insert).place(x=270,y=440)
    Button(root2,text="Clear",command=clear).place(x=170,y=440)
    Button(root2,text="Go Back",command=Goback).place(x=420,y=470)


    i=200
    cur.execute("select * from stock")
    rec=cur.fetchall()

    root3=Tk()
    root3.geometry("500x500+600+100")
    root3.title("Current Stock")
    root3.iconbitmap("ICON.ico")
        
    imag = PhotoImage(file="Background.png",master=root3)
    imag2= PhotoImage(file="LOGO.png",master=root3)
    Label(root3,image=imag).place(x=0,y=0)
    Label(root3,image=imag2).place(x=50,y=0)
    Label(root3,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root3,text="Product code",font="arial 11 ").place(x=50,y=150)
    Label(root3,text="Product Name",font="arial 11 ").place(x=155,y=150)
    Label(root3,text="Quantity",font="arial 11 ").place(x=270,y=150)
    Label(root3,text="Product Price",font="arial 11 ").place(x=345,y=150)
    
    
    for x in rec:
        Label(root3,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
        Label(root3,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
        Label(root3,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
        Label(root3,text=x[3],width=12,relief=GROOVE).place(x=355,y=i)
        i=i+20

    
def deletescr():
    global root1
    global root3
    global root2
    global v1
    global img
    global img2
    global imag
    global imag2

    #deleting by product code only

    cur.execute("select * from customer")
    reco=cur.fetchall()
    
    if (reco==[]):
        messagebox.showinfo("Reliance store","Cart empty! Cannot proceed.")
    else:    
        root1.destroy()

        i=200
        
        cur.execute("select * from reciept")
        rec=cur.fetchall()

        root2=Tk()
        root2.geometry("500x500+600+100")
        root2.title("Your Cart")
        root2.iconbitmap("ICON.ico")
        
        img = PhotoImage(file="Background.png",master=root2)
        img2= PhotoImage(file="LOGO.png",master=root2)
        Label(root2,image=img).place(x=0,y=0)
        Label(root2,image=img2).place(x=50,y=0)
        Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
        
        Label(root2,text="Product code",font="arial 11 ").place(x=50,y=150)
        Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=150)
        Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=150)
        Label(root2,text="Product Price",font="arial 11 ").place(x=345,y=150)
        
        
        for x in rec:
            Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
            Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
            Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
            Label(root2,text=x[3],width=12,relief=GROOVE).place(x=355,y=i)
            i=i+20

            
        root3=Tk()
        root3.geometry("500x500+70+100")
        root3.title("RELIANCE STORE")
        root3.iconbitmap("ICON.ico")
        
        imag = PhotoImage(file="Background.png",master=root3)
        imag2= PhotoImage(file="LOGO.png",master=root3)
        Label(root3,image=imag).place(x=0,y=0)
        Label(root3,image=imag2).place(x=50,y=0)
        Label(root3,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
        
        v1=StringVar(root3)
        
        Label(root3,text="DELETE RECORDS",font="arial 14 bold").place(x=155,y=150)
        
        Label(root3,text="Enter Product code",font="arial 12 bold").place(x=50,y=200)
        e1=Entry(root3,textvariable=v1).place(x=250,y=200)
        Button(root3,text="Delete",command=delete).place(x=275,y=250)
        Button(root3,text="Go Back",command=Goback).place(x=420,y=470)

def updatescr():
    global root1
    global root3
    global root2
    global v1
    global v2
    global v3
    global v4
    global img
    global img2
    global imag
    global imag2

    cur.execute("select * from customer")
    reco=cur.fetchall()
    
    if (reco==[]):
        messagebox.showinfo("Reliance store","Cart empty! Cannot proceed.")
    else:
        root1.destroy()

        i=200
        cur.execute("select * from reciept")
        rec=cur.fetchall()

        root2=Tk()
        root2.geometry("500x500+600+100")
        root2.title("Your Cart")
        root2.iconbitmap("ICON.ico")
        
        img = PhotoImage(file="Background.png",master=root2)
        img2= PhotoImage(file="LOGO.png",master=root2)
        Label(root2,image=img).place(x=0,y=0)
        Label(root2,image=img2).place(x=50,y=0)
        Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
        
        Label(root2,text="Product code",font="arial 11 ").place(x=50,y=150)
        Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=150)
        Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=150)
        Label(root2,text="Product Price",font="arial 11 ").place(x=345,y=150)
        
        
        for x in rec:
            Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
            Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
            Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
            Label(root2,text=x[3],width=12,relief=GROOVE).place(x=355,y=i)
            i=i+20

        
        root3=Tk()
        root3.geometry("500x500+70+100")
        root3.title("RELIANCE STORE")
        root3.iconbitmap("ICON.ico")

        imag = PhotoImage(file="Background.png",master=root3)
        imag2= PhotoImage(file="LOGO.png",master=root3)
        Label(root3,image=imag).place(x=0,y=0)
        Label(root3,image=imag2).place(x=50,y=0)
        Label(root3,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

        v1=StringVar(root3)
        v2=StringVar(root3)
        v3=StringVar(root3)
        v4=StringVar(root3)

        Label(root3,text="Cart Update",font="arial 14 bold").place(x=170,y=150)
        Label(root3,text="Kindly try not to make a mistake this time. Thanks!",font="arial 14").place(x=35,y=200)
        Label(root3,text="Product Code",font="arial 12 bold").place(x=50,y=250)
        Label(root3,text="Product Name",font="arial 12 bold").place(x=50,y=300)
        Label(root3,text="Quantity",font="arial 12 bold").place(x=50,y=350)
        Label(root3,text="Price",font="arial 12 bold").place(x=50,y=400)


            
        e1=Entry(root3,textvariable=v1).place(x=200,y=250)
        e2=Entry(root3,textvariable=v2).place(x=200,y=300)
        e3=Entry(root3,textvariable=v3).place(x=200,y=350)
        e4=Entry(root3,textvariable=v4).place(x=200,y=400)

        Button(root3,text="Search",command=search1).place(x=350,y=250)
        Button(root3,text="Update",command=update).place(x=270,y=440)
        Button(root3,text="Clear",command=clear).place(x=170,y=440)
        Button(root3,text="Go Back",command=Goback).place(x=420,y=470)

def showscr():
    global root1
    global root2
    global img
    global img2

    cur.execute("select * from customer")
    reco=cur.fetchall()
    
    if (reco==[]):
        messagebox.showinfo("Reliance store","Cart empty! Cannot proceed.")
    else:
        root1.destroy()

        i=200
        cur.execute("select * from reciept")
        rec=cur.fetchall()

        root2=Tk()
        root2.geometry("500x500+70+100")
        root2.title("Your Cart")
        root2.iconbitmap("ICON.ico")
            
        img = PhotoImage(file="Background.png",master=root2)
        img2= PhotoImage(file="LOGO.png",master=root2)
        Label(root2,image=img).place(x=0,y=0)
        Label(root2,image=img2).place(x=50,y=0)
        Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

        Label(root2,text="Product code",font="arial 11 ").place(x=50,y=150)
        Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=150)
        Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=150)
        Label(root2,text="Product Price",font="arial 11 ").place(x=345,y=150)
        
        
        for x in rec:
            Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
            Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
            Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
            Label(root2,text=x[3],width=12,relief=GROOVE).place(x=355,y=i)
            i=i+20

        Button(root2,text="Go Back",command=Goback).place(x=420,y=470)


def FSCR():
    global root2
    global root3
    global img
    global img2
    global Gt
    global P1
    global P2
    global v1

    root2.destroy()

    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("Bill Generator")
    root2.iconbitmap("ICON.ico")
    
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    Label(root2,image=img).place(x=0,y=0)
    Label(root2,image=img2).place(x=50,y=0)
    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
    
    Label(root2,text="Order Summary",font="arial 12 bold").place(x=50,y=140)

    i=200
    j=200
    
    cur.execute("select price * quantity as Total from reciept")
    total=cur.fetchall()

    Gt=0
    Gr=list(map(sum, total))
    for x in Gr:
        Gt=Gt+x
        
    cur.execute("select * from reciept")
    Prods=cur.fetchall()

    Label(root2,text="Product code",font="arial 11 ").place(x=50,y=170)
    Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=170)
    Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=170)
    Label(root2,text="Total Price",font="arial 11 ").place(x=350,y=170)
    
    
    for x in Prods:
        Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
        Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
        Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
        i=i+20
        cur.execute("update stock set quantity=quantity-{} where Pcode={}".format(x[2],x[0]))

    for x in range(0,len(total)):
        Label(root2,text=total[x],width=12,relief=GROOVE).place(x=355,y=j)
        j=j+20
        
    Label(root2,text=Gt,width=12,relief=GROOVE).place(x=355,y=400)
    Label(root2,text="Grand Total",width=10,font="arial 11").place(x=270,y=400)

    v1=StringVar(root2)
    e1=Entry(root2,textvariable=v1).place(x=350,y=440)
    Label(root2,text="*Please enter your name",font="arial 11").place(x=180,y=440)
    
    Button(root2,text="Done",command=exitt).place(x=380,y=470)
    
def Cpurchase():
    global root2
    global root3
    global img
    global img2
    global Gt
    global P1
    global P2

    root2.destroy()

    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("Confirm purchase")
    root2.iconbitmap("ICON.ico")
    
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    Label(root2,image=img).place(x=0,y=0)
    Label(root2,image=img2).place(x=50,y=0)
    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root2,text="Please select a payment option :",font="arial 12 bold").place(x=50,y=150)

    P1= PhotoImage(file="Card.png",master=root2)
    P2= PhotoImage(file="Cash.png",master=root2)
    Button(root2,text="Card",command=FSCR, image= P1).place(x=20,y=220)
    Label(root2,text="Credit/Debit Card",font="arial 14 bold").place(x=40,y=370)

    Button(root2,text="Cash",command=FSCR,image= P2).place(x=270,y=220)
    Label(root2,text="Cash",font="arial 14 bold").place(x=350,y=370)

    txt="Your total payable amount is:-"+str(Gt)
    Label(root2,text=txt,font="arial 12 bold").place(x=50,y=175)
    Button(root2,text="Go Back",command=Goback).place(x=420,y=470)

def billing():
    global root1
    global root2
    global img
    global img2
    global Gt
    
    cur.execute("select * from customer")
    reco=cur.fetchall()
    
    if (reco==[]):
        messagebox.showinfo("Reliance store","Cart empty! Cannot proceed.")
    else:    
        root1.destroy()

        root2=Tk()
        root2.geometry("500x500+70+100")
        root2.title("Bill Generator")
        root2.iconbitmap("ICON.ico")
        
        img = PhotoImage(file="Background.png",master=root2)
        img2= PhotoImage(file="LOGO.png",master=root2)
        Label(root2,image=img).place(x=0,y=0)
        Label(root2,image=img2).place(x=50,y=0)
        Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

        Label(root2,text="Your Bill",font="arial 12 bold").place(x=50,y=150)

        i=200
        j=200
        
        cur.execute("select price * quantity as Total from reciept")
        total=cur.fetchall()

        Gt=0
        Gr=list(map(sum, total))
        for x in Gr:
            Gt=Gt+x
            
        cur.execute("select * from reciept")
        Prods=cur.fetchall()

        Label(root2,text="Product code",font="arial 11 ").place(x=50,y=150)
        Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=150)
        Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=150)
        Label(root2,text="Total Price",font="arial 11 ").place(x=350,y=150)
        
        
        for x in Prods:
            Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
            Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
            Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
            i=i+20

        for x in range(0,len(total)):
            Label(root2,text=total[x],width=12,relief=GROOVE).place(x=355,y=j)
            j=j+20
            
        Label(root2,text=Gt,width=12,relief=GROOVE).place(x=355,y=440)
        Label(root2,text="Grand Total",width=10,font="arial 11").place(x=270,y=440)
        
        Button(root2,text="Confirm purchase",command=Cpurchase).place(x=300,y=470)
        Button(root2,text="Go Back",command=Goback).place(x=420,y=470)
    
def customer():
    global root
    global root1
    global img
    global img2
        
    root.destroy()
    
    root1=Tk()
    root1.geometry("500x500+70+100")
    root1.title("Welcome! Customer")
    root1.iconbitmap("ICON.ico")

    img = PhotoImage(file="Background.png")
    img2= PhotoImage(file="LOGO.png")
    Label(root1,image=img).place(x=0,y=0)
    Label(root1,image=img2).place(x=50,y=0)
    Label(root1,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root1,text="WHAT DO YOU WANT TO DO?",font="arial 14 bold").place(x=100,y=200)
    
    Button(root1,text="Add To Cart From Product List",command=insertscr).place(x=15,y=260)
    Button(root1,text="Delete From Cart",command=deletescr).place(x=370,y=260)
    Button(root1,text="Update Field Of Existing Product",command=updatescr).place(x=15,y=300)
    Button(root1,text="Show Cart",command=showscr).place(x=370,y=300)
    Button(root1,text="Proceed for billing",command=billing).place(x=200,y=370)
    Button(root1,text="Go Back",command=back).place(x=420,y=470)



################################      ADMIN STARTS HERE      ##################################

"""

The admin section deals with all the manipulation and checking of stocks and sales... The default username is set to "Admin007" and
default password is set to "0075RXT"... However you cannot change the password or username from the program as the
company (Reliance store here) distributes the default passwords and username to the amdins and it can never be changed..
keeping in mind the work flow of admin section the option to change password and username is not provided by us in the program...

"""

### basic functions for admin ###

def ainsert():
    global v1
    global v2
    global v3
    global v4

    cd=v1.get()
    nm=v2.get()
    qty=v3.get()
    pr=v4.get()
    cur.execute("insert into stock values (%s,%s,%s,%s)",(cd,nm,qty,pr))
    db.commit()
    messagebox.showinfo("Reliance Store ","Succesful!")

def aupdate():
    global v1
    global v2
    global v3
    global v4
    
    cd=v1.get()
    nm=v2.get()
    qty=v3.get()
    pr=v4.get()
    sql1="update stock set Pname=%s,quantity=%s,price=%s where Pcode=%s"
    val=(nm,qty,pr,cd)
    cur.execute(sql1,val)
    db.commit()
    messagebox.showinfo("Reliance Store","Stocks updated successfully")
    
def aclear():
    global v1
    global v2
    global v3
    global v4
    
    v1.set('')
    v2.set('')
    v3.set('')
    v4.set('')


    
def goback():
    global root2
    global P1
    global P2
    global P3
    global P4
    global img
    global img2

    root2.destroy()

    root2=Tk()
    root2.title("Welcome Admin!")
    root2.geometry("500x500+70+100")
    root2.iconbitmap("ICON.ico")
 
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    Label(root2,image=img).place(x=0,y=0)
    Label(root2,image=img2).place(x=50,y=0)
    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    P1= PhotoImage(file="Manage.png",master=root2)
    P2= PhotoImage(file="Check.png",master=root2)
    P3= PhotoImage(file="Logout.png",master=root2)
    P4= PhotoImage(file="Sales.png",master=root2)
    
    Button(root2,text="Update Stock",command=SUpdate,image=P1).place(x=35,y=150)
    Button(root2,text="Check Stock",command=Sshow,image=P2).place(x=285,y=150)
    Button(root2,text="Logout",command=logout,image=P3).place(x=420,y=400)
    Button(root2,text="Sales Check",command=Salecheck,image=P4).place(x=160,y=300)

    Label(root2,text="Manage Stock",font="arial 14 bold").place(x=49,y=266)
    Label(root2,text="Check Stock",font="arial 14 bold").place(x=305,y=266)
    Label(root2,text="Logout",font="arial 14 bold").place(x=415,y=461)
    Label(root2,text="Total Sales Check",font="arial 14 bold").place(x=157,y=430)

def login():
    global v1
    global v2
    global img
    global img2
    global P1
    global P2
    global P3
    global P4
    global root1
    global root2

    cur.execute("select * from user")
    rec=cur.fetchall()

    UN= v1.get()
    PS= v2.get()
    x=[UN,PS]
    i=tuple(x)
    
    if i in rec:

        root1.destroy()
        
        root2=Tk()
        root2.title("Welcome Admin!")
        root2.geometry("500x500+70+100")
        root2.iconbitmap("ICON.ico")
     
        img = PhotoImage(file="Background.png",master=root2)
        img2= PhotoImage(file="LOGO.png",master=root2)
        Label(root2,image=img).place(x=0,y=0)
        Label(root2,image=img2).place(x=50,y=0)
        Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
    
        P1= PhotoImage(file="Manage.png",master=root2)
        P2= PhotoImage(file="Check.png",master=root2)
        P3= PhotoImage(file="Logout.png",master=root2)
        P4= PhotoImage(file="Sales.png",master=root2)
        
        Button(root2,text="Update Stock",command=SUpdate,image=P1).place(x=35,y=150)
        Button(root2,text="Check Stock",command=Sshow,image=P2).place(x=285,y=150)
        Button(root2,text="Logout",command=logout,image=P3).place(x=420,y=400)
        Button(root2,text="Sales Check",command=Salecheck,image=P4).place(x=160,y=300)

        Label(root2,text="Manage Stock",font="arial 14 bold").place(x=49,y=266)
        Label(root2,text="Check Stock",font="arial 14 bold").place(x=305,y=266)
        Label(root2,text="Logout",font="arial 14 bold").place(x=415,y=461)
        Label(root2,text="Total Sales Check",font="arial 14 bold").place(x=157,y=430)

    else:
        messagebox.showinfo("Reliance store","Invalid Credentials! Please try again")


def Salecheck():
    global root2
    global img
    global img2
                
    root2.destroy()

    cur.execute("select * from totalsales")
    rec=cur.fetchall()
    i=200

    cur.execute("select SUM(Amount) from totalsales")
    total=cur.fetchall()

    
        
    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("Current Stock")
    root2.iconbitmap("ICON.ico")

    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)

    Label(root2,image=img).place(x=0,y=0)
    Label(root2,image=img2).place(x=50,y=0)
    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root2,text="Customer name",font="arial 12 ").place(x=50,y=150)
    Label(root2,text="Purchase Amount",font="arial 12 ").place(x=190,y=150)

    Button(root2,text="Go Back",command=goback).place(x=420,y=470)
       
    for x in rec:
        Label(root2,text=x[0],width=16,relief=GROOVE).place(x=60,y=i)
        Label(root2,text=x[1],width=16,relief=GROOVE).place(x=200,y=i)
        i=i+20
        
    TS="Total sales till now in INR. "+str(total[0])    
    Label(root2,text=TS,font="arial 12 ").place(x=60,y=450)

def logout():
    global root2
    global root1
    global img
    global img2
    global v1
    global v2

    root2.destroy()
    
    root1=Tk()
    root1.geometry("500x500+70+100")
    root1.title("RELIANCE STORE")
    root1.iconbitmap("ICON.ico")
     
    img = PhotoImage(file="Background.png",master=root1)
    img2= PhotoImage(file="LOGO.png",master=root1)
    Label(root1,image=img).place(x=0,y=0)
    Label(root1,image=img2).place(x=50,y=0)
    Label(root1,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root1,text="Please Enter Username And password to Gain access!",font="arial 12 bold").place(x=35,y=150)
    
    Label(root1,text="USER NAME",font="arial 14 bold").place(x=50,y=200)
    Label(root1,text="PASSWORD",font="arial 14 bold").place(x=50,y=250)

    v1=StringVar(root1)
    v2=StringVar(root1)

    e1=Entry(root1,textvariable=v1).place(x=200,y=205)
    e2=Entry(root1,textvariable=v2).place(x=200,y=255)
    
    Button(root1,text="LOGIN",command=login).place(x=225,y=350)
    Button(root1,text="Go Back",command=back).place(x=420,y=470)

def Sshow():
    global root2
    global img
    global img2
                
    root2.destroy()

    i=200
    cur.execute("select * from stock")
    rec=cur.fetchall()

    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("Current Stock")
    root2.iconbitmap("ICON.ico")
        
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    Label(root2,image=img).place(x=0,y=0)
    Label(root2,image=img2).place(x=50,y=0)
    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    Label(root2,text="Product code",font="arial 11 ").place(x=50,y=150)
    Label(root2,text="Product Name",font="arial 11 ").place(x=155,y=150)
    Label(root2,text="Quantity",font="arial 11 ").place(x=270,y=150)
    Label(root2,text="Product Price",font="arial 11 ").place(x=345,y=150)
    
    
    for x in rec:
        Label(root2,text=x[0],width=12,relief=GROOVE).place(x=60,y=i)
        Label(root2,text=x[1],width=12,relief=GROOVE).place(x=165,y=i)
        Label(root2,text=x[2],width=7,relief=GROOVE).place(x=278,y=i)
        Label(root2,text=x[3],width=12,relief=GROOVE).place(x=355,y=i)
        i=i+20

    Button(root2,text="Go Back",command=goback).place(x=420,y=470)


def SUpdate():
    global root3
    global root2
    global v1
    global v2
    global v3
    global v4
    global img
    global img2
    global imag
    global imag2

    root2.destroy()
    
    root2=Tk()
    root2.geometry("500x500+70+100")
    root2.title("RELIANCE STORE")
    root2.iconbitmap("ICON.ico")
    
    img = PhotoImage(file="Background.png",master=root2)
    img2= PhotoImage(file="LOGO.png",master=root2)
    L1=Label(root2,image=img)
    L1.place(x=0,y=0)
    L2=Label(root2,image=img2)
    L2.place(x=50,y=0)

    Label(root2,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

    v1=StringVar(root2)
    v2=StringVar(root2)
    v3=StringVar(root2)
    v4=StringVar(root2)

    Label(root2,text="Stock management",font="arial 14 bold").place(x=170,y=150)
    Label(root2,text="Product Code",font="arial 12 bold").place(x=50,y=250)
    Label(root2,text="Product Name",font="arial 12 bold").place(x=50,y=300)
    Label(root2,text="Quantity",font="arial 12 bold").place(x=50,y=350)
    Label(root2,text="Price",font="arial 12 bold").place(x=50,y=400)


        
    e1=Entry(root2,textvariable=v1).place(x=200,y=250)
    e2=Entry(root2,textvariable=v2).place(x=200,y=300)
    e3=Entry(root2,textvariable=v3).place(x=200,y=350)
    e4=Entry(root2,textvariable=v4).place(x=200,y=400)


    Button(root2,text="Add",command=ainsert).place(x=220,y=440)
    Button(root2,text="Update",command=aupdate).place(x=300,y=440)
    Button(root2,text="Clear",command=aclear).place(x=140,y=440)
    Button(root2,text="Go Back",command=goback).place(x=420,y=470)



def admin():
    global root
    global root1
    global img
    global img2
    global v1
    global v2
    
    root.destroy()

    root1=Tk()
    root1.geometry("500x500+70+100")
    root1.title("RELIANCE STORE")
    root1.iconbitmap("ICON.ico")
     
    img = PhotoImage(file="Background.png",master=root1)
    img2= PhotoImage(file="LOGO.png",master=root1)
    Label(root1,image=img).place(x=0,y=0)
    Label(root1,image=img2).place(x=50,y=0)

    Label(root1,text="Please Enter Username And password to Gain access!",font="arial 12 bold").place(x=35,y=150)
    Label(root1,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)
    
    Label(root1,text="USER NAME",font="arial 14 bold").place(x=50,y=200)
    Label(root1,text="PASSWORD",font="arial 14 bold").place(x=50,y=250)

    v1=StringVar(root1)
    v2=StringVar(root1)

    e1=Entry(root1,textvariable=v1).place(x=200,y=205)
    e2=Entry(root1,textvariable=v2,show="*").place(x=200,y=255)
    
    Button(root1,text="LOGIN",command=login).place(x=225,y=350)
    Button(root1,text="Go Back",command=back).place(x=420,y=470)
    
    




###########################         MAIN PROGRAM STARTS HERE        #########################

"""

The main program start running from here, we have used a pre-selected logo for our application and it can be seen in the GUI itself
as well as it can also be seen in the code where "PhotoImage" function of Tkinter has been used by us...
Have a look!!

"""


root=Tk()
root.geometry("500x500+70+100")
root.title("RELIANCE STORE")
root.iconbitmap("ICON.ico")

#creating the background image

img = PhotoImage(file="Background.png",master=root)
img2= PhotoImage(file="LOGO.png",master=root)
Label(root,image=img).place(x=0,y=0)
Label(root,image=img2).place(x=50,y=0)

Label(root,text="Hey There! Welcome To Reliance Store",font="arial 14 bold").place(x=60,y=140)
Label(root,text="How do you wish to continue?",font="arial 14 bold").place(x=100,y=180)
Label(root,text="©2019 Tanuj ",font="arial 7 ").place(x=50,y=113)

P1= PhotoImage(file="Admin.png",master=root)
P2= PhotoImage(file="customer.png",master=root)

Button(root,text="ADMIN",command=admin, image= P1).place(x=90,y=230)

Label(root,text="Admin",font="arial 14 bold").place(x=104,y=333)

Button(root,text="CUSTOMER",command=customer,image= P2).place(x=265,y=227)
Label(root,text="Customer",font="arial 14 bold").place(x=296,y=336)

Button(root,text="EXIT",command=exit).place(x=420,y=470)

root.mainloop()
