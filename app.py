import json
#from os import stat
from flask import Flask, redirect, render_template, request
from sqlalchemy import null
#import mydatabase
from database import mydatabase
#from database.mydatabase import MyDatabase as mydatabase
api = Flask(__name__)
dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname='mydb.sqlite')
# -------------------------------------- home -------------------------------------------
@api.route('/')
def home():
    res= dbms.print_all(table= mydatabase.CUSTOMERS)
    return render_template("home.html",res=res)
# --------------------------------------- customers -------------------------------------------
#customers page
@api.route('/customers', methods=['GET','POST'])
def customers():
    if request.method=='GET':
        if request.args.get('name') != None:
            customersList=dbms.print_customer_by_name(request.args.get('name'))
            return render_template("customers.html",customersList=customersList)
    customersList= dbms.print_all(table= mydatabase.CUSTOMERS)
    return render_template("customers.html",customersList=customersList)

@api.route('/addCustomer',methods=['POST'])
def addCustomer():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        age = request.form.get('age')
        dbms.insert_customer(name,city,age)
        return customers()
    return customers()

@api.route('/deleteCustomer')
def deleteCustomer():
    name = request.args.get('name')
    id = request.args.get('id')
    dbms.delete_customer(name,id)
    return redirect('/customers')


# --------------------------------------- books ---------------------------------------------
# Books page 
@api.route('/books', methods=['GET','POST'])
def books():
    if request.method=='GET':
        if request.args.get('name') != None:
            booksList=dbms.print_book_by_name(request.args.get('name'))
            return render_template("books.html",booksList=booksList)
    booksList= dbms.print_all(table= mydatabase.BOOKS)
    return render_template("books.html",booksList=booksList) 

@api.route('/addBook',methods=['POST','GET'])
def addBook():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        yearPublished = request.form.get('yearpublished')
        type = request.form.get('type')
        status = 'Available'
        image = request.form.get("image")
        dbms.insert_book(name,author,int(yearPublished),int(type),status,image)
        print(name,author,yearPublished,type,status)
        return books()
    return books() 

@api.route('/deleteBook')
def deleteBook():
    name = request.args.get('name')
    id = request.args.get('id')
    dbms.delete_book(name,id)
    return redirect('/books')
#-------------------------------------- loans -------------------------------------------------
@api.route('/addRent', methods=['POST','GET'])
def addRent():
    if request.method=='POST':
        bookId = request.form.get('bookId')
        custId = request.form.get('custId')
        booktype = request.form.get('booktype')
        print(bookId, custId, booktype)
        dbms.insert_loan(int(bookId),int(custId),int(booktype))
        dbms.update_book_status_notAvailable(request.form.get('bookId'))
        return loansNEW()
    return loansNEW()

@api.route('/loansNEW')
def loansNEW():
    if request.method=='GET':
        if request.args.get('name') != None:
            loansList=dbms.print_loans_by_name(request.args.get('name'))
            return render_template("loansNEW.html",loansList=loansList)
        if request.args.get('bookid') != null:
          dbms.update_loan_status_returned(request.args.get('loanid'))
          dbms.update_loan_actual_returnDate(request.args.get('loanid'))
          dbms.update_book_status_Available(request.args.get('bookid'))
    loansList= dbms.print_all_loans()
    return render_template("loansNEW.html",loansList=loansList)

@api.route('/lateReturn')
def lateReturn():
    loansList= dbms.late_return()
    return render_template("loansNEW.html",loansList=loansList)



#--------------------------------------- main -------------------------------------------------
def main():
    api.run(debug=True)
    dbms.create_tables()
   
# run the program
if __name__ == "__main__": main()