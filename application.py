# Proprietary
import sqlite3
import sys
import os
sys.path.insert(0,os.getcwd()+"/termcolor/termcolor.py") # dont delete this tory its needed!!!!!!

from termcolor import colored, cprint


# Created
from menus import*
from manager_portal import*
from customer_portal import*


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


con = EstablishConnection()
print colored(Welcome , 'red')
print colored(pizzaIcon, 'red')
# print("________________________________________________________________________________________")

while True:
    
    print(MainMenu)
    cprint
    tmp = raw_input("Enter Value: ")
    try:
        tmp = int(tmp)
    except ValueError:
        print("ENTER A NUMBER, PLEASE\n")
        continue

    if int(tmp) == 2 :
        ky = CheckManager(con)
        if (ky != -9):
            ManagerPortal(con,ky)
    elif int(tmp) == 3:
        # print("____________________________________________________________________________________________")
        print colored(divider , 'red')
        print colored(ByeBye, 'red')
        con.close();
        sys.exit(0);    # Expected Termination
    elif int(tmp) == 1:
        print colored(divider , 'red')
        CustomerPortal(con)
