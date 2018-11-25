import sqlite3
import sys
import re
import random
import os
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









































connection = False
while True:
    print(Menu)
    tmp = raw_input("Enter value: ")
    try:
        tmp = int(tmp)
    except ValueError:
        print("ENTER A NUMBER, PLEASE\n")
        print("\n")
        continue
    if  int(tmp) == 0 :
        con = EstablishConnection()
        connection = True
    elif int(tmp) == -1:
        if connection:
            con.close();
        sys.exit(1);
    elif int(tmp) == 1 :
        CountWingsAndDelivery(con);
    elif int(tmp) == 2 :
        CountStores_W_BeerAndWings(con);
