import sqlite3
import sys
import re
import random
import os
import getpass
from querries import*

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
            data = con.execute(Retrive_Psw,(Username,))
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
                data = con.execute(Retrive_skey,(Username,))
                x = data.fetchone();
                for r in x :
                    key = r
                # get store name
                data = con.execute(Retrive_Store,(key,))
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


def Manager_stuff(con):
    while True:
        print(Manager_menu)
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break

def Guest_stuff(con):
    while True:
        print(Guest_Menu)
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break
        elif int(tmp) == 1 :
            CountWingsAndDelivery(con);
        elif int(tmp) == 2 :
            CountStores_W_BeerAndWings(con);
    return

def CountWingsAndDelivery(con):
    cursor =  con.cursor();
    try:
        cur = con.cursor();
        data = con.execute(Count_Wings_AND_Deliver,)
        x = data.fetchone();
        for r in x:
            amt = r
            print"Number of stores: " ,amt;
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
#END OF COUNT_WINGS_AND_DELIVERY

def CountStores_W_BeerAndWings(con):
    cursor =  con.cursor();
    try:
        cur = con.cursor();
        data = con.execute(Count_Store_WithBeer,)
        x = data.fetchone();
        for r in x:
            amt = r
            print"Number of stores: " ,amt;
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
#END OF COUNT_STORES_WITH_WINGS_AND_BEER



con = EstablishConnection()

while True:
    print (Inital_Menu)
    tmp = raw_input("Enter Value: ")
    try:
        tmp = int(tmp)
    except ValueError:
        print("ENTER A NUMBER, PLEASE\n")
        continue
    if int(tmp) == 2 :
        if (CheckManager(con)):
            Manager_stuff(con)
    elif int(tmp) == 3:
        con.close();
        sys.exit(1);
    elif int(tmp) == 1:
        Guest_stuff(con)

