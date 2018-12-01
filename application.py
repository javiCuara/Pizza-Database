# Proprietary
import sqlite3
import sys
import os

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
while True:
    print (MainMenu)

    tmp = raw_input("Enter Value: ")
    print("---------------------------------------\n")
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
        con.close();
        sys.exit(1);
    elif int(tmp) == 1:
        CustomerPortal(con)
