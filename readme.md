## PROJECT 1 ##

1. About me 
Name: Dafni Ruderman
Age: 24
Course: Python Full Stack Developer

2. About this project
In this project I implemented a simple system to manage books library. 
for run this project you need to run and control+click the https.
This system was established for bookstores. 

- HOME :
- home screen will explain you about me and about this project

- CUSTOMERS : 
- Introducing new customers
- View all customers
- Customer display by name
- Delete customer

- BOOKS :
- View all books
- Introducing new books : when adding a new book we need to add url image for the book
- Book view by name
- loan a book (if it is available. if not the button will be disabled. when we loan a book it will added to the loans table). when we click on the loan button we need to know customer id. 
- Delete book

- LOANS :
- display all loans (customer name, book name+id, loan date, return date(when id should be returned, actual return date(the day this book returned) and status ))
- display late loans
- display loans by customer's name/ book's name
- return a book (when we will return a book the status will change color to green)

# INFRASTRUCTURE:

- python programing 
- flask
- sqlite, sqlalchemy
- HTML
- bootstrap

# DATA BASE:
Tables:

- books -> 
columns: id(PK) ,name, author, year published, type(1: up to 10 days, 2: up to 5 days, 3: up to 2 days), status, image url

- customers -> 
columns: id(PK), name, city, age

- loans -> 
columns: customer id(FK), book id(FK), loan date, return date, actual return date, status

# CLASS:

1. books:           DONE
2. customers:       DONE 
3. loans:           DONE

# Flask:            

- layout HTML with navbar in every page
1. home page with details about me           
2. for the books page to print all the books in cards       
3. for loans a page that print all the loans in a table     
4. for customers a page with table

# FUNCTIONS:

1. add customers - DONE  CUSTOMERS PAGE                 
2. add book - DONE BOOKS PAGE                     
3. loan book - DONE BOOKS PAGE                                                                     
4. return book- DONE LOANS PAGE
5. print all books - DONE BOOKS PAGE                 
6. print all customers - DONE CUSTOMERS PAGE         
7. print all loans - DONE LOANS PAGE                                      
8. print all late loans - DONE LOANS PAGE                                                          
9. find(print) book by name - DONE BOOKS PAGE       
10. find (print) customer by name - DONE CUSTOMERS PAGE
11. remove book - DONE BOOKS PAGE                   
12. remove customer - DONE  CUSTOMERS PAGE           

