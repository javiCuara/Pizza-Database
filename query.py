RetrievePsw = '''
SELECT Password
  FROM Managers
  WHERE Username = ?;
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

prepared_Update = '''
Update ?
  Set ? = ?
  WHERE ? = ? AND ? = ?;
'''

# Retrive topping inventory for store ?
ToppingStock = '''SELECT t_name,
       t_stock
  FROM toppings
  WHERE t_storekey = ?
  GROUP BY t_name;'''

SideStock = '''SELECT s_name,
       s_stock
  FROM sides
Where s_storekey = ?
GROUP BY s_name;'''

sauceStock = '''SELECT sc_name,
       sc_stock
  FROM sauce
  WHERE sc_offeredBy = ?
  GROUP BY sc_name;'''

entreStock = '''
SELECT e_name,
       e_stock
  FROM entree
  WHERE e_storekey = ?
  GROUP BY e_name; '''

drinkStock = '''
SELECT d_brand,
       d_stock
  FROM drink
  WHERE  d_storekey = ?
  GROUP BY d_brand;'''

getBestSelling_Items = ''' 
SELECT Q3.Entree , Q2.Side , Q1.Drink 
FROM getBestDrink  Q1,
     getBestSide  Q2, 
     getBestEntree  Q3
 Where Q1.Store = Q2.Store AND 
       Q3.Store = Q1.Store AND 
       Q1.Store = ?
'''

def UpdateTable(tableName, attrToUpdate, updateValue, attrItemName, itemName, attrKey, key):
    query = "UPDATE " + str(tableName) + " SET " + str(attrToUpdate) + " = " + str(updateValue) +  " WHERE " + str(attrItemName) + " = " + '"' + str(itemName) + '"' + " AND " + str(attrKey) + " = " + str(key) + ";"
    return query

# -- 1) Count how many stores that sell Wings Deliver as well
Count_Wings_AND_Deliver ='''
 SELECT COUNT(DISTINCT st_name)
  FROM sides,
       store,
       Orders
 WHERE s_storekey = st_storekey AND
       s_name LIKE "%Wings%" AND
       st_orderkey = o_orderkey AND
       o_dev = 1;
'''
#-- 2) for each store that carries beer, count how many delivery orders have been made
Count_Store_WithBeer = '''
SELECT COUNT(DISTINCT order_id)
  FROM drink,
       Orders,
       store,
       Delivery
 WHERE order_id = o_orderkey AND
       d_type = "beer" AND
       o_drink = d_key
 GROUP BY st_storekey;
 '''
#-- 3) Count how many ordered pizzas that have mushrooms are in each type of pizza at Pizza Factory
Count_MushroomPizzas_Factory = '''
SELECT COUNT( * )
  FROM store,
       Orders,
       entree,
       toppings
 WHERE st_orderkey = o_orderkey AND
       o_entree = e_key AND
       e_ingredients LIKE "%Mushroom%" AND
       st_name = "Pizza Factory";
 '''
 #-- 4) For each store, which drink is least ordered (which has the most stock)
ListStores_MostSoldDrink = '''
SELECT st_name,
       d_brand
  FROM store,
       drink
 WHERE d_storekey = st_storekey
 GROUP BY st_name
HAVING MAX(d_stock);
'''
#-- 5) For each customer that Dominos delivers to, find their order (entree, drink, side)
ListDeliveredOrder_FromCustomerDominos = '''
SELECT e_name,
       d_brand,
       s_name
  FROM Customer,
       entree,
       sides,
       drink,
       Orders,
       store,
       Delivery
 WHERE order_id = st_orderkey AND
       st_orderkey = o_orderkey AND
       o_custkey = c_key AND
       o_drink = d_key AND
       o_entree = e_key AND
       o_side = s_key AND
       st_name = "Dominos"
 GROUP BY c_name;
'''
#6-- 6) Take the inventory of each side, entree ingredient, and drink for each store that offers tea
Inv_forStores_OfferTea = '''
    SELECT q.name, COUNT(d_stock), COUNT(s_stock), COUNT(t_stock)
     FROM drink, sides, toppings,
      (
            SELECT st_storekey AS id, st_name AS name
            FROM store, drink
            WHERE d_type = "tea" AND d_storekey = st_storekey
      ) as q
       WHERE d_storekey = q.id AND
             s_storekey = q.id AND
             t_storekey = q.id
      GROUP BY q.id;
'''
#7-- 7) Find the customer(s) who ordered from pizza hut and asked for a pizza with thin crust
List_Customers_OrderedThin = '''
    SELECT c_name
    FROM Customer,
         Orders,
         store,
         entree
    WHERE c_key = o_custkey AND
          o_orderkey = st_orderkey AND
          st_name = "Pizza Hut" AND
          o_entree = e_key AND
          e_ingredients LIKE "%Thin Cust%";
 '''
Find_Most_Ordered_Combination = '''
SELECT
       info.Entree,
       info.Side,
       info.Drink,
       max(info.[key])
  FROM (
           SELECT count( * ) AS [Key],
                  Q1.e_key AS Entree,
                  Q1.d_key AS Drink,
                  Q1.s_key AS Side,
                  Q1.[Key] AS Store
             FROM Combinations Q1
            GROUP BY Entree,
                     Side,
                     Drink,
                     Store
            ORDER BY Store ASC
       )
       AS info
 WHERE info.Store = ?;
 '''
Customer_List = '''
 SELECT  c_name 
 FROM Customer, Orders
 WHERE c_key = o_custkey AND
       o_store = ?  '''

store_VIP = '''
SELECT c_name,
       max(info.cnt) 
  FROM (
           SELECT c_name,
                  count( * ) AS cnt,
                  o_store
             FROM Orders,
                  Customer
            WHERE o_custkey = c_key
            GROUP BY c_key,
                     o_store
       )
       AS info
 WHERE info.o_store = ?;
'''
myDrivers = '''
SELECT Driver_name,
       o_store
  FROM Orders,
       Delivery
 WHERE o_orderkey = order_id AND 
       o_store = ?;
 '''

Mvp = '''
     ___  ___   _     _   _____  
    /   |/   | | |   / / |  _  \ 
   / /|   /| | | |  / /  | |_| | 
  / / |__/ | | | | / /   |  ___/ 
 / /       | | | |/ /    | |     
/_/        |_| |___/     |_|     
'''
Login = '''
 _       _____   _____   _   __   _  
| |     /  _  \ /  ___| | | |  \ | | 
| |     | | | | | |     | | |   \| | 
| |     | | | | | |  _  | | | |\   | 
| |___  | |_| | | |_| | | | | | \  | 
|_____| \_____/ \_____/ |_| |_|  \_|  '''

ByeBye = '''
 _____   _____   _____   _____        _____  __    __  _____  
/  ___| /  _  \ /  _  \ |  _  \      |  _  \ \ \  / / | ____| 
| |     | | | | | | | | | | | |      | |_| |  \ \/ /  | |__   
| |  _  | | | | | | | | | | | |      |  _  |   \  /   |  __|  
| |_| | | |_| | | |_| | | |_| |      | |_| |   / /    | |___  
\_____/ \_____/ \_____/ |_____/      |_____/  /_/     |_____| 
'''
Mvps_favoriteOrder = '''
SELECT Q1.c_name,
       Q1.e_name,
       Q1.s_name,
       Q1.d_brand,
       Q1.st_name
  FROM PlacedOrders Q1,
       getMVPS Q2,
       store M
 WHERE Q1.c_name = Q2.c_name AND 
       Q2.store = M.st_storekey AND 
       M.st_name = Q1.st_name
       GROUP BY Q1.st_name AND 
       M.st_storekey = ? AND 
       Q1.c_name = ?;
'''

# SELECT e_key,
#        s_key,
#        d_key,
#        d_storekey as KEY
#    FROM entree, sides, drink, Orders
#    WHERE e_storekey = s_storekey AND
#          d_storekey = e_storekey AND
#          o_store = d_storekey AND 
#          o_entree = e_key AND
#          o_drink = d_key AND
#          o_side = s_key
#      GROUP by KEY , o_orderkey
# SELECT DISTINCT c_name,
#        max(info.cnt),
#        info.c_key,
#        info.o_store
#   FROM (
#            SELECT c_name,
#                   count( * ) AS cnt,
#                   o_store, 
#                   c_key
#              FROM Orders,
#                   Customer
#             WHERE o_custkey = c_key
#             GROUP BY c_key,
#                      o_store
#        )
#        AS info
# GROUP By info.o_store