# Proprietary
import sqlite3
import sys
import os
sys.path.insert(0,os.getcwd()+"/termcolor/termcolor.py") # dont delete this tory its needed!!!!!!

# sys.path.append('.../')import re
import getpass
import time
from termcolor import colored, cprint
# Created
from menus import*
from query import*

def CheckManager(con):
     # ask for credentials
    s_key = -9
    cur =  con.cursor();
    tmpWord = "something"
    while True:
        print colored(Login, 'red')
        print colored(divider , 'red')
        Username = raw_input("Enter UserID: ")
        Pass = str(getpass.getpass())
        print colored(divider , 'red')
        # now that we have inputs check if they are valid
        try:
            cur =  con.cursor();
            data = con.execute(RetrievePsw,(Username,))
            x = data.fetchone();
            if x != None:   # only check if a value is returned
                for r in x :
                    tmpWord = r
        except sqlite3.Error, e:
            print'Error: ', e.args[0]

        #check credentials
        if Pass == tmpWord:
            try:
                # get store key
                cur = con.cursor();
                data = con.execute(RetrieveManagerStore,(Username,))
                x = data.fetchone();
                for r in x:
                    key = r
                s_key = key

                break
            except sqlite3.Error, e:
                print'Error: ', e.args[0]

        # if credentials are not valid then ask....
        else:
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
            else:
                break
    # when loop ends then return boolean
    return s_key

def ManagerPortal(con, key):
    cur = con.cursor()

    while True:
        try:
            # get store name
            data = cur.execute(RetrieveStore, [key])
            x = data.fetchone();
            for r in x :
                name = r
                # print store name
                # print 'Welcome Manager:', name
        except sqlite3.Error, e:
            print("Error: ", e.args[0])
            print("Problem Determining Store, returning to main menu.")
            return
        printGreeting(key)
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

        elif int(tmp) == 1:
            getTotalInventory(con,key)

        elif int(tmp) == 2:
            IndividualStock(con, key)

        elif int(tmp) == 3:
            updateInventory(con,key)

        elif int(tmp)  == 4:
            viewBestSelling(con,key)

        elif int(tmp)  == 5:
           viewBest_sellingCombination(con,key)
        
        elif int(tmp)  == 6:
           List_Customers(con,key)
        
        elif int(tmp)  == 7:
            Vip_customer(con,key)

        elif int(tmp)  == 8:
            List_myDrivers(con,key)
        
        elif int(tmp) == 9:
            reviewCustomerXXXOrder(con,key)
        
        elif int(tmp) == 10:
            print colored(divider,'red')
            goToInsertPortal(con,key)
        elif int(tmp) == 11:
            print colored(divider,'red')
            goToDeletePortal(con,key)


def goToInsertPortal(con,key):
    print Insert_menu
    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break
        elif int(tmp) == 1:
            InsertEntree(con,key)
            break

        elif int(tmp) == 2:
            InsertDrink(con,key)
            break

        elif int(tmp) == 3:
            InsertSide(con,key)
            break

        elif int(tmp) == 4:
            InsertSauce(con,key)
            break

        elif int(tmp) == 5:
            InsertTopping(con,key)
            break

def goToDeletePortal(con,key):
    print Delete_menu
    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break
        elif int(tmp) == 1:
            deleteEntree(con,key)
            break
        elif int(tmp) == 2:
            deleteDrink(con,key)
            break
        elif int(tmp) == 3:
            deleteSide(con,key)
            break
        elif int(tmp) == 5:
            deleteTopping(con,key)
            break
        elif int(tmp) == 4:
            deleteSauce(con,key)
            break


def getTotalInventory(con,key):
    Top = getToppings(con,key)
    Sides = getSides(con,key)
    sauce = getSauce(con,key)
    entree = getEntree(con,key)
    drink = getDrink(con,key)

    print("              Toppings                ")
    print("---------------------------------------")
    for i in Top:
        print '|',i[0],' \t|',i[1]
    print("---------------------------------------\n")

    print("               Sides                    ")
    print("---------------------------------------")
    for i in Sides:
        print '|',i[0],'|',i[1]
    print("---------------------------------------\n")

    print("               Sauces                    ")
    print("---------------------------------------")
    for i in sauce:
        print '|',i[0],' \t|',i[1]
    print("---------------------------------------\n")

    print("               Entrees                   ")
    print("---------------------------------------")
    for i in entree:
        print '|',i[0],' \t|',i[1]
    print("---------------------------------------\n")

    print("               Drinks                    ")
    print("---------------------------------------")
    for i in drink:
        print '|',i[0],' \t|',i[1]
    print("---------------------------------------\n")

def getToppings(con,key):
    cur = con.cursor()
    T_List = []
    #print key
    result = cur.execute(ToppingStock, (key,))
    data = result.fetchall()
    for r in data:
       T_List.append((r[0],r[1]))
    #print data
    return T_List

def getSides(con, key):
    cur = con.cursor()
    T_List = []
    #print key
    result = cur.execute(SideStock, (key,))
    data = result.fetchall()
    for r in data:
       T_List.append((r[0],r[1]))
    #print data
    return T_List

def getSauce(con,key):
    cur = con.cursor()
    T_List = []
    #print key
    result = cur.execute(sauceStock, (key,))
    data = result.fetchall()
    for r in data:
       T_List.append((r[0],r[1]))
    #print data
    return T_List

def getEntree(con,key):
    cur = con.cursor()
    T_List = []
    #print key
    result = cur.execute(entreStock, (key,))
    data = result.fetchall()
    for r in data:
       T_List.append((r[0],r[1]))
    #print data
    return T_List

def getDrink(con,key):
    cur = con.cursor()
    T_List = []
    #print key
    result = cur.execute(drinkStock, (key,))
    data = result.fetchall()
    for r in data:
       T_List.append((r[0],r[1]))
    #print data
    return T_List


def IndividualStock(con,key):
    getList = []
    entrySuccess = False
    mainReturn = False
    availableTables = ["entree", "drink","sauce","sides","toppings"]
    while True:
        print(Indiv_Inventory)
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) == 0 :
            break

        elif int(tmp) == 1:
            getList = getEntree(con, key)
            print("\n              Entrees")

        elif int(tmp) == 2:
            getList = getDrink(con, key)
            print("\n              Drinks:")

        elif int(tmp) == 3 :
            getList = getSauce(con, key)
            print("\n              Sauce")

        elif int(tmp) == 4:
            getList =getSides(con, key)
            print("\n              Sides")

        elif int(tmp) == 5:
            getList = getToppings(con, key)
            print("\n              Toppings")

        print("---------------------------------------")
        for i in getList:
            print '|',i[0],' \t|',i[1]
        print("---------------------------------------\n")

        # Ask User if they want to modify data
        while True and entrySuccess:
            print("Would You like to modify this table?")
            ans = raw_input("Enter: 1 for yes | 2 for no ~ ")
            try:
                ans = int(ans)
            except ValueError:
                print("ENTER A NUMBER, PLEASE\n")
                print("\n")
                continue
            if  int(ans) == 2 :
                break
            elif int(ans) == 1:
                    update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp)) # darn indexing
                    # print("---------------------------------------\n")
                    return

def update_Selected_Inventory(con, key, selected_table, table_key):
    amount = 0
    isNegative = False
    selected_item = "boo"
    index = 0
    newTotal = 0
    getSchema  = "PRAGMA table_info(" + selected_table + ");"
    # print 'hey u made it here: ', selected_table
    # first get the table schema and find they item key
    cur = con.cursor()
    T_List = []
    getList = []
    #print key
    result = cur.execute(getSchema, )
    data = result.fetchall()
    for r in data:
        T_List.append(r[1])
        # print(r[1])

    # print the options to update
    if table_key == 1:
        getList = getEntree(con, key)
        print("\n              Entrees")

    elif table_key == 2:
        getList = getDrink(con, key)
        print("\n              Drinks:")

    elif table_key == 3 :
        getList = getSauce(con, key)
        print("\n              Sauce")

    elif table_key == 4:
        getList =getSides(con, key)
        print("\n              Sides")

    elif table_key == 5:
        getList = getToppings(con, key)
        print("\n              Toppings")

    print("---------------------------------------")
    z = 1
    for i in getList:
        if(selected_table == 'entree'):
            print z,':',i[0], 'pizza'
        else: 
            print z,':',i[0]
        z += 1
    print("---------------------------------------\n")

    print("Please select what item you want to update")

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,z):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  getList[index]
            selected_item = selected_item[0]
            break
    print("Do you wish to increment or decrement stock ?")
    value = ''
    while True:
        option =  raw_input("Enter: 1 for Increment | 2 for Decrement ~ ")
        try:
            option = int(option)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if int(option) == 1:
            while True:
                inv =  getList[index]
                inv = inv[1]
                print 'Current Inventory is: ' , inv
                value = raw_input( "Enter amount: ")
                try:
                     value = int(value)
                except ValueError:
                     print("ENTER A NUMBER, PLEASE\n")
                     print("\n")
                     continue
                if int(value) >= 0:
                    check = int(inv) + int(value)
                    print'New Stock for ' , selected_item , ' is ' , check
                    newTotal = check
                    break
                else :
                    print("Enter a positive number")
            break
        elif int(option) == 2:
            while True:
                inv =  getList[index]
                inv = inv[1]
                print 'Current Inventory is: ' , inv
                value = raw_input( "Enter amount: ")
                try:
                     value = int(value)
                except ValueError:
                     print("ENTER A NUMBER, PLEASE\n")
                     print("\n")
                     continue
                if int(value) >= 0:
                    check = int(inv) - int(value)
                    if check < 0:
                        print("You cannot have negative stock!")
                    else:
                        print'New Stock for ' , selected_item , ' is ' , check
                        newTotal = check
                        break
                else :
                    print("Enter a positive number")
            break
    # print("Updating information ...")
    print colored(Updating,'red')
    print colored(divider , 'red')

    name = "boo"
    table_name_stock = "meh"
    store_column = "yyy"
    for r in T_List:
        if "name"  in r or 'brand' in r:
            name = r
            # print r
            break
    for r in T_List:
        if 'stock' in r:
            table_name_stock = r
            # print r
            break

    for r in T_List:
        if 'storekey' in r or 'offeredBy' in r :
            store_column = r
            # print r
            break

    try:
        query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(query,)
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination

def updateInventory(con, key):
    getList = []
    availableTables = ["entree", "drink","sauce","sides","toppings"]

    while True:
        print(Update_Menu)
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if int(tmp) == 0 :
            break
        
        elif int(tmp) == 1 :
            getList = getEntree(con, key)
            update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp))
            # print("\n              Entrees")

        elif int(tmp) == 2:
            getList = getDrink(con, key)
            update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp))
            # print("\n              Drinks:")

        elif int(tmp) == 3 :
            getList = getSauce(con, key)
            update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp))
            # print("\n              Sauce")

        elif int(tmp) == 4:
            getList =getSides(con, key)
            update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp))
            # print("\n              Sides")

        elif int(tmp) == 5:
            getList = getToppings(con, key)
            update_Selected_Inventory(con,key,availableTables[tmp-1],int(tmp))

def updateEntree(con, key):
    # List out options
    cur = con.cursor()
    storeList = []
    print("--------------------------------------")
    result = cur.execute("SELECT e_name,e_stock FROM entree WHERE e_storekey = ? GROUP BY e_name",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1]))

    print("Which Entree would you like to update?")
    i = 1
    for entry in storeList:
        print("{0}: {1}:{2}").format(i, entry[0], entry[1])
        i += 1
def retrive_Table_Information(con,key,selected_table):
    print("comming soon")

def viewBestSelling(con,key):
    items = []
    cur = con.cursor()
    result = cur.execute(getBestSelling_Items, (key,))
    data = result.fetchall()
    for row in data:
        # print row[0]
        items.append((row[0],row[1],row[2]))
    print 'These are the Best selling Items'
    for r in items:
        print '|' , r[0] , 'Pizza |' , r[1] , '|' , r[2]       
    print("--------------------------------------")

def viewBest_sellingCombination(con,key):
    order = []
    
    Entree = "something"
    Side = "Something"
    Drink = "Something"

    cur = con.cursor()
    result = cur.execute(Find_Most_Ordered_Combination, (key,))
    data = result.fetchall()
    
    for row in data:
        order.append((row[0],row[1],row[2]))
    # the query gives use the keys to the corresponding items 
    # now querry for them
    for r in order:
        Entree = r[0]
        Side = r[1]
        Drink = r[2]
    

    result = cur.execute("SELECT e_name FROM entree WHERE e_key = ? AND e_storekey = ? ", (Entree,key,))
    data = result.fetchall()
    for r in data :
        Entree = r[0]

    result = cur.execute("SELECT s_name FROM sides WHERE s_key = ? AND s_storekey = ? ", (Side,key,))
    data = result.fetchall()
    for r in data :
        Side = r[0]

    result = cur.execute("SELECT d_brand FROM drink WHERE d_key = ? AND d_storekey = ? ", (Drink,key,))
    data = result.fetchall()
    for r in data :
        Drink = r[0]


    print 'This is the Best selling order combination'
    print '|' , Entree , 'Pizza With' , Side, '&' , Drink       
    print("--------------------------------------")

def List_Customers(con,key):
    print("---------------------------------------")
    
    cur = con.cursor()
    result = cur.execute(Customer_List, (key,))
    data = result.fetchall()
    print 'These are our customers:'
    print("_______________________________________")
    i = 1
    for row in data:
        print i, ':', row[0]
        i+=1
    print("_______________________________________")
    print("---------------------------------------")

def Vip_customer(con,key):
    name = 'Jane Doe'
    cur = con.cursor()
    result = cur.execute(store_VIP, (key,))
    data = result.fetchall()
    print colored(divider , 'red')
    # print("_______________________________________")
    print colored(Mvp,'red') 
    for r in data:
        print '\t',r[0]
        name = r[0]
    # print("_______________________________________")
    print colored(divider , 'red')
    print "Would you like to see their favorite items?"
    while True:
        tmp = raw_input("Enter: 1 for Yes | 2 for No ~ ")
        try:
            tmp = int(tmp)
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if int(tmp) == 2 :
            break
        elif int(tmp) == 1:
            # print 'coming soon'
            MVP_FavOrder(con,key,name)
            break



def List_myDrivers(con,key):
    cur = con.cursor()
    result = cur.execute(myDrivers, (key,))
    data = result.fetchall()
    print('These are all active drivers:')
    print("_______________________________________")
    for r in data:
        print r[0]
    print("_______________________________________")

def MVP_FavOrder(con,key,name):
    cur = con.cursor()
    result = cur.execute(Mvps_favoriteOrder, (key,name,))
    data = result.fetchall()
    print("_______________________________________\n")
    print name, "favorite order is:"
    for r in data:
        print r[1] , 'Pizza with' , r[2] , 'and', r[3]
        # print r[0] 
        # print r[4]
    print("_______________________________________")

def printGreeting(key):
    if key == 1:
        # print hello
        # print To
        print colored(Dominos , 'red')
    elif key == 2:
        # print hello
        # print To
        print colored(PizzaHut , 'red')
    elif key == 3:
        # print hello
        # print To
        print colored(Mountain , 'red')
    elif key == 4:
        # print hello
        # print To
        print colored(PizzaPalace,'red')
    elif key == 5:
        # print hello
        # print To
        print colored(PizzaFactory,'red')
    elif key == 6:
        # print hello
        # print To
        print colored(PizzaGuys,'red')
    elif key == 7:
        # print hello
        # print To
        print colored(PizzaVilla,'red')
    elif key == 8:
        # print hello
        # print To
        print colored(PizzaLoca,'red')
    elif key == 9:
        # print hello
        # print To
        print colored(LittleOven,'red')

def printOrder(con, key, c_name,s_name):
    # print 'coming soon'
    cur = con.cursor()
    result = cur.execute(receiptForXYZ, (c_name,s_name,))
    data = result.fetchall()
    print c_name , 'Ordered:'
    print("_______________________________________")
    for r in data:
        print  r[1] , 'Pizza with' , r[2] , 'and' , r[3]
        print("-----------------------------------------")
        # print r
    print("_______________________________________")

def getCustomers(con,key):
    getList = []
    cur = con.cursor()
    result = cur.execute(Customer_List, (key,))
    data = result.fetchall()
    for r in data:
        getList.append(r[0])
    return getList

def getStoreName(con,key):
    Name = 'Something'
    cur = con.cursor()
    result = cur.execute("SELECT st_name FROM store WHERE st_storekey = ?", (key,))
    data = result.fetchall()
    for r in data:
        Name = r[0]
    return Name

def reviewCustomerXXXOrder(con,key):
    print '-1: To cancel'
    # this prints the customers
    List_Customers(con,key)
    # this gets them in a lis
    myCustomers = getCustomers(con,key)
    myRange = len(myCustomers)
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
        # elif(usrInput == 0):
        #     print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
        #     continue
        elif int(usrInput) not in range(1,myRange):
            print("***PLEASE CHOOSE FROM THE LIST PROVIDED***\n")
        else:
            choice = myCustomers[usrInput-1]
            storeName = getStoreName(con,key)
            printOrder(con,key,choice,storeName)
            print colored(divider,'red')
            time.sleep(1)
            break

def check_for_Injections(broma):
    tmp = broma.upper();
    if 'LIKE' in tmp:
        return True
    elif 'SELECT' in tmp:
        return True
    elif 'INSERT' in tmp:
        return True
    elif 'UPDATE' in tmp:
        return True
    elif 'DELETE' in tmp:
        return True
    elif 'DROP' in tmp:
        return True
    elif 'CREATE' in tmp:
        return True
    else:
        return False

def checkForNumbers(broma):
    try:
        broma =  int(broma)
        return True
    except ValueError:
        return False
def InsertTopping(con,key):
    newS_key = 0
    S_name = "Something"
    # D_type = "Something"
    S_stock = 0
    # Ingredients = []
    cur = con.cursor()

    result = cur.execute(getMaxToppint_key, (key,))
    data = result.fetchall()
    
    for r in data:
        newS_key = r[0] +1
    
    # once that is done then ask user what they want to input
    while True:
        S_name = str(raw_input('Enter Topping name : '))
        if (check_for_Injections(S_name)) or (checkForNumbers(S_name)) or (len(S_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    
    while True:
        tmp = raw_input('Enter the current inventory stock: ')
        try:
            tmp = int(tmp)
        except ValueError:
            print 'Please enter a number'
            continue
        if tmp < 0:
            print 'You cant have negative stock'
        else :
            S_stock = tmp
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Insert_intoToppings,(S_name ,  newS_key , key ,S_stock , ))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination

def InsertSauce(con,key):
    newS_key = 0
    S_name = "Something"
    # D_type = "Something"
    S_stock = 0
    # Ingredients = []
    cur = con.cursor()

    result = cur.execute(getMaxSide_key, (key,))
    data = result.fetchall()
    
    for r in data:
        newS_key = r[0] +1
    
    # once that is done then ask user what they want to input
    while True:
        S_name = str(raw_input('Enter Sauce name : '))
        if (check_for_Injections(S_name)) or (checkForNumbers(S_name)) or (len(S_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    
    while True:
        tmp = raw_input('Enter the current inventory stock: ')
        try:
            tmp = int(tmp)
        except ValueError:
            print 'Please enter a number'
            continue
        if tmp < 0:
            print 'You cant have negative stock'
        else :
            S_stock = tmp
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Insert_intoSauce,(S_name ,  newS_key , key ,S_stock , ))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination
def  InsertSide(con,key):
    newS_key = 0
    S_name = "Something"
    # D_type = "Something"
    S_stock = 0
    # Ingredients = []
    cur = con.cursor()

    result = cur.execute(getMaxSide_key, (key,))
    data = result.fetchall()
    
    for r in data:
        newS_key = r[0] +1
    
    # once that is done then ask user what they want to input
    while True:
        S_name = str(raw_input('Enter Side name : '))
        if (check_for_Injections(S_name)) or (checkForNumbers(S_name)) or (len(S_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    
    while True:
        tmp = raw_input('Enter the current inventory stock: ')
        try:
            tmp = int(tmp)
        except ValueError:
            print 'Please enter a number'
            continue
        if tmp < 0:
            print 'You cant have negative stock'
        else :
            S_stock = tmp
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Insert_intoSides,(S_name ,  S_stock , key , newS_key ,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination
def InsertDrink(con,key):
    newD_key = 0
    D_brand = "Something"
    D_type = "Something"
    D_stock = 0
    # Ingredients = []
    cur = con.cursor()

    result = cur.execute(getMaxSauce_key, (key,))
    data = result.fetchall()
    
    for r in data:
        newD_key = r[0] +1
    
    # once that is done then ask user what they want to input
    while True:
        D_brand = str(raw_input('Enter Drink name : '))
        if (check_for_Injections(D_brand)) or (checkForNumbers(D_brand)) or (len(D_brand)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    while True:
        D_type = str(raw_input('Enter Drink type : '))
        if (check_for_Injections(D_type)) or (checkForNumbers(D_type)) or (len(D_type)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    while True:
        tmp = raw_input('Enter the current inventory stock: ')
        try:
            tmp = int(tmp)
        except ValueError:
            print 'Please enter a number'
            continue
        if tmp < 0:
            print 'You cant have negative stock'
        else :
            D_stock = tmp
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Insert_intoDrink,(D_type , newD_key , D_stock , D_brand , key ,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination


def InsertEntree(con,key):
    newE_key = 0
    E_name = "Something"
    E_stock = 0
    Ingredients = []
    cur = con.cursor()

    result = cur.execute(getMaxEntree_key, (key,))
    data = result.fetchall()
    
    for r in data:
        newE_key = r[0] +1
    
    # once that is done then ask user what they want to input
    while True:
        E_name = str(raw_input('Enter Entree name <No need to add Pizza to name> : '))
        if (check_for_Injections(E_name)) or (checkForNumbers(E_name)) or (len(E_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            break
    
    while True:
        tmp = raw_input('Enter the current inventory stock: ')
        try:
            tmp = int(tmp)
        except ValueError:
            print 'Please enter a number'
            continue
        if tmp < 0:
            print 'You cant have negative stock'
        else :
            E_stock = tmp
            break
    while True:
        tString = str(raw_input('Enter the crust: '))
        if (check_for_Injections(E_name)) or (checkForNumbers(E_name)) or (len(E_name)>20): 
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            tString = tString + ' - '
            Ingredients.append(tString)
            break
    while True:
        tString = str(raw_input('Enter the sauce: '))
        if (check_for_Injections(E_name)) or (checkForNumbers(E_name)) or (len(E_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        else:
            tString = tString + ' - '
            Ingredients.append(tString)
            break
    Ingredients_counter = 0        
    print 'Max number of toppings per Pizza is 3'
    print "Type 'Done' to stop"
    while True:
        # print Ingredients_counter
        tString = str(raw_input('Enter a toping: '))
        if (check_for_Injections(E_name)) or (checkForNumbers(E_name)) or (len(E_name)>24):
            print colored('PLEASE INSERT A valid Input', 'red') 
        elif tString.upper() == 'DONE':
            break
        elif Ingredients_counter >=2:
            tString = tString + ' - '
            Ingredients.append(tString)
            break
        else:
            tString = tString + ' - '
            Ingredients.append(tString)
            # break
        Ingredients_counter += 1
    # now we need to make a new string 
    E_toppings = " ".join(Ingredients)
    # print E_toppings
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Insert_intoEntree,(E_name,key,E_stock,newE_key,E_toppings,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination
def deleteEntree(con,key):
    cur = con.cursor()
    storeList = []
    selected_item =  []
    print("--------------------------------------")
    result = cur.execute("SELECT e_name,e_stock,e_key FROM entree WHERE e_storekey = ? GROUP BY e_name",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1],row[2]))

    print("Which Entree would you like to Delete?")
    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry[0])
        i += 1

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,i):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  storeList[index]
            # selected_item = selected_item[0]
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Delete_FromEntree,(selected_item[0],key,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)     # Unexpected Termination
    # print selected_item
    # print selected_item[0]
    # print selected_item[0][0]


def deleteDrink(con,key):
    cur = con.cursor()
    storeList = []
    selected_item =  []
    print("--------------------------------------")
    result = cur.execute("SELECT d_brand ,d_stock,d_key FROM drink WHERE d_storekey = ? GROUP BY d_brand",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1],row[2]))

    print("Which drink would you like to Delete?")
    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry[0])
        i += 1

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,i):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  storeList[index]
            # selected_item = selected_item[0]
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Delete_FromEntree,(selected_item[0],key,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)
    # print 'Comming soon'
def deleteSide(con,key):
    cur = con.cursor()
    storeList = []
    selected_item =  []
    print("--------------------------------------")
    result = cur.execute("SELECT s_name ,s_stock,s_key FROM sides WHERE s_storekey = ? GROUP BY s_name",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1],row[2]))

    print("Which side would you like to Delete?")
    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry[0])
        i += 1

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,i):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  storeList[index]
            # selected_item = selected_item[0]
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Delete_FromSides,(selected_item[0],key,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)
def deleteSauce(con,key):
    cur = con.cursor()
    storeList = []
    selected_item =  []
    print("--------------------------------------")
    result = cur.execute("SELECT sc_name ,sc_stock,sc_key FROM sauce WHERE sc_offeredBy = ? GROUP BY sc_name",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1],row[2]))

    print("Which sauce would you like to Delete?")
    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry[0])
        i += 1

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,i):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  storeList[index]
            # selected_item = selected_item[0]
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Delete_FromSides,(selected_item[0],key,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)
def deleteTopping(con,key):
    cur = con.cursor()
    storeList = []
    selected_item =  []
    print("--------------------------------------")
    result = cur.execute("SELECT t_name ,t_stock,t_key FROM toppings WHERE t_storekey = ? GROUP BY t_name",(key,))
    data = result.fetchall()
    for row in data:
        storeList.append((row[0],row[1],row[2]))

    print("Which topping would you like to Delete?")
    i = 1
    for entry in storeList:
        print("{0}: {1}").format(i, entry[0])
        i += 1

    while True:
        tmp = raw_input("Enter value: ")
        try:
            tmp = int(tmp)
            entrySuccess = True
        except ValueError:
            print("ENTER A NUMBER, PLEASE\n")
            print("\n")
            continue
        if  int(tmp) not in range(1,i):
            print("***Please enter a valid number***")

        else :
            index = int(tmp)-1
            selected_item =  storeList[index]
            # selected_item = selected_item[0]
            break
    try:
        # query = UpdateTable(selected_table, table_name_stock, newTotal, name, selected_item, store_column, key)
        cur.execute(Delete_FromToppings,(selected_item[0],key,))
        con.commit();
        time.sleep(2)
        print colored(success,'red')
        print colored(divider , 'red')
        #  print("____________________________________________________________________________________________")

        # print("Database updated successfuly!\n")
    except sqlite3.Error, e:
        print'Error: ', e.args[0]
        con.close()
        sys.exit(1)