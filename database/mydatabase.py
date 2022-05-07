#from ast import Pass
from datetime import datetime, timedelta
import json
from sqlite3 import Connection
from click import echo
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

#from app import customers
SQLITE                  = 'sqlite'
# Table Names
BOOKS            = 'books'
CUSTOMERS       = 'customers'
LOANS    ="loans"

class MyDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
    }
    # Main DB Connection Ref Obj
    db_engine = None
    
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)

            self.db_engine = create_engine(engine_url, echo=True)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")
    
    # creating the table
    def create_tables(self):
        metadata = MetaData()
        books = Table(BOOKS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('Name', String),
                      Column('Author', String),
                      Column('YearPublished', Integer),
                      Column('Type', Integer),
                      Column('Status', String),
                      Column('Image',String)
                      )

        customers = Table(CUSTOMERS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('Name', String),
                      Column('City', String),
                      Column('Age', Integer)
                      )

        loans = Table(LOANS, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('CustID', None, ForeignKey('customers.id')),
                        Column('BookID', None, ForeignKey('books.id')),
                        Column('Loandate', String),
                        Column('Returndate', String),
                        Column('ActualReturndate', String),
                        Column('Status', String)
                        )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)
    
    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : print('aaaaaa')

        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)
    
    # print all data / data by queries
    def print_all(self, table='', query=''):
        query = query if query != '' else f"SELECT * FROM '{table}';"
        #print(query)
        print(" ")
        print(f'printing {table} table : ')
        print('__________________________')
        print(" ")
        res = []
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    res.append( row)
                result.close()
        return (res)


# --------------------------------------------------------books--------------------------------------------------------------------------
    # insert a book to the books table
    def insert_book(self,name,author,yearPublished,type,status,Image):
        # Insert Data
        query = f"INSERT INTO '{BOOKS}' (Name,Author,YearPublished,Type,Status,Image) " \
                f"VALUES ( '{name}','{author}',{yearPublished},{type},'{status}','{Image}');"
        print(query)
        self.execute_query(query)
    
    # delete book by name
    def delete_book(self,name,id):
        query = f"DELETE FROM '{BOOKS}' WHERE Name='{name}' AND id='{id}'"
        self.execute_query(query)
        #self.print_all(BOOKS)
        print(f"book {name} deleted ")

    # print book by name
    def print_book_by_name(self,name):
        query2 = f"SELECT * FROM {BOOKS} WHERE {BOOKS}.Name LIKE '%{name}%';"
        print(query2)
        return self.print_all(table=BOOKS,query=query2)
    
    # update the bookws status to not available
    def update_book_status_notAvailable(self,id):
        query = f"UPDATE '{BOOKS}' SET Status='Not Available' WHERE id={id};"
        print(query)
        self.execute_query(query)
    
    # update the bookws status to available
    def update_book_status_Available(self,id):
        query = f"UPDATE '{BOOKS}' SET Status='Available' WHERE id={id};"
        print(query)
        self.execute_query(query)
# --------------------------------------------------------customers--------------------------------------------------------------------------
    # insert a customer to the customers table
    def insert_customer(self,name,city,age):
        # Insert Data
        query = f"INSERT INTO '{CUSTOMERS}' (Name,City,Age) " \
                f"VALUES ( '{name}','{city}',{age});"
        self.execute_query(query)
           
    # delete customer by name
    def delete_customer(self,name,id):
        query = f"DELETE FROM '{CUSTOMERS}' WHERE Name='{name}' AND id='{id}'"
        self.execute_query(query=query)
        #self.print_all(CUSTOMERS)
        print(f"customer : {name} deleted ")
    
    # print customer by name
    def print_customer_by_name(self,name):
        query = f"SELECT * FROM '{CUSTOMERS}' WHERE {CUSTOMERS}.Name LIKE '%{name}%';"
        print(query)
        return self.print_all(table=CUSTOMERS,query=query)
# --------------------------------------------------------loans--------------------------------------------------------------------------        
    # insert a loan to the loans table   
    def insert_loan(self,bookId,custId,booktype):
        loandate = datetime.now()
        if booktype == 1:
            returndate = datetime.now() + timedelta(days=10)
        elif booktype == 2 :
            returndate = datetime.now() + timedelta(days=5)
        else:
            returndate = datetime.now() + timedelta(days=2)
        ActualReturndate = '-'
        Status = 'Not returned yet'
        # Insert Data
        query = f"INSERT INTO '{LOANS}' (CustID,BookID,Loandate,Returndate,ActualReturndate,Status) " \
                f"VALUES ({custId},{bookId},'{loandate}','{returndate}','{ActualReturndate}','{Status}');"
        print(query)
        self.execute_query(query)
    
    # print all loans
    def print_all_loans(self):
        query = f"SELECT L.id, C.Name AS 'CUSTOMERNAME', B.Name AS 'BOOKNAME', L.BookID, L.Loandate, L.Returndate, L.ActualReturndate, L.Status  FROM '{CUSTOMERS}' AS C INNER JOIN '{LOANS}' AS L ON C.id=L.CustID INNER JOIN '{BOOKS}' AS B ON L.BookID=B.id;"
        return self.print_all(query=query)
    
    # print laye return
    def late_return(self):
        query = f"SELECT L.id, C.Name AS 'CUSTOMERNAME', B.Name AS 'BOOKNAME', L.BookID, L.Loandate, L.Returndate, L.ActualReturndate, L.Status FROM '{CUSTOMERS}' AS C INNER JOIN '{LOANS}' AS L ON C.id=L.CustID INNER JOIN '{BOOKS}' AS B ON L.BookID=B.id WHERE (L.ActualReturndate != '-' and L.ActualReturndate > L.Returndate) OR ((L.ActualReturndate == '-' and '{datetime.now()}'>L.Returndate)  ;"
        return self.print_all(query=query)

    # print loans by name (search bar)
    def print_loans_by_name(self,name):
        query = f"SELECT C.Name AS 'CUSTOMERNAME', B.Name AS 'BOOKNAME', L.Loandate, L.Returndate  FROM '{CUSTOMERS}' AS C INNER JOIN '{LOANS}' AS L ON C.id=L.CustID INNER JOIN '{BOOKS}' AS B ON L.BookID=B.id WHERE C.Name LIKE '%{name}%' OR B.Name LIKE '%{name}%' ;"
        return self.print_all(query=query)

    # update loan status to 'returned'
    def update_loan_status_returned(self,id):
        query = f"UPDATE '{LOANS}' SET Status='Returned' WHERE id={id};"
        print(query)
        self.execute_query(query)

    # update loan table column : actual return to the real time
    def update_loan_actual_returnDate(self,id):
        query = f"UPDATE '{LOANS}' SET ActualReturndate='{datetime.now()}' WHERE id={id};"
        print(query)
        self.execute_query(query)