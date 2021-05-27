#current known mySQL commands for command line > further info > https://www.tutorialspoint.com/mysql/mysql-create-tables.htm

#website for pretty table https://pypi.org/project/prettytable/

#print all information in accounts table
    #SELECT * FROM accounts;

#show currently created databases
    #SHOW databases;

#to enter database directory
    #USE "database name";
    
#shows all current tables in a database
    #SHOW tables;

#to delete a table from a database
    #DROP table "table name";


#to delete a row from a table
    #DELETE FROM "table_name" WHERE "attribute" = "variable";


# Two different syntax's to take user input and execute it as a mysql prompt
    #1 is exemplfied in creat_new_db function > further info > https://www.mysqltutorial.org/python-mysql-insert/
    #2 is in function close_account

#Checking mysql for the amount of rows in a database or table
    # for database < SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'bankingdb';
    # for table < SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'bankingdb' AND table_name = 'table_name';

#To update an existing variable in the database already
    #UPDATE "table_name" SET "attribute" = variable WHERE "attribute" = variable"


from os import name
import random
import json
from re import U 
from mysql.connector import connect, Error
from prettytable import PrettyTable





def create_new_db():
    # assign the _SQL query to a variable and send the _SQL variable to MySQL to execute

    # Create the accounts table in mysql

    _SQL = """

    CREATE TABLE accounts (

        acct_num INT AUTO_INCREMENT,
        name VARCHAR(128) NOT NULL,
        pin MEDIUMINT NOT NULL,
        balance DECIMAL(12,2) DEFAULT 0,
        PRIMARY KEY (acct_num)

        )"""

    cursor.execute(_SQL)

    #used to populate data into existing database
    with open("code/example.json", "r") as acct_file:
        json_file = acct_file.read()

    json_obj = json.loads(json_file)


    acct_objs = json_obj["json_acct_objs"]

    query = "INSERT INTO accounts(acct_num,name,pin,balance)" \
            "VALUES(%s,%s,%s,%s)"
    
    for acct in acct_objs:
        acct_num = acct["acct_num"]
        name = acct["name"]
        pin = acct["pin"]
        balance = acct["balance"]
        args = (acct_num,name,pin,balance)
        cursor.execute(query, args)
    
    
    connection.commit()
   
def stuff(): 
    # describe my accounts table i created in the db

    # you will need to create a table in the db too

    # _SQL = """describe accounts"""

    # cursor.execute(_SQL)

    # results = cursor.fetchall()

    # for row in results:

    #     print(row)



    # #this is the create aaccount

    # insert entries into the table

    # _SQL = """insert into accounts

    #        (acct_num, name, pin, balance)

    #         values

    #         (%s,%s,%s,%s)"""




    # user_input = input("Input num: ")

    # connection.commit()


    # print our entries
    return

#creates a random number 4 digit number that does not currently exists in database
def create_acct_num(): 
    num = random.randint(10000,99999)

    while True:
        cursor.execute("SELECT * FROM accounts WHERE acct_num LIKE %s", (num,))

        results = cursor.fetchall()
        if not results:
            return num

#Displays all currently created accounts in database
def display_created_acct():
    x = PrettyTable()
    _SQL = """select * from accounts"""

    cursor.execute(_SQL)

    x.field_names = ["acct_num", "name", "pin", "balance"]

    for row in cursor.fetchall():
        x.add_row([row[0],row[1],row[2],row[3]])

    print(x)

    return 


#Account holder functions
def acct_sign_in():
    acct_num = 0
    ifexists = 0
    user_input = "1"
    acct_pin = 0
    user_pin = 1
    while(user_pin != acct_pin):
        #Checks if inputed accoutn number exists
        while(ifexists == 0):
            while user_input.isdigit() == False or len(user_input) != 5:
                print()
                user_input = input("Type 0 = exit, or 5 digit account number:" + "\n")

                if user_input == "0":
                    return 1

                if user_input.isdigit() == False or len(user_input) != 5:
                    print("Invalid Response, Plese enter a 5 digit account number")

            if user_input.isdigit() == True:
                acct_num = int(user_input)
                cursor.execute("SELECT EXISTS(SELECT * from accounts WHERE acct_num = %s)", (acct_num,))
                ifexists = cursor.fetchone()
                ifexists = ifexists[0]
                # print(ifexists)
                if ifexists == 0:
                    print("Invalid Account Number: " + user_input)
                    user_input = "1"
            else:
                print("Invalid Response:" +  user_input)

        # print("here")
        #Gets pin for user specified account from db
        acct = cursor.execute("SELECT * FROM accounts WHERE acct_num = %s", (acct_num,))
        acct = cursor.fetchone()
        acct_pin = acct[2]
        acct_name = acct[1]
        user_pin = ""

        #Asks for pin
        while True:
            user_pin = input("Type 0 = exit, or 4 digit account pin:" + "\n")

            if user_pin == "0":
                print("Returning to account selection." + "\n")
                break
            
            print()
            if user_pin.isdigit() == True:
                if int(user_pin) != acct_pin:
                    print("Incorrect input, please try again")
                else:
                    print("Signed in, " + "Welcome " + acct_name + "\n") 
                    return acct

            else:
                print("Invalid response: "+ user_pin +", Please type a 4 digit pin number:" + "\n")

            # print()
            # print("user pin" + user_pin)
            # print("acct pin"+ str(acct_pin))

        if user_pin == "0":
            break
    return 1  

def check_balance(acct):
    print("Your balance is $" + str(acct[3]))
    print()
    return

def deposit(acct):
    crnt_bal = acct[3]
    new_bal = 0
    deposit = 0
    user_input = "a"
    while(True):
        print()
        while(user_input.isdigit() == False):
            crnt_bal = acct[3]
            print("Your current balance is: $" + str(crnt_bal))
            user_input = input("How much would you like to deposit, Type: 0 = exit" + "\n")

            if user_input == "0":
                print()
                return
            
            if user_input.isdigit() == False:
                user_input = input("Invalid Response: Input numbers only please" + "\n")

        deposit = int(user_input)
        user_input = input("Are you sure y/n: " + "\n")

        if user_input.lower() == "y":
            print("Confirming transaction..." + "\n")

            new_bal = crnt_bal + deposit

            cursor.execute("UPDATE accounts SET balance = %s WHERE acct_num = %s", (new_bal,acct[0],))

            print("Your new balance is: $" + str(new_bal) + "\n")
            connection.commit()

            acct_new = cursor.execute("SELECT * FROM accounts WHERE acct_num = %s", (acct[0],))
            acct_new = cursor.fetchone()
            acct_new = list(acct_new)
            return acct_new


        elif user_input.lower() == "n":
            pass
        else:
            print("Invalid Response, Please try again")

def withdraw(acct):
    crnt_bal = acct[3]
    new_bal = 0
    withdraw = 0
    user_input = "a"
    while(True):
        print()
        while(user_input.isdigit() == False):
            crnt_bal = acct[3]
            print("Your current balance is: $" + str(crnt_bal))
            user_input = input("How much would you like to withdraw, Type: 0 = exit" + "\n")

            if user_input == "0":
                print()
                return
            
            if user_input.isdigit() == False:
                user_input = input("Invalid Response: Input numbers only please" + "\n")

        withdraw = int(user_input)
        user_input = input("Are you sure y/n: " + "\n")

        if user_input.lower() == "y":
            print("Confirming transaction..." + "\n")

            new_bal = crnt_bal - withdraw

            if new_bal < 0:
                print("YOU HAVE OVERDRAWN. Deducting overcharge fee of $75" + "\n")
                new_bal += 75

            cursor.execute("UPDATE accounts SET balance = %s WHERE acct_num = %s", (new_bal,acct[0],))

            print("Your new balance is: $" + str(new_bal) + "\n")

            connection.commit()

            acct_new = cursor.execute("SELECT * FROM accounts WHERE acct_num = %s", (acct[0],))
            acct_new = cursor.fetchone()
            acct_new = list(acct_new)
            
            return acct_new


        elif user_input.lower() == "n":
            pass
        else:
            print("Invalid Response, Please try again")


    

    
    return 

#Admin functions
def create_account():
    #exit no work
    while(True):
        name = input("Type, 0 = exit | Clients name?" + "\n")
        if name == 0:
            break

        pin = input("Type, 0 = exit | What is the clients pin? 4 digit number please" + "\n")
        if pin == 0:
            break

        while len(pin) != 4 or pin.isdigit() == False:
            pin = input("Invalid response. Please input a 4 digit pin number" + "\n")

        balance = input("Type, 0 = exit |  Does clients have a starting balance? (y/n)" + "\n")
        if balance == 0:
            break

        while(True):
            if balance.lower() == "y":
                balance = input("Please input starting balance: " + "\n")
                while balance.isdigit() == False:
                    balance = input("That is not a number. Try again" + "\n")
                break

            elif balance.lower() == "n":
                print("okay! Balance will be set to 0")
                balance = "0"
                break
            else:
                balance = input("Invalid response. Does client have money already deopsited in account? (y/n)"+ "\n")

        pin = int(pin)
        balance = int(balance)
        acct_num = create_acct_num()

        print()
        print(f"Name: {name}\nAccount number: {acct_num}\nPin: {pin}\nBalance: {balance}")

        x = input("Are you okay with the current account? y/n " + "\n" + "warning if no, this will delete all current progress" + "\n")
        while True: 
            if x.lower() == "n":
                x = "not key"
                break
            elif x.lower() == "y":
                print(f"NOTICE: take note of your acct_num: {acct_num} as you will need it for future logins\nThank you for using ---- banking")
                print("Returning to previous screen")
                print()
                query = "INSERT INTO accounts(acct_num,name,pin,balance)" \
                        "VALUES(%s,%s,%s,%s)"

                args = (acct_num,name,pin,balance)
                cursor.execute(query, args)
                x = "key"
                break
            else:
                print()
                print(f"Name: {name}\nAccount number: {acct_num}\nPin: {pin}\nBalance: {balance}")
                x = input("Invalid response try again. Are you okay with this accoutn? y/n")

        if x != "not key":
            break

    connection.commit()
    return 

def modify_account():
    user_input = ""
    ifexists = 0
    acct_num = 0

    #Lets user select account
    while user_input.isdigit() == False or ifexists == 0:
        print()
        print("Which account would you like to modify?")
        display_created_acct()
        user_input = input("Type 0 = exit, or desired account number under column labeled acct_num" + "\n")

        if user_input == "0":
            print("Returning to previous screen")
            return

        if user_input.isdigit() == True:
            acct_num = int(user_input)
            cursor.execute("SELECT EXISTS(SELECT * from accounts WHERE acct_num = %s)", (acct_num,))
            ifexists = cursor.fetchone()
            ifexists = ifexists[0]
            if ifexists == 0:
                print("Invalid Account Number: " + user_input)
            #print(ifexists)
        else:
            print("Invalid Response:" +  user_input)

    #takes inputed account and turns it into a pretty table
    acct = cursor.execute("SELECT * FROM accounts WHERE acct_num = %s", (acct_num,))
    acct = cursor.fetchone()


    crnt_name = acct[1]
    crnt_pin = acct[2]
    crnt_bal = acct[3]

    new_name = crnt_name
    new_pin = crnt_pin
    new_bal = crnt_bal

    prettyacct = PrettyTable()
    prettyacct.field_names = ["acct_num", "name", "pin", "balance"]
    prettyacct.add_row([acct[0],crnt_name,crnt_pin,crnt_bal])


    #Figue out what to change and stacks up mysql executable's
    while(user_input != 0):
        print()
        print("what would you like to change?")
        user_input = input("type 0 = exit, 1 = name, 2 = pin, 3 = balance" + "\n" + "Please note Typing 0 = exit, WILL DELETE ALL CURRENT PROGRESS" + "\n")
    
        if user_input == "0":
            print("Returning to previous screen")
            return

        if user_input.lower() == "1":
            while(True):
                user_input = input("Type 0 = exit or enter to continue" + "\n")

                if user_input == "0":
                    break
                
                print("Current name: " + crnt_name)
                new_name = input("New name: ")
                print()
                user_input = input("Name changed from: " + crnt_name + " to " + new_name + ", keep changes? y/n" + "\n")
                if user_input.lower() == "y":
                    cursor.execute("UPDATE accounts SET name = %s WHERE acct_num = %s", (new_name,acct_num,))

                    break
    
                else:
                    print("Change undone")

        elif user_input.lower() == "2":
            while(True):
                user_input = input("Type 0 = exit or enter to continue" + "\n")

                if user_input == "0":
                    break
                
                print("Current pin: " + str(crnt_pin))
                new_pin = input("New pin: ")
                while len(new_pin) != 4 or new_pin.isdigit() == False:
                    new_pin = input("Invalid response. Please input a 4 digit pin number" + "\n")
                print()
                user_input = input("Pin changed from: " + str(crnt_pin) + " to " + str(new_pin) + ", keep changes? y/n" + "\n")
                if user_input.lower() == "y":
                    cursor.execute("UPDATE accounts SET pin = %s WHERE acct_num = %s", (new_pin,acct_num,))

                    break
    
                else:
                    print("Change undone")

        elif user_input.lower() == "3":
            while(True):
                user_input = input("Type 0 = exit or enter to continue" + "\n")

                if user_input == "0":
                    break
                
                print("Current balance: " + str(crnt_bal))
                new_bal = input("New balance: ")
                while new_bal.isdigit() == False:
                    new_bal = input("Invalid response. Please input a integer/decimal value" + "\n")
                print()
                user_input = input("Balance changed from: " + str(crnt_bal) + " to " + str(new_bal) + ", keep changes? y/n" + "\n")
                if user_input.lower() == "y":
                    cursor.execute("UPDATE accounts SET balance = %s WHERE acct_num = %s", (new_bal,acct_num,))

                    break
    
                else:
                    print("Change undone")

        else:
            print("Invalid resonse: " + user_input + " Try again")

        prettyacct.add_row([acct[0],new_name,new_pin,new_bal])

        while(True):
            
            print("Is this all you want to change?" + "\n")
            print("Previous Account info:")
            print(prettyacct[0])

            print("New Account info:")
            print(prettyacct[1])

            user_input = input("Type 0 = exit , 1 = go back to editing, 2 = commit changes" + "\n" + "Typing 0 = exit, WILL DELETE ALL CURRENT PROGRESS" + "\n")

            if user_input == "0":
                print("Returning to previous screen" + "\n")
                return

            elif user_input == "1":
                prettyacct.del_row(1)
                break

            elif user_input == "2":
                connection.commit()
                print("Returning to previous screen" + "\n")
                return

            else:
                print("Invalid Response")

def close_account():
    while(True):
        user_input = ""
        ifexists = 0
        acct_num = 0

        #here check if inputed work is a digit
        while user_input.isdigit() == False or ifexists == 0:
            print()
            print("Which account would you like to modify?")
            display_created_acct()
            user_input = input("Type 0 = exit, or desired account number under column labeled acct_num" + "\n")

            if user_input == "0":
                print("Returning to previous screen")
                return

            if user_input.isdigit() == True:
                acct_num = int(user_input)
                cursor.execute("SELECT EXISTS(SELECT * from accounts WHERE acct_num = %s)", (acct_num,))
                ifexists = cursor.fetchone()
                ifexists = ifexists[0]
                if ifexists == 0:
                    print("Invalid Account Number: " + user_input)
                print(ifexists)
            else:
                print("Invalid Response:" +  user_input)
            
    
        x = input("Are you sure? y/n" + "\n")
        while x.lower() != "y" and x.lower() != "n":
            x = input("Invalid response try again. y/n" + "\n")

        if x.lower() == "n":
            print("Running again" + "\n")
  
        if x.lower() == "y":
            cursor.execute("DELETE FROM accounts WHERE acct_num = %s", (acct_num,))
            connection.commit()
            print()
            print("Account closed - Returning to previous screen")
            print()
            return   
 


def main(): 
    #Check mysql database if there are any entries in table at all, if not populate table with info from json
    _SQL = """SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'bankingdb'"""

    cursor.execute(_SQL)

    results = cursor.fetchall()
    results = results[0]

    if results[0] == 0:
        create_new_db()


    print("Welcome to --- Banking" + "\n")
    print("Connecting to database")
    while(True):
        print("who are you:")
        user_input = input("Type: 0 = exit, 1 = Administrator, 2 = Account holder" + "\n")

        if user_input == "0":
            print("Bye, thank you for your patronage")
            break

        #if admin
        elif user_input == "1":

            while(True):
                print("what would you like to do?")

                user_input = input("type, 0 = exit, 1 = open new account, 2 = close account, 3 = modify account" + "\n")
                
                if user_input == "0":
                    print("Returning to previous screen" + "\n")
                    break

                elif user_input == "1":
                    print()
                    create_account()

                elif user_input == "2":
                    print()
                    close_account()

                elif user_input == "3":
                    print()
                    modify_account()
                
                else:
                    print("Invalid response: Please try again:")
                    
        #if account holder
        elif user_input == "2":
            acct = acct_sign_in()

            if acct == None:
                print("Database information colleciton error, returning to user identification screen")

            if acct == 1:
                print("Returning to user identification screen" + "\n")

            acct = list(acct)
            while(acct != 1):
                print("Welcome "+ acct[1] + " what would you like to do?")
                user_input = input("Type: 0 = exit, 1 = check balance, 2 = deposit, 3 = withdraw" + "\n")

                if user_input == "0":
                    print("Returning to previous screen" + "\n")
                    break

                elif user_input == "1":
                    print()
                    check_balance(acct)
                    
                elif user_input == "2":
                    print()
                    deposit(acct)

                elif user_input == "3":
                    print()
                    withdraw(acct)

                else:
                    print("Invalid response: " + user_input + " Please try again:")

        else:
            print("Invalid response: " + user_input + " Please try again:")
    return



#Start of stuff actually running

#config for connection to mysql
dbconfig = { 'host': 'localhost',
'user' : 'root',
'password' : 'Milbee12',
'database' : 'bankingdb'}

# create a connection to the mysql Server
try:
    connection = connect(**dbconfig)    
except Error as e:
    print(e)

# Get a cursor to send commands to the server and retrieve results
cursor = connection.cursor()


main()


# close the DB
cursor.close()
connection.close()