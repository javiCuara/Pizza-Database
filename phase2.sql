-- 1) Count how many orders for pasta have been placed for stores that can deliver to Jordan J. Kirby
    SELECT COUNT(*) FROM entree, Orders, store, Delivery, Customer WHERE c_key = o_custkey AND o_orderkey = st_orderkey AND st_orderkey = order_id AND c_name = "Jordan J. Kirby" AND e_name = "pasta";

-- 2) for each store that carries beer, count how many delivery orders have been made
    SELECT COUNT(DISTINCT order_id) FROM drink, Orders, store, Delivery WHERE order_id = o_orderkey AND d_type = "beer" AND o_drink = d_key GROUP BY st_storeID;

-- 3) Count how many ordered pizzas that have mushrooms are in each type of pizza at Pizza Factory
    SELECT COUNT(*) FROM store, Orders, entree, toppings WHERE st_orderkey = o_orderkey AND o_entree = e_key AND e_name LIKE "pizza" AND st_name = "Pizza Factory";

-- 4) For each customer, which drink is most ordered

-- 5) For each customer that Dominos delivers to, find their order (entree, drink, side)
    SELECT e_name, d_name, s_name FROM entree, side, drink, Orders, store, Delivery WHERE order_id = st_orderkey AND st_orderkey = o_orderkey AND o_custkey = c_custkey AND o_drink = d_key AND o_entree = e_key AND o_side = s_key AND st_name = "Dominos" GROUP BY c_name;

-- 6) Take the inventory of each side, entree ingredient, and drink for each store that offers tea
    SELECT COUNT(d_stock), COUNT(s_stock), COUNT(t_stock), COUNT(cr_stock), COUNT(sc_stock) FROM drinks, sides, toppings, (SELECT st_storeID AS id FROM store, drink WHERE d_type = "tea" AND d_storekey = st_storeID) as q WHERE d_storekey = q.id AND s_storekey = q.id AND t_storekey = q.id GROUP BY q.id;

-- 7) Find the customer(s) who orderd from pizza hut and asked for a pizza with thin crust
    SELECT c_name FROM Customer, Orders, store, entree, crust WHERE c_custkey = o_orderkey AND o_orderkey = st_orderkey AND st_name = "Pizza Hut" AND o_entree = e_key AND e_ingredients LIKE "thin crust";

-- 8) List the stores that carry more than 2 types of drinks
    SELECT st_name FROM (SELECT COUNT(DISTINCT d_type) AS numdrinks FROM drink, store WHERE st_storeID = d_storekey) AS q, store GROUP BY st_name HAVING q.numdrinks > 2;
