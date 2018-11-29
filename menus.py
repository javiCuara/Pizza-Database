# Menu list 
MainMenu = '''
1: Continue as Guest
2: Continue as Store Manager
3: Exit
 '''

GuestMenu = ''' Select one of the following
    0: Return to main menu
    1: Count how many stores that sell Wings Deliver as well 
    2: For each store that carries beer, count how many delivery orders have been made
    '''

ManagerMenu = '''
0: Return to main menu
1:
2:
3:
'''

RetrievePsw = '''
SELECT Password
  FROM Managers
  WHERE Username = ?;
'''

RetrieveManagerStore = '''
SELECT M_store
  FROM Managers
  WHERE Username = ?;
'''

RetrieveStore = '''
SELECT st_name
  FROM store
  Where st_storekey = ?;'''


