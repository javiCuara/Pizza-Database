# Main Script for terminal based application 
# CSE 111- Proj "Pizza Time""
import sqlite3
import sys
import re
import random
import os
# all querries will be on a seperate file /querries.py
# so we need to import the variables aka querries
from querries import*

def EstablishConnection():
    dB = "PizzaTime.db"
    try :
        # Sine path might not be the same we need to get current dir path
        # and add the databse name since they should be in the same folder
        path = os.getcwd() + dB 
        conn = sqlite3.connect(path)
        print("Connection Established");
    except ValueError:
        print("Could not connect to server !");
    return conn
#END OF ESTABLISH_CONNECTION 

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

    break;