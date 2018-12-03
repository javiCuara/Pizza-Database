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
Insert_intoDrink = '''
INSERT INTO drink (
                      d_type,
                      d_key,
                      d_stock,
                      d_brand,
                      d_storekey
                  )
                  VALUES (
                      ?,
                      ?,
                      ?,
                      ?,
                      ?
                  );

'''
Insert_intoEntree = '''
INSERT INTO entree (
                       e_name,
                       e_storekey,
                       e_stock,
                       e_key,
                       e_ingredients
                   )
                   VALUES (
                       ?,
                       ?,
                       ?,
                       ?,
                       ?
                   );

'''
Insert_intoSauce = '''
INSERT INTO sauce (
                      sc_name,
                      sc_key,
                      sc_offeredBy,
                      sc_stock
                  )
                  VALUES (
                      ?,
                      ?,
                      ?,
                      ?
                  );

'''
Insert_intoSides = '''
INSERT INTO sides (
                      s_name,
                      s_stock,
                      s_storekey,
                      s_key
                  )
                  VALUES (
                      ?,
                      ?,
                      ?,
                      ?
                  );

'''
Insert_intoToppings = '''
INSERT INTO toppings (
                         t_name,
                         t_key,
                         t_storekey,
                         t_stock
                     )
                     VALUES (
                         ?,
                         ?,
                         ?,
                         ?
                      );

'''
Delete_FromToppings = '''
DELETE FROM toppings
      WHERE t_name = ? AND
            t_key = ? AND
            t_storekey = ? AND
            t_stock = ?;

'''
Delete_FromEntree = '''
DELETE FROM entree
      WHERE e_name = ? AND
            e_storekey = ? AND
            e_stock = ? AND
            e_key = ? AND
            e_ingredients = ?;

'''
Delete_FromSides = '''
DELETE FROM sides
      WHERE s_name = ? AND
            s_stock = ? AND
            s_storekey = ? AND
            s_key = ?;

'''
Delete_FromSauce = '''
DELETE FROM sauce
      WHERE sc_name = ? AND
            sc_key = ? AND
            sc_offeredBy = ? AND
            sc_stock = ?;

'''
Delete_FromDrinks = '''
DELETE FROM drink
      WHERE d_type = ? AND
            d_key = ? AND
            d_stock = ? AND
            d_brand = ? AND
            d_storekey = ?;

'''
getEntree_key = '''
SELECT e_key
  FROM entree
  WHERE e_storekey = ?;

'''
getDrink_key = '''
SELECT d_key
  FROM drink
  WHERE d_storekey = ?;
'''
getSide_key = '''
SELECT s_key
  FROM sides
  WHERE s_storekey = ?;
'''
getSauce_key = '''
SELECT sc_key
  FROM sauce
  WHERE sc_offeredBy = ?;
'''
getToppint_key = '''
SELECT t_key
  FROM toppings
  WHERE t_storekey = ?
'''

getMaxEntree_key = '''
SELECT max(e_key)
  FROM entree
  WHERE e_storekey = ?;

'''
getMaxDrink_key = '''
SELECT max(d_key)
  FROM drink
  WHERE d_storekey = ?;
'''
getMaxSide_key = '''
SELECT max(s_key)
  FROM sides
  WHERE s_storekey = ?;
'''
getMaxSauce_key = '''
SELECT max(sc_key)
  FROM sauce
  WHERE sc_offeredBy = ?;
'''
getMaxToppint_key = '''
SELECT max(t_key)
  FROM toppings
  WHERE t_storekey = ?
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
 SELECT  DISTINCT c_name
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
receiptForXYZ = '''
SELECT Q1.c_name,
       Q1.e_name,
       Q1.s_name,
       Q1.d_brand,
       Q1.st_name
  FROM PlacedOrders Q1
 WHERE Q1.c_name = ? AND Q1.st_name = ?


'''



hello ='''
____    __    ____  _______  __        ______   ______   .___  ___.  _______
\   \  /  \  /   / |   ____||  |      /      | /  __  \  |   \/   | |   ____|
 \   \/    \/   /  |  |__   |  |     |  ,----'|  |  |  | |  \  /  | |  |__
  \            /   |   __|  |  |     |  |     |  |  |  | |  |\/|  | |   __|
   \    /\    /    |  |____ |  `----.|  `----.|  `--'  | |  |  |  | |  |____
    \__/  \__/     |_______||_______| \______| \______/  |__|  |__| |_______|
'''
To = '''
.___________.  ______
|           | /  __  \
`---|  |----`|  |  |  |
    |  |     |  |  |  |
    |  |     |  `--'  |
    |__|      \______/
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
 __        ______     _______  __  .__   __.
|  |      /  __  \   /  _____||  | |  \ |  |  _
|  |     |  |  |  | |  |  __  |  | |   \|  | (_)
|  |     |  |  |  | |  | |_ | |  | |  . `  |
|  `----.|  `--'  | |  |__| | |  | |  |\   |  _
|_______| \______/   \______| |__| |__| \__| (_)
                                                '''

Updating = '''
 __    __  .______    _______       ___   .___________. __  .__   __.   _______
|  |  |  | |   _  \  |       \     /   \  |           ||  | |  \ |  |  /  _____|
|  |  |  | |  |_)  | |  .--.  |   /  ^  \ `---|  |----`|  | |   \|  | |  |  __
|  |  |  | |   ___/  |  |  |  |  /  /_\  \    |  |     |  | |  . `  | |  | |_ |
|  `--'  | |  |      |  '--'  | /  _____  \   |  |     |  | |  |\   | |  |__| |     __     __     __
 \______/  | _|      |_______/ /__/     \__\  |__|     |__| |__| \__|  \______|    (__)   (__)   (__)
'''
success = '''
     _______. __    __    ______   ______  _______     _______.     _______.    __
    /       ||  |  |  |  /      | /      ||   ____|   /       |    /       |   |  |
   |   (----`|  |  |  | |  ,----'|  ,----'|  |__     |   (----`   |   (----`   |  |
    \   \    |  |  |  | |  |     |  |     |   __|     \   \        \   \       |  |
.----)   |   |  `--'  | |  `----.|  `----.|  |____.----)   |   .----)   |      |__|
|_______/     \______/   \______| \______||_______|_______/    |_______/       (__)
'''
ByeBye = '''
  _______   ______     ______    _______     .______   ____    ____  _______
 /  _____| /  __  \   /  __  \  |       \    |   _  \  \   \  /   / |   ____|
|  |  __  |  |  |  | |  |  |  | |  .--.  |   |  |_)  |  \   \/   /  |  |__
|  | |_ | |  |  |  | |  |  |  | |  |  |  |   |   _  <    \_    _/   |   __|
|  |__| | |  `--'  | |  `--'  | |  '--'  |   |  |_)  |     |  |     |  |____
 \______|  \______/   \______/  |_______/    |______/      |__|     |_______|
'''
TryAgain = '''
 .___________..______     ____    ____         ___       _______      ___       __  .__   __.
|           ||   _  \    \   \  /   /        /   \     /  _____|    /   \     |  | |  \ |  |
`---|  |----`|  |_)  |    \   \/   /        /  ^  \   |  |  __     /  ^  \    |  | |   \|  |
    |  |     |      /      \_    _/        /  /_\  \  |  | |_ |   /  /_\  \   |  | |  . `  |
    |  |     |  |\  \----.   |  |         /  _____  \ |  |__| |  /  _____  \  |  | |  |\   |
    |__|     | _| `._____|   |__|        /__/     \__\ \______| /__/     \__\ |__| |__| \__|
'''
Welcome_Manager = '''
____    __    ____  _______  __        ______   ______   .___  ___.  _______       .___  ___.      ___      .__   __.      ___       _______  _______ .______
\   \  /  \  /   / |   ____||  |      /      | /  __  \  |   \/   | |   ____|      |   \/   |     /   \     |  \ |  |     /   \     /  _____||   ____||   _  \
 \   \/    \/   /  |  |__   |  |     |  ,----'|  |  |  | |  \  /  | |  |__         |  \  /  |    /  ^  \    |   \|  |    /  ^  \   |  |  __  |  |__   |  |_)  |
  \            /   |   __|  |  |     |  |     |  |  |  | |  |\/|  | |   __|        |  |\/|  |   /  /_\  \   |  . `  |   /  /_\  \  |  | |_ | |   __|  |      /
   \    /\    /    |  |____ |  `----.|  `----.|  `--'  | |  |  |  | |  |____       |  |  |  |  /  _____  \  |  |\   |  /  _____  \ |  |__| | |  |____ |  |\  \----.
    \__/  \__/     |_______||_______| \______| \______/  |__|  |__| |_______|      |__|  |__| /__/     \__\ |__| \__| /__/     \__\ \______| |_______|| _| `._____|
'''
Manager_name = '''
 .___  ___.      ___      .__   __.      ___       _______  _______ .______
|   \/   |     /   \     |  \ |  |     /   \     /  _____||   ____||   _  \
|  \  /  |    /  ^  \    |   \|  |    /  ^  \   |  |  __  |  |__   |  |_)  |
|  |\/|  |   /  /_\  \   |  . `  |   /  /_\  \  |  | |_ | |   __|  |      /
|  |  |  |  /  _____  \  |  |\   |  /  _____  \ |  |__| | |  |____ |  |\  \----.
|__|  |__| /__/     \__\ |__| \__| /__/     \__\ \______| |_______|| _| `._____|

'''
Dominos = '''
 _______   ______   .___  ___.  __  .__   __.   ______    __     _______.
|       \ /  __  \  |   \/   | |  | |  \ |  |  /  __  \  (_ )   /       |
|  .--.  |  |  |  | |  \  /  | |  | |   \|  | |  |  |  |  |/   |   (----`
|  |  |  |  |  |  | |  |\/|  | |  | |  . `  | |  |  |  |        \   \
|  '--'  |  `--'  | |  |  |  | |  | |  |\   | |  `--'  |    .----)   |
|_______/ \______/  |__|  |__| |__| |__| \__|  \______/     |_______/

        _______.___________.  ______   .______       _______
       /       |           | /  __  \  |   _  \     |   ____|
      |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
       \   \       |  |     |  |  |  | |      /     |   __|
   .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
   |_______/       |__|      \______/  | _| `._____||_______|
 '''
LittleOven = '''
  __       __  .___________.___________. __       _______         ______   ____    ____  _______ .__   __.
|  |     |  | |           |           ||  |     |   ____|       /  __  \  \   \  /   / |   ____||  \ |  |
|  |     |  | `---|  |----`---|  |----`|  |     |  |__         |  |  |  |  \   \/   /  |  |__   |   \|  |
|  |     |  |     |  |        |  |     |  |     |   __|        |  |  |  |   \      /   |   __|  |  . `  |
|  `----.|  |     |  |        |  |     |  `----.|  |____       |  `--'  |    \    /    |  |____ |  |\   |
|_______||__|     |__|        |__|     |_______||_______|       \______/      \__/     |_______||__| \__|

                           .______    __   ________   ________      ___
                           |   _  \  |  | |       /  |       /     /   \
                           |  |_)  | |  | `---/  /   `---/  /     /  ^  \
                           |   ___/  |  |    /  /       /  /     /  /_\  \
                           |  |      |  |   /  /----.  /  /----./  _____  \
                           | _|      |__|  /________| /________/__/     \__\
'''
Mountain = '''
.___  ___.   ______    __    __  .__   __. .___________.    ___       __  .__   __.       .___  ___.  __   __  ___  _______ __     _______.
|   \/   |  /  __  \  |  |  |  | |  \ |  | |           |   /   \     |  | |  \ |  |       |   \/   | |  | |  |/  / |   ____(_ )   /       |
|  \  /  | |  |  |  | |  |  |  | |   \|  | `---|  |----`  /  ^  \    |  | |   \|  |       |  \  /  | |  | |  '  /  |  |__   |/   |   (----`
|  |\/|  | |  |  |  | |  |  |  | |  . `  |     |  |      /  /_\  \   |  | |  . `  |       |  |\/|  | |  | |    <   |   __|        \   \
|  |  |  | |  `--'  | |  `--'  | |  |\   |     |  |     /  _____  \  |  | |  |\   |       |  |  |  | |  | |  .  \  |  |____   .----)   |
|__|  |__|  \______/   \______/  |__| \__|     |__|    /__/     \__\ |__| |__| \__|       |__|  |__| |__| |__|\__\ |_______|  |_______/

            .______    __   ________   ________      ___                 _______.___________.  ______   .______       _______
            |   _  \  |  | |       /  |       /     /   \               /       |           | /  __  \  |   _  \     |   ____|
            |  |_)  | |  | `---/  /   `---/  /     /  ^  \             |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
            |   ___/  |  |    /  /       /  /     /  /_\  \             \   \       |  |     |  |  |  | |      /     |   __|
            |  |      |  |   /  /----.  /  /----./  _____  \        .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
            | _|      |__|  /________| /________/__/     \__\       |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaFactory = '''
.______    __   ________   ________      ___          _______    ___       ______ .___________.  ______   .______     ____    ____
|   _  \  |  | |       /  |       /     /   \        |   ____|  /   \     /      ||           | /  __  \  |   _  \    \   \  /   /
|  |_)  | |  | `---/  /   `---/  /     /  ^  \       |  |__    /  ^  \   |  ,----'`---|  |----`|  |  |  | |  |_)  |    \   \/   /
|   ___/  |  |    /  /       /  /     /  /_\  \      |   __|  /  /_\  \  |  |         |  |     |  |  |  | |      /      \_    _/
|  |      |  |   /  /----.  /  /----./  _____  \     |  |    /  _____  \ |  `----.    |  |     |  `--'  | |  |\  \----.   |  |
| _|      |__|  /________| /________/__/     \__\    |__|   /__/     \__\ \______|    |__|      \______/  | _| `._____|   |__|

                                         _______.___________.  ______   .______       _______
                                        /       |           | /  __  \  |   _  \     |   ____|
                                       |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                                        \   \       |  |     |  |  |  | |      /     |   __|
                                    .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
                                    |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaGuys = '''
.______    __   ________   ________      ___           _______  __    __  ____    ____  _______.
|   _  \  |  | |       /  |       /     /   \         /  _____||  |  |  | \   \  /   / /       |
|  |_)  | |  | `---/  /   `---/  /     /  ^  \       |  |  __  |  |  |  |  \   \/   / |   (----`
|   ___/  |  |    /  /       /  /     /  /_\  \      |  | |_ | |  |  |  |   \_    _/   \   \
|  |      |  |   /  /----.  /  /----./  _____  \     |  |__| | |  `--'  |     |  | .----)   |
| _|      |__|  /________| /________/__/     \__\     \______|  \______/      |__| |_______/

                    _______.___________.  ______   .______       _______
                   /       |           | /  __  \  |   _  \     |   ____|
                  |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                   \   \       |  |     |  |  |  | |      /     |   __|
               .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
               |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaHut = '''
.______    __   ________   ________      ___             __    __   __    __  .___________.
|   _  \  |  | |       /  |       /     /   \           |  |  |  | |  |  |  | |           |
|  |_)  | |  | `---/  /   `---/  /     /  ^  \          |  |__|  | |  |  |  | `---|  |----`
|   ___/  |  |    /  /       /  /     /  /_\  \         |   __   | |  |  |  |     |  |
|  |      |  |   /  /----.  /  /----./  _____  \        |  |  |  | |  `--'  |     |  |
| _|      |__|  /________| /________/__/     \__\       |__|  |__|  \______/      |__|

                 _______.___________.  ______   .______       _______
                /       |           | /  __  \  |   _  \     |   ____|
               |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                \   \       |  |     |  |  |  | |      /     |   __|
            .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
            |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaLoca = '''
.______    __   ________   ________      ___             __        ______     ______     ___
|   _  \  |  | |       /  |       /     /   \           |  |      /  __  \   /      |   /   \
|  |_)  | |  | `---/  /   `---/  /     /  ^  \          |  |     |  |  |  | |  ,----'  /  ^  \
|   ___/  |  |    /  /       /  /     /  /_\  \         |  |     |  |  |  | |  |      /  /_\  \
|  |      |  |   /  /----.  /  /----./  _____  \        |  `----.|  `--'  | |  `----./  _____  \
| _|      |__|  /________| /________/__/     \__\       |_______| \______/   \______/__/     \__\

                    _______.___________.  ______   .______       _______
                   /       |           | /  __  \  |   _  \     |   ____|
                  |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                   \   \       |  |     |  |  |  | |      /     |   __|
               .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
               |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaPalace = '''
.______    __   ________   ________      ___            .______      ___       __          ___       ______  _______
|   _  \  |  | |       /  |       /     /   \           |   _  \    /   \     |  |        /   \     /      ||   ____|
|  |_)  | |  | `---/  /   `---/  /     /  ^  \          |  |_)  |  /  ^  \    |  |       /  ^  \   |  ,----'|  |__
|   ___/  |  |    /  /       /  /     /  /_\  \         |   ___/  /  /_\  \   |  |      /  /_\  \  |  |     |   __|
|  |      |  |   /  /----.  /  /----./  _____  \        |  |     /  _____  \  |  `----./  _____  \ |  `----.|  |____
| _|      |__|  /________| /________/__/     \__\       | _|    /__/     \__\ |_______/__/     \__\ \______||_______|

                             _______.___________.  ______   .______       _______
                            /       |           | /  __  \  |   _  \     |   ____|
                           |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                            \   \       |  |     |  |  |  | |      /     |   __|
                        .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
                        |_______/       |__|      \______/  | _| `._____||_______|
'''
PizzaVilla = '''
.______    __   ________   ________      ___            ____    ____  __   __       __          ___
|   _  \  |  | |       /  |       /     /   \           \   \  /   / |  | |  |     |  |        /   \
|  |_)  | |  | `---/  /   `---/  /     /  ^  \           \   \/   /  |  | |  |     |  |       /  ^  \
|   ___/  |  |    /  /       /  /     /  /_\  \           \      /   |  | |  |     |  |      /  /_\  \
|  |      |  |   /  /----.  /  /----./  _____  \           \    /    |  | |  `----.|  `----./  _____  \
| _|      |__|  /________| /________/__/     \__\           \__/     |__| |_______||_______/__/     \__\

                    _______.___________.  ______   .______       _______
                   /       |           | /  __  \  |   _  \     |   ____|
                  |   (----`---|  |----`|  |  |  | |  |_)  |    |  |__
                   \   \       |  |     |  |  |  | |      /     |   __|
               .----)   |      |  |     |  `--'  | |  |\  \----.|  |____
               |_______/       |__|      \______/  | _| `._____||_______|
'''
Welcome = '''
____    __    ____  _______  __        ______   ______   .___  ___.  _______    .___________.  ______
\   \  /  \  /   / |   ____||  |      /      | /  __  \  |   \/   | |   ____|   |           | /  __  \
 \   \/    \/   /  |  |__   |  |     |  ,----'|  |  |  | |  \  /  | |  |__      `---|  |----`|  |  |  |
  \            /   |   __|  |  |     |  |     |  |  |  | |  |\/|  | |   __|         |  |     |  |  |  |
   \    /\    /    |  |____ |  `----.|  `----.|  `--'  | |  |  |  | |  |____        |  |     |  `--'  |
    \__/  \__/     |_______||_______| \______| \______/  |__|  |__| |_______|       |__|      \______/

      .______    __   ________   ________      ___         .___________. __  .___  ___.  _______
      |   _  \  |  | |       /  |       /     /   \        |           ||  | |   \/   | |   ____|
      |  |_)  | |  | `---/  /   `---/  /     /  ^  \       `---|  |----`|  | |  \  /  | |  |__
      |   ___/  |  |    /  /       /  /     /  /_\  \          |  |     |  | |  |\/|  | |   __|
      |  |      |  |   /  /----.  /  /----./  _____  \         |  |     |  | |  |  |  | |  |____
      | _|      |__|  /________| /________/__/     \__\        |__|     |__| |__|  |__| |_______|

 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|
'''
pizzaIcon = '''
                     ..........,,,,,,,,,,,,,,,,,,,,,*,,,,,,,,,,*,**,**,,,,.   
                      .,...,...,,.,.,.,,.....,,,....,.,,//,.,.....,###,,,,,.
                        *,,,*,,./#(((#(/.,,,.,*,,.,,,/####(#*,,,,.,##(,,,,,.
                         /*,*,.(#(######*.,.,***..,,*########.**,,,###/,,,,.
                          /**,.(###(####,,.,***.,.,.,#######(,,*./####/,,,,.
                           ./*,,*####(*.,.,,,.,,....,,/#(#(,,,*/*####(,**,*
                             /*,,,,,,,,,..,,..........,...,..,,,(###(,,,,,,
                              */,,,/,.,,,,......,(((##(((..,...,####*,,,*,
                                //*,,,,/##(,...,((#####(##,....,####*,,,,*
                                 */*,,/####(,.,,(##(#####(,.,,,/####*,,**.
                                  */*,,####(.,,./(##(###(,,,,*####(*,,***
                                    /*,,,,,,,*,,,,/####*,,,,####(,,,****
                                     **,,,*****,.......,.,,,%##*,,*****.
                                      ./*,///*,,.,,,,.,,,,,,%##*******
                                        *,,,,,,,,***,,*,,,,(%#%/*****
                                         .*,,,,///,*,(/,,#%%%#******
                                           **,,,,,,,*((#%%%/******
                                             **,,,,,,/%%%%******.
                                              ***,,,#%%(/*****.
                                                **%%%%******
                                                 **(******
                                                  ,****.
'''
divider = '''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|
'''
