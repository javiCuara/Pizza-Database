-- 1) Count how many stores that sell Wings Deliver as well 
     SELECT COUNT( DISTINCT st_name )  FROM sides, store, Orders WHERE s_storekey = st_storekey AND s_name LIKE "%Wings%" AND st_orderkey = o_orderkey AND o_dev = 1;

-- 2) for each store that carries beer, count how many delivery orders have been made
    SELECT COUNT(DISTINCT order_id) FROM drink, Orders, store, Delivery WHERE order_id = o_orderkey AND d_type = "beer" AND o_drink = d_key GROUP BY st_storekey;

-- 3) Count how many ordered pizzas that have mushrooms are in each type of pizza at Pizza Factory
    SELECT COUNT(*) FROM store, Orders, entree, toppings WHERE st_orderkey = o_orderkey AND o_entree = e_key AND e_ingredients LIKE "%Mushroom%" AND st_name = "Pizza Factory";

-- 4) For each store, which drink is least ordered (which has the most stock)
    SELECT st_name, d_brand FROM store, drink WHERE d_storekey = st_storekey GROUP BY st_name HAVING MAX(d_stock);

-- 5) For each customer that Dominos delivers to, find their order (entree, drink, side)
    SELECT e_name, d_brand, s_name FROM Customer, entree, sides, drink, Orders, store, Delivery WHERE order_id = st_orderkey AND st_orderkey = o_orderkey AND o_custkey = c_key AND o_drink = d_key AND o_entree = e_key AND o_side = s_key AND st_name = "Dominos" GROUP BY c_name;

-- 6) Take the inventory of each side, entree ingredient, and drink for each store that offers tea
    SELECT q.name, COUNT(d_stock), COUNT(s_stock), COUNT(t_stock) FROM drink, sides, toppings, (SELECT st_storekey AS id, st_name AS name FROM store, drink WHERE d_type = "tea" AND d_storekey = st_storekey) as q WHERE d_storekey = q.id AND s_storekey = q.id AND t_storekey = q.id GROUP BY q.id;

-- 7) Find the customer(s) who ordered from pizza hut and asked for a pizza with thin crust
    SELECT c_name FROM Customer, Orders, store, entree WHERE c_key = o_custkey AND o_orderkey = st_orderkey AND st_name = "Pizza Hut" AND o_entree = e_key AND e_ingredients LIKE "%Thin Cust%";

-- 8) List the stores that carry more than 2 types of drinks
    SELECT st_name FROM (SELECT COUNT(DISTINCT d_type) AS numdrinks FROM drink, store WHERE st_storekey = d_storekey) AS q, store GROUP BY st_name HAVING q.numdrinks > 2;

-- 9) Delete any orders by Suki Sheppard
    DELETE FROM Customer WHERE c_name = "Suki Sheppard";

-- 10) Insert a new drink "Cactus Cooler" into the drink table, where Pizza palace (key# 4) is the only place to sell it
    INSERT INTO drink VALUES ("soda", 10, 20, "Cactus Cooler", 4);

-- 11) Pizza Villa has started to sell Cactus Cooler and Pizza Palace has dropped it. Update the table to reflect this change
    UPDATE drink SET d_storekey = 7 WHERE d_brand = "Cactus Cooler";

-- 12) Find the topping with the least stock for each store
    SELECT st_name, t_name FROM toppings, store WHERE t_storekey = st_storekey GROUP BY st_name HAVING MIN(t_stock);

-- 13) List all stores that sell beer and wings
    SELECT st_name FROM store, drink, sides WHERE st_storekey = d_storekey AND s_storekey = st_storekey AND d_type = 'beer' AND s_name LIKE '%Wings%' GROUP BY st_name;

-- 14) List stores that sell more than 2 drinks, with top pizza
    SELECT st_name, e_name, count(DISTINCT o_orderkey) FROM drink, Orders, entree, store,(SELECT count(d_type) AS ct, d_storekey AS [key] FROM drink GROUP BY d_storekey) AS info
 WHERE d_storekey = o_store AND 
       e_storekey = o_store AND 
       d_storekey = info.[key] AND 
       info.ct > 2 AND 
       o_store = st_storekey
 GROUP BY o_store;

-- 15) Which store did the most deliveries
	SELECT st_name
FROM store, Orders,
    (SELECT max(DISTINCT o_orderkey) as ct, o_store as key
     FROM Orders 
     WHERE o_dec = 1) as info
WHERE st_storekey = o_store AND st_storekey = info.key

-- 16) List Sides ordered by customers whos names start with 
    SELECT DISTINCT s_name
FROM Orders, Customer, sides
WHERE c_name Like 'D%' AND
      c_key = o_custkey AND 
      o_side = s_key
      
-- 17) What stores sell Hawaiian pizza and list the ingredients
	SELECT st_name, e_ingredients FROM store, entree WHERE st_storekey = e_storekey AND e_name = "Hawaiian" GROUP BY st_name;

-- 18) Find entre that contains ingredient
    SELECT e_name FROM entree WHERE e_ingredients Like '%Pineapple%'
    
-- 19) List each customer that has ordered a Pepsi with wings
	SELECT DISTINCT c_name
	FROM Customer, Orders, drink, sides
	WHERE c_key = o_custkey AND o_drink = d_key AND o_side = s_key AND d_brand = "Pepsi" AND s_name LIKE "%Wings%";

-- 20)
