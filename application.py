import sqlite3
import sys
import re
import random
import os
import getpass
from menus import*

def EstablishConnection():
    dB = "/PizzaTime.db"
    try :
        path = os.getcwd() + dB 
        conn = sqlite3.connect(path)
        print("Connection Established");
    except ValueError:
        print("Could not connect to server !");
    return conn
#END OF ESTABLISH_CONNECTION

def CheckManager(con):
     # ask for credentials
    connect = False
    cur =  con.cursor();
    tmpWord = "something"
    while True: 
        print("-------------------------------------- " )
        Username = raw_input("Enter UserID: ")
        Pass = str(getpass.getpass())
        print("-------------------------------------- " )
        # now that we have inputs check if they are valid
        try:
            cur =  con.cursor();
            data = con.execute(RetrievePsw,(Username,))
            x = data.fetchone();
            if x  != None: # only while a value is returned
                for r in x :
                    tmpWord = r
        except sqlite3.Error, e:
            print'Error: ', e.args[0]

        #check credentials
        if Pass == tmpWord : 
            try:
                # get store key
                cur =  con.cursor();
                data = con.execute(RetrieveStore,(Username,))
                x = data.fetchone();
                for r in x :
                    key = r
                # get store name
                data = con.execute(RetriveStore,(key,))
                x = data.fetchone();
                for r in x :
                    name = r
                # print store name
                print 'Welcome Manager:', name
                connect = True # condition is met
                break
            except sqlite3.Error, e:
                print'Error: ', e.args[0]

        # if credentials are not valid then ask....
        else :
            tmp = raw_input("1:Try again | 2: Return ~")
            try:
                tmp = int(tmp)
            except ValueError:
                print("ENTER A NUMBER, PLEASE\n")
                continue
            if int(tmp) == 1:
                continue
            elif int(tmp) == 2:
                break
            else :
                break
    # when loop ends then return boolean 
    return connect


def ManagerPortal(con):
    while True:
        print(ManagerMenu)
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break

def CustomerPortal(con):
    choice = StoreSelectMenu(con)
    print(choice)

    return

def StoreSelectMenu(con):
    cur = con.cursor()
    StoreList = []
    
    result = cur.execute("SELECT st_name FROM store GROUP BY st_name;")
    data = result.fetchall()
    tempStoreName = ""
    for row in data:
        StoreList.append(row[0])

    print("Which store would you like to order from?")
    i = 1
    for entry in StoreList:
        print("{0}: {1}").format(i, entry)
        i += 1

    usrInput = raw_input("Enter value: ")
    try:
        usrInput = int(usrInput)
    except ValueError:
        print("ENTER A NUMBER PLEASE")
        print("\n")
    
    return usrInput


con = EstablishConnection()

while True:
    print (MainMenu)
    
    tmp = raw_input("Enter Value: ")
    try:
        tmp = int(tmp)
    except ValueError:
        print("ENTER A NUMBER, PLEASE\n")
        continue

    if int(tmp) == 2 :
        if (CheckManager(con)):
            ManagerPortal(con)
    elif int(tmp) == 3:
        con.close();
        sys.exit(1);
    elif int(tmp) == 1:
        CustomerPortal(con)

