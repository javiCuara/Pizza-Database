# Proprietary
import sqlite3
import sys
import os
import random
import fnmatch
import getpass
sys.path.insert(0,os.getcwd()+"/termcolor/termcolor.py")
from termcolor import colored, cprint

# Created
from menus import*
from query import*

def CheckCustomer(con):
    cur = con.cursor()
    tempPass = ''

    print(CustomerLoginMenu)
    while(True):
        choice = int(raw_input("Enter selection: "))

        if(choice == 3):
            return -1
        elif(choice == 1):
            while(True):
                print colored(Login, 'red')
                print colored(divider , 'red')
                usr = raw_input("Enter UserID: ")
                passw = str(getpass.getpass())
                print colored(divider , 'red')

                try:
                    result = con.execute(RetrieveCustPsw,(usr,))
                    data = result.fetchone();
                    if(data != None):   # only check if a value is returned
                        for r in data:
                            tempPass = r
                except sqlite3.Error, e:
                    print'Error: ', e.args[0]

                if(passw == tempPass):
                    return [usr, passw]
                else:
                    tmp = raw_input("1: Try again | 2: Return ~ ")
                    try:
                        tmp = int(tmp)
                    except ValueError:
                        print("INVALID INPUT\n")
                        continue
                    if int(tmp) == 1:
                        continue
                    elif int(tmp) == 2:
                        break

            return -1
        elif(choice == 2):
            #do another different thing
            return ['Guest', '']
        else:
            print("INVALID INPUT\n")

def CustomerPortal(login, con):
    cur = con.cursor()

    if(login[0] == 'Guest'):
        GuestPortal(con)
        return
    else:
        custKey = -1
        custAddress = ''
        custEmail = ''
        custName = ''
        custPhone = 0

        usr = login[0]
        passw = login[1]
        try:
            result = cur.execute(RetreiveCustInfo, (usr, passw,))
            data = result.fetchall()
            for row in data:
                custName = row[0]
                custEmail = row[1]
                custAddress = row[2]
                custKey = row[3]
                custPhone = row[4]
        except sqlite3.Error, e:
            print("Error: ", e.args[0])
            con.close()
            sys.exit(1)

        print("Will this order be for delivery?\n1: Yes\n2: No")
        while(True):
            delivery = raw_input("Please Make Your Selection: ")
            if(delivery == '1'):
                delivery = "YES"
                print('')
                break
            elif(delivery == '2'):
                delivery = "NO"
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
    try:
        count = -1

        # Entree Decrement
        result = cur.execute("SELECT e_stock FROM entree WHERE e_storekey = ? AND e_key = ?", (storeKey, entreeKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE entree SET e_stock = ? WHERE e_storekey = ? AND e_key = ?", (count, storeKey, entreeKey))
        con.commit()

        # Sides Decrement
        result = cur.execute("SELECT s_stock FROM sides WHERE s_storekey = ? AND s_key = ?", (storeKey, sideKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE sides SET s_stock = ? WHERE s_storekey = ? AND s_key = ?", (count, storeKey,  sideKey))
        con.commit()

        # Drink Decrement
        result = cur.execute("SELECT d_stock FROM drink WHERE d_storekey = ? AND d_key = ?", (storeKey, drinkKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE drink SET d_stock = ? WHERE d_storekey = ? AND d_key = ?", (count, storeKey, drinkKey))
        con.commit()
    except sqlite3.Error, e:
        print("Error: ", e.args[0])
        con.close()
        sys.exit(1)

    # Lastly, we have to add the customer to the delivery table (if the order was specified for delivery)
    if(delivery == 1):
        # Add another entry to the delivery table
        drivers = []
        result = cur.execute(myDrivers, (storeKey,))
        data = result.fetchall()
        for r in data:
            drivers.append(r[0])
        rnjesusBlessedThisDriver = random.choice(drivers)
        print(rnjesusBlessedThisDriver + " will be your deilvery driver\n")
        print("Thank you and have a nice day!")

        #Driver_name, order_id
        cur.execute("INSERT INTO Delivery VALUES (?, ?)", (rnjesusBlessedThisDriver, orderKey,))
        con.commit()

    return

def GuestPortal(con):
    cur = con.cursor()
    custKey = -1
    custAddress = ''
    custEmail = ''
    custName = ''
    guestPhone = 0000000000

    print("Will this order be for delivery?\n1: Yes\n2: No")
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
    try:
        count = -1

        # Entree Decrement
        result = cur.execute("SELECT e_stock FROM entree WHERE e_storekey = ? AND e_key = ?", (storeKey, entreeKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE entree SET e_stock = ? WHERE e_storekey = ? AND e_key = ?", (count, storeKey, entreeKey))
        con.commit()

        # Sides Decrement
        result = cur.execute("SELECT s_stock FROM sides WHERE s_storekey = ? AND s_key = ?", (storeKey, sideKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE sides SET s_stock = ? WHERE s_storekey = ? AND s_key = ?", (count, storeKey,  sideKey))
        con.commit()

        # Drink Decrement
        result = cur.execute("SELECT d_stock FROM drink WHERE d_storekey = ? AND d_key = ?", (storeKey, drinkKey,))
        data = result.fetchone()
        for r in data:
            count = r
        count -= 1
        cur.execute("UPDATE drink SET d_stock = ? WHERE d_storekey = ? AND d_key = ?", (count, storeKey, drinkKey))
        con.commit()
    except sqlite3.Error, e:
        print("Error: ", e.args[0])
        con.close()
        sys.exit(1)

    # Lastly, we have to add the customer to the delivery table (if the order was specified for delivery)
    if(delivery == 1):
        # Add another entry to the delivery table
        drivers = []
        result = cur.execute(myDrivers, (storeKey,))
        data = result.fetchall()
        for r in data:
            drivers.append(r[0])
        rnjesusBlessedThisDriver = random.choice(drivers)
        print(rnjesusBlessedThisDriver + " will be your deilvery driver\n")
        print("Thank you and have a nice day!")

        #Driver_name, order_id
        cur.execute("INSERT INTO Delivery VALUES (?, ?)", (rnjesusBlessedThisDriver, orderKey,))
        con.commit()

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
