# Proprietary
import sqlite3
import sys

# Created
from menus import*
from query import*

def CustomerPortal(con):
    storeChoice = StoreSelectMenu(con)   # Return the NAME of the store chosen
    if(storeChoice == "MAIN_MENU_RETURN"):
        return

    entreeChoice  = CustomerEntreeOrder(storeChoice, con)
    if(entreeChoice == "MAIN_MENU_RETURN"):
        return

    sideChoice  = CustomerSideOrder(storeChoice, con)
    if(sideChoice == "MAIN_MENU_RETURN"):
        return

    drinkChoice  = CustomerDrinkOrder(storeChoice, con)
    if(drinkChoice == "MAIN_MENU_RETURN"):
        return

    print('''
    You've ordered:
    {0}
    {1}
    {2}
    from {3}
    ''').format(entreeChoice, sideChoice, drinkChoice, storeChoice)

    # Now that we've completed the order, we have to do some database management
    # in the background to reflect the order.
    #
    # First, we have to create a new entry in the orders table
    # Second, we have to update (decrement) the stock of what was ordered by the customer
    # Third, we have to (EITHER BEFORE OR AFTER ORDERING) save the customer information

    # The first part, we now have to create a new entry in the orders table

    return

def StoreSelectMenu(con):
    cur = con.cursor()
    storeList = []      # The list of stores available in the database
    choice = ""         # The name of the store chosen by the user

    print("Which store would you like to order from?\n")

    result = cur.execute("SELECT st_name FROM store GROUP BY st_name;")
    data = result.fetchall()
    for row in data:
        storeList.append(row[0])

    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry)
        i += 1
    print("-1: Return to Main Menu\n")

    while(True):
        usrInput = raw_input("Enter value: ")
        print("---------------------------------------\n")
        try:
            usrInput = int(usrInput)
        except ValueError:
            print("ENTER A NUMBER PLEASE")
            continue

        if(usrInput == -1):
            return "MAIN_MENU_RETURN"
        elif(usrInput == 0):
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

        try:
            choice = storeList[usrInput - 1]
            break
        except IndexError:
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

    return choice

def CustomerEntreeOrder(store, con):
    cur = con.cursor()
    pizzaList = []
    choice = ""

    print("What kind of pizza would you like to order?\n")

    # Query for the pizzas available at the store provided
    result = cur.execute("SELECT e_name FROM store, entree WHERE st_storekey = e_storekey AND st_name = ? GROUP BY e_name; ", (store,))
    data = result.fetchall()
    for row in data:
        pizzaList.append(row[0])

    i = 1
    for entry in pizzaList:
        print("{0}: {1}").format(i, entry)
        i += 1
    print("-1: Return to Main Menu\n")

    while(True):
        usrInput = raw_input("Enter value: ")
        print("---------------------------------------\n")
        try:
            usrInput = int(usrInput)
        except ValueError:
            print("ENTER A NUMBER PLEASE")
            continue

        if(usrInput == -1):
            return "MAIN_MENU_RETURN"
        elif(usrInput == 0):
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

        try:
            choice = pizzaList[usrInput - 1]
            break
        except IndexError:
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

    return choice

def CustomerSideOrder(store, con):
    cur = con.cursor()
    sidesList = []
    choice = ""

    print("What kind of side would you like to order?\n")

    # Query for the pizzas available at the store provided
    result = cur.execute("SELECT s_name FROM store, sides WHERE st_storekey = s_storekey AND st_name = ? GROUP BY s_name; ", (store,))
    data = result.fetchall()
    for row in data:
        sidesList.append(row[0])

    i = 1
    for entry in sidesList:
        print("{0}: {1}").format(i, entry)
        i += 1
    print("-1: Return to Main Menu\n")

    while(True):
        usrInput = raw_input("Enter value: ")
        print("---------------------------------------\n")
        try:
            usrInput = int(usrInput)
        except ValueError:
            print("ENTER A NUMBER PLEASE")
            continue

        if(usrInput == -1):
            return "MAIN_MENU_RETURN"
        elif(usrInput == 0):
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

        try:
            choice = sidesList[usrInput - 1]
            break
        except IndexError:
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

    return choice

def CustomerDrinkOrder(store, con):
    cur = con.cursor()
    drinkList = []
    choice = ""

    print("What kind of drink would you like to order?\n")

    # Query for the pizzas available at the store provided
    result = cur.execute("SELECT d_brand FROM store, drink WHERE st_storekey = d_storekey AND st_name = ? GROUP BY d_brand; ", (store,))
    data = result.fetchall()
    for row in data:
        drinkList.append(row[0])

    i = 1
    for entry in drinkList:
        print("{0}: {1}").format(i, entry)
        i += 1
    print("-1: Return to Main Menu\n")

    while(True):
        usrInput = raw_input("Enter value: ")
        print("---------------------------------------\n")
        try:
            usrInput = int(usrInput)
        except ValueError:
            print("ENTER A NUMBER PLEASE")
            continue

        if(usrInput == -1):
            return "MAIN_MENU_RETURN"
        elif(usrInput == 0):
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

        try:
            choice = drinkList[usrInput - 1]
            break
        except IndexError:
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
            continue

    return choice
