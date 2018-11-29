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
# ManagerMenu = '''
# 0: Return to main menu
# 1:
# 2:
# 3:
# '''
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
#8

#9

#10


#11


#12
