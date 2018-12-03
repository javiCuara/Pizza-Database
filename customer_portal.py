# Proprietary
import sqlite3
import sys
import os
import fnmatch
sys.path.insert(0,os.getcwd()+"/termcolor/termcolor.py")
from termcolor import colored, cprint

# Created
from menus import*
from query import*

def CustomerPortal(con):
    cur = con.cursor()
    custKey = -1
    custAddress = ''
    custEmail = ''
    custName = ''
    guestPhone = 0000000000

    print('''Will this order be for delivery?
1: Yes
2: No
    ''')
    while(True):
        delivery = raw_input("Please Make Your Selection: ")
        if(delivery == '1'):
            delivery = "YES"
            custAddress = raw_input("Please enter your address:  ")
            print('')
            break
        elif(delivery == '2'):
            delivery = "NO"
            custAddress = 'NOT PROVIDED BY GUEST -- NO DELIV'
            print('')
            break
        else:
            print("INVALID INPUT\n")

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
    FROM {3}
    FOR DELIVERY: {4}
    ''').format(entreeChoice, sideChoice, drinkChoice, storeChoice, delivery)

    custName = raw_input("\nYour name for the order?   ")
    custName = "".join((custName,' (GUEST)'))
    while(True):
        custEmail = raw_input("Your email? We'll let you know when the order is ready!   ")
        filt = fnmatch.filter(custEmail, '*@*')
        if(len(filt) < 1):
            print("Enter a valid Email please!\n")
            continue
        else:
            break


    #Now we add them to the Customer table in the database
    try:
        results = cur.execute("SELECT MAX(c_key) FROM Customer;")
        data = results.fetchone()
        for r in data:
            custKey = r
        custKey += 1
    except sqlite3.Error, e:
        print("Error: ", e.args[0])

    #c_name, c_email, c_address, c_key, c_phone
    cur.execute(InsertNewCustomer, {"name": custName, "email": custEmail, "addr": custAddress, "key": custKey, "phone": guestPhone})
    con.commit()


    # Now that we've completed the order, we have to do some database management
    # in the background to reflect the order.
    #
    # First, we have to create a new entry in the orders table
    # Second, we have to update (decrement) the stock of what was ordered by the customer

    # The first part, we now have to automatically create a new entry in the orders table
    orderKey = -1
    sideKey = -1
    entreeKey = -1;
    drinkKey = -1;
    storeKey = -1;

    try:
        result = cur.execute("SELECT MAX(o_orderkey) FROM Orders")
        data = result.fetchone()
        for r in data:
            orderKey = r
        orderKey += 1

        result = cur.execute(getStoreKey, (storeChoice,))
        data = result.fetchone()
        for r in data:
            storeKey = r

        result = cur.execute(getSideKey, (storeKey, sideChoice,))
        data = result.fetchone()
        for r in data:
            sideKey = r

        result = cur.execute(getEntreeKey, (storeKey, entreeChoice,))
        data = result.fetchone()
        for r in data:
            entreeKey = r

        result = cur.execute(getDrinkKey, (storeKey, drinkChoice,))
        data = result.fetchone()
        for r in data:
            drinkKey = r

        if(delivery == 'YES'):
            delivery = 1
        else:
            delivery = 0
    except sqlite3.Error, e:
        print("Error: ", e.args[0])
        con.close()
        sys.exit(1)

    #'o_custkey', 'o_orderkey', 'o_side', 'o_entree', 'o_drink', 'o_store', 'o_dev'
    cur.execute(UpdateOrders, (custKey, orderKey, sideKey, entreeKey, drinkKey, storeKey, delivery,))
    con.commit()

    # Secondly, we have to decrease the stock of what was chosen. We saved the choices
    # as variables which we can use to query and modify the stock count

    # DO THE THING WITH STOCK DECREMENT

    # Lastly, we have to add the customer to the delivery table, should we actually

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

# def check_for_Injections(broma):
#     tmp = broma.upper();
#     if 'LIKE' in tmp:
#         return True
#     elif 'SELECT' in tmp:
#         return True
#     elif 'INSERT' in tmp:
#         return True
#     elif 'UPDATE' in tmp:
#         return True
#     elif 'DELETE' in tmp:
#         return True
#     elif 'DROP' in tmp:
#         return True
#     elif 'CREATE' in tmp:
#         return True
#     else:
#         return False
# def InsertEntree(con,key):
#     newE_key = 0
#     E_name = "Something"
#     cur = con.cursor()

#     result = cur.execute(getMaxEntree_key, (key,))
#     data = result.fetchall()

#     for r in data:
#         newE_key = r[0] +1

#     # once that is done then ask user what they want to input
#     while True:
