from economy_collection import economy
from economy_collection import crafting

import unittest


class TestEconomy(unittest.TestCase):
    def test_trade(self):

        T1 = economy.Transaction(-2, "wood", 10, "gold", -5)
        T2 = economy.Transaction(-1, "wood", -10, "gold", 6)

        transactions = [T1, T2]

        p = economy.calculate_profit_from_trades(transactions)
        
        assert p =={'wood': {'amount': 0, 'profit': 1}}

    def test_define_tradegood(self):
        economy.Tradegood("wood")

    def test_market_health(self):
        TG = economy.Tradegood
        w = TG("water")
        # shortage
        w.desired_sell = 200
        w.desired_buy = 200
        w.sell_order_volume = 1
        w.buy_order_volume = 1000
        w.average_sell = 5

        w.weekly_sell_volume = 100
        w.weekly_buy_volume = 100

        # sell_order_volume > good.weekly_sell_volume:
        i = TG("iron")
        i.desired_sell = 15
        i.desired_buy = 5
        i.average_sell = 100
        i.sell_order_volume = 10
        i.buy_order_volume = 1
        i.weekly_sell_volume = 5
        i.weekly_buy_volume = 5

        b = TG("bread")
        m = TG("milk")
        goods = {w.name: w, i.name: i, b.name: b}
        request_table = [w.name, i.name, b.name, m.name]
        result_table = economy.market_health_check(goods, request_table)
        
        assert result_table == {'water': {'sell volume': 0.01, 'buy volume': 1, 'sell state': 'undervalued', 'buy state': 'undervalued'}, 'iron': {'sell volume': 1, 'buy volume': 0.2, 'sell state': 'overpriced', 'buy state': 'undervalued'}, 'bread': {'sell state': 'not sold', 'buy state': 'not bought'}}
    
    def test_find_cheapest_seller(self):
        
        
        MyAgent = economy.EconomyAgent()
        
        
        TG = economy.Tradegood
        water = TG("Water")
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":20}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":20}})
        MySeller3 = economy.EconomyAgent({"Water":{"amount":20}})
        # default position is (0,0,0)
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((1,0,0),)
        M2 = economy.Market((5,0,0),)
        M3 = economy.Market((4,3,0),)
        
        O1=economy.Order(water.name,price=5,amount=10,creator=MySeller1,sell=True)
        M1.put_order(O1,MySeller1,sell=True)
        
        O2=economy.Order(water.name,price=1,amount=10,creator=MySeller2,sell=True)
        M2.put_order(O2,MySeller2,sell=True)
        
        O3=economy.Order(water.name,price=3,amount=10,creator=MySeller3,sell=True)
        M3.put_order(O3,MySeller3,sell=True)
        
        E.locations[M1.id] = M1
        E.locations[M2.id] = M2
        E.locations[M3.id] = M3
        
        MyAgent.ensure_d_list(E)
        
        r = MyAgent.find_closest_market()
        
        
        #I'm expecting some reasonable output here.
        assert r == M1
        r = MyAgent.find_cheapest_seller(E,water.name)
        
        assert r[0].location == M2
        
        
        MyAgent.pos = (6,0,0)
        
        MyAgent.ensure_d_list(E)
        r = MyAgent.find_closest_market()
        
        
        #I'm expecting some reasonable output here.
        assert r == M2
        
        # arguably, this isn't finding the cheapest seller right now.
        r = MyAgent.find_cheapest_seller(E,water.name)
        assert r[0].location == M2
    
    
    def test_get_manufacturing_price_points_basic(self):
        
        
        MyAgent = economy.EconomyAgent()
        
        materials, products, recipes = crafting.default()
        
        good_recipe = recipes["Bread"]
        
        
        TG = economy.Tradegood
        water = TG("Water")
        wheat = TG("Grain")
        bread = TG("Bread")
        goods = {water.name: water, wheat.name: wheat, bread.name: bread}
        request_table = [water.name, wheat.name, bread.name]
        #result_table = economy.market_health_check(goods, request_table)
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller3 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20},"Bread":{"amount":10}})
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((1,0,0),)
        M2 = economy.Market((5,0,0),)
        M3 = economy.Market((4,3,0),)
        
        O11 = economy.Order(water.name,price=5,amount=10,creator=MySeller1,sell=True)
        O12 = economy.Order(wheat.name,price=5,amount=10,creator=MySeller1,sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        
        O21 = economy.Order(water.name,price=1,amount=10,creator=MySeller2,sell=True)
        O22 = economy.Order(wheat.name,price=1,amount=10,creator=MySeller2,sell=True)
        M2.put_order(O21,MySeller2,sell=True)
        M2.put_order(O22,MySeller2,sell=True)
        
        O31 = economy.Order(water.name,price=3,amount=10,creator=MySeller3,sell=True)
        O32 = economy.Order(wheat.name,price=3,amount=10,creator=MySeller3,sell=True)
        O33 = economy.Order(bread.name,price=3,amount=10,creator=MySeller3,sell=True)
        M3.put_order(O31,MySeller3,sell=True)
        M3.put_order(O32,MySeller3,sell=True)
        M3.put_order(O33,MySeller3,sell=True)
        
        E.locations[M1.id] = M1
        E.locations[M2.id] = M2
        E.locations[M3.id] = M3
        
        amount = 25
        
        price_point_breaks, relevant_orders, requirements_cost  = MyAgent.get_coverage_relevant_orders(E, good_recipe, amount)
        mpps = MyAgent.get_manufacturing_price_points( relevant_orders, price_point_breaks, good_recipe, amount)
        
        assert mpps[0].amount == 10
        assert mpps[0].price == 2
        assert mpps[1].amount == 10
        assert mpps[1].price == 6
        assert mpps[2].amount == 5
        assert mpps[2].price == 10
    
    
    
    def test_get_manufacturing_price_points_insufficient_orders(self):
        
        
        MyAgent = economy.EconomyAgent()
        
        materials, products, recipes = crafting.default()
        
        good_recipe = recipes["Bread"]
        
        
        TG = economy.Tradegood
        water = TG("Water")
        wheat = TG("Grain")
        bread = TG("Bread")
        goods = {water.name: water, wheat.name: wheat, bread.name: bread}
        request_table = [water.name, wheat.name, bread.name]
        #result_table = economy.market_health_check(goods, request_table)
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller3 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20},"Bread":{"amount":10}})
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((1,0,0),)
        M2 = economy.Market((5,0,0),)
        M3 = economy.Market((4,3,0),)
        
        O11 = economy.Order(water.name,price=5,amount=5,creator=MySeller1,sell=True)
        O12 = economy.Order(wheat.name,price=5,amount=5,creator=MySeller1,sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        
        O21 = economy.Order(water.name,price=1,amount=5,creator=MySeller2,sell=True)
        O22 = economy.Order(wheat.name,price=1,amount=5,creator=MySeller2,sell=True)
        M2.put_order(O21,MySeller2,sell=True)
        M2.put_order(O22,MySeller2,sell=True)
        
        O31 = economy.Order(water.name,price=3,amount=5,creator=MySeller3,sell=True)
        O32 = economy.Order(wheat.name,price=3,amount=5,creator=MySeller3,sell=True)
        O33 = economy.Order(bread.name,price=3,amount=5,creator=MySeller3,sell=True)
        M3.put_order(O31,MySeller3,sell=True)
        M3.put_order(O32,MySeller3,sell=True)
        M3.put_order(O33,MySeller3,sell=True)
        
        E.locations[M1.id] = M1
        E.locations[M2.id] = M2
        E.locations[M3.id] = M3
        
        # this is the amount I'm requesting
        amount = 25
        
        price_point_breaks, relevant_orders, requirements_cost  = MyAgent.get_coverage_relevant_orders(E,good_recipe,amount)
        mpps = MyAgent.get_manufacturing_price_points(relevant_orders, price_point_breaks, good_recipe, amount)
        
        # this is what I can deliver
        assert mpps[0].amount == 5
        assert mpps[0].price == 2
        assert mpps[1].amount == 5
        assert mpps[1].price == 6
        assert mpps[2].amount == 5
        assert mpps[2].price == 10
        
        # which is less than I want, but that's not really a problem
        # of that function.
        
        my_sum = 0
        for x in mpps:
            my_sum+=x.amount
            
        assert my_sum == 15
        assert my_sum < amount

    
    def test_get_relevant_orders(self):
        
        MyAgent = economy.EconomyAgent()
        
        materials, products, recipes = crafting.default()
        
        good_recipe = recipes["Bread"]
        amount = 25
        
        TG = economy.Tradegood
        water = TG("Water")
        wheat = TG("Grain")
        bread = TG("Bread")
        goods = {water.name: water, wheat.name: wheat, bread.name: bread}
        request_table = [water.name, wheat.name, bread.name]
        #result_table = economy.market_health_check(goods, request_table)
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20}})
        MySeller3 = economy.EconomyAgent({"Water":{"amount":20},"Grain":{"amount":20},"Bread":{"amount":10}})
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((1,0,0),)
        M2 = economy.Market((5,0,0),)
        M3 = economy.Market((4,3,0),)
        
        O11 = economy.Order(water.name,price=5,amount=10,creator=MySeller1,sell=True)
        O12 = economy.Order(wheat.name,price=5,amount=10,creator=MySeller1,sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        
        O21 = economy.Order(water.name,price=1,amount=10,creator=MySeller2,sell=True)
        O22 = economy.Order(wheat.name,price=1,amount=10,creator=MySeller2,sell=True)
        M2.put_order(O21,MySeller2,sell=True)
        M2.put_order(O22,MySeller2,sell=True)
        
        O31 = economy.Order(water.name,price=3,amount=10,creator=MySeller3,sell=True)
        O32 = economy.Order(wheat.name,price=3,amount=10,creator=MySeller3,sell=True)
        O33 = economy.Order(bread.name,price=3,amount=10,creator=MySeller3,sell=True)
        M3.put_order(O31,MySeller3,sell=True)
        M3.put_order(O32,MySeller3,sell=True)
        M3.put_order(O33,MySeller3,sell=True)
        
        E.locations[M1.id] = M1
        E.locations[M2.id] = M2
        E.locations[M3.id] = M3
        
        
        coverage_output  = MyAgent.get_coverage_relevant_orders(E,good_recipe,amount)
        
        price_point_breaks, relevant_orders, requirements_cost = coverage_output
        my_orders  = relevant_orders
        
        assert my_orders["Water"][0].price == 1
        assert my_orders["Water"][0].amount == 10
        assert my_orders["Water"][1].price == 3
        assert my_orders["Water"][1].amount == 10
        assert my_orders["Water"][2].price == 5
        assert my_orders["Water"][2].amount == 10
        
        assert my_orders["Grain"][0].price == 1
        assert my_orders["Grain"][0].amount == 10
        assert my_orders["Grain"][1].price == 3
        assert my_orders["Grain"][1].amount == 10
        assert my_orders["Grain"][2].price == 5
        assert my_orders["Grain"][2].amount == 10
    
    
    def test_trade_splitting(self):
        """theoretical problem for sawtooth basically, to prevent shortage for things."""
        MySeller1 = economy.EconomyAgent({"Water":{"amount":50},"Grain":{"amount":50},"money":{"amount":15}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":50},"Grain":{"amount":50},"money":{"amount":15}})
        
        # the problem is if I want to buy and sell large quanitites of stuff, but I have very little money and it would work out
        # with bartering, but not if you buy and then sell all at once.
        
        # solution : sell first then buy -> no liquidity problem.
        # also put in limit for lots of small trades.
        
        a = 1
    
    def test_make_or_buy(self):
                
        MyAgent = economy.EconomyAgent()
        
        TG = economy.Tradegood
        water = TG("Water")
        wheat = TG("Grain")
        
        bread = TG("Bread")
        goods = {water.name: water, wheat.name: wheat, bread.name: bread}
        request_table = [water.name, wheat.name, bread.name]
        result_table = economy.market_health_check(goods, request_table)
        
        E = economy.EconomyEnvironment()
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":50},"Grain":{"amount":50}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":50},"Grain":{"amount":50}})
        MySeller3 = economy.EconomyAgent({"Water":{"amount":50},"Grain":{"amount":50},"Bread":{"amount":10}})
        
        # default position is (0,0,0)
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((1,0,0),)
        M2 = economy.Market((5,0,0),)
        M3 = economy.Market((4,3,0),)
        
        O11 = economy.Order(water.name, price=10, amount=10, creator=MySeller1, sell=True)
        O12 = economy.Order(wheat.name, price=10, amount=10, creator=MySeller1, sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        
        O21 = economy.Order(water.name, price=1, amount=10, creator=MySeller2, sell=True)
        O22 = economy.Order(wheat.name, price=1, amount=10, creator=MySeller2, sell=True)
        M2.put_order(O21,MySeller2,sell=True)
        M2.put_order(O22,MySeller2,sell=True)
        
        O31 = economy.Order(water.name, price=3, amount=10, creator=MySeller3, sell=True)
        O32 = economy.Order(wheat.name, price=3, amount=10, creator=MySeller3, sell=True)
        O33 = economy.Order(bread.name, price=8, amount=10, creator=MySeller3, sell=True)
        M3.put_order(O31,MySeller3,sell=True)
        M3.put_order(O32,MySeller3,sell=True)
        M3.put_order(O33,MySeller3,sell=True)
        
        E.locations[M1.id] = M1
        E.locations[M2.id] = M2
        E.locations[M3.id] = M3
        
        materials, products, recipies = crafting.default()
        
        bread_recipe = recipies["Bread"]
        
        r = MyAgent.make_or_buy(E,bread_recipe,amount =25)
        
        make_average = 4
        make_cost = (10*(1+1))+(10*(3+3))
        make_amount = 20
        
        buy_price = 8 
        buy_total = 80
        buy_amount = 10
        
        # material price for the stuff that I'm not making,
        # would be 20 per piece.
        
        assert r["make"]['total cost'] == make_cost
        assert r["make"]['amount'] == make_amount
        assert r['buy']['total price'] == buy_total
        assert r['buy']['amount'] == buy_amount
        
        #assert result_table == {'water': {'sell volume': 0.01, 'buy volume': 1, 'sell state': 'undervalued', 'buy state': 'undervalued'}, 'iron': {'sell volume': 1, 'buy volume': 0.2, 'sell state': 'overpriced', 'buy state': 'undervalued'}, 'bread': {'sell state': 'not sold', 'buy state': 'not bought'}}
        
        
        # this still fails,
        # because at low amount(s) (here, less than 21(?) 25 in the other example, it's not creating enough objects
        # with the data.
        r = MyAgent.make_or_buy(E,bread_recipe)
    
    def test_find_manufacturing_cost_fail(self):
        MyAgent = economy.EconomyAgent()
        E = economy.EconomyEnvironment()
        #E.locations[M1.id] = M1
        
        materials, products, recipies = crafting.default()
        
        bread_recipe = recipies["Bread"]
        
        r = MyAgent.find_manufacturing_cost(E,bread_recipe,27)
        
        # can't make any for any price.
        assert r == (0, [], 0)

    def test_find_manufacturing_cost_stocks_prices(self):
        
        MyAgent = economy.EconomyAgent()
        
        MyAgent.inventory = {
                            "Water":{"amount":50},
                            "Grain":{"amount":50},
                            }
                            
        MyAgent.prices = {
                         "Water":1,
                         "Grain":0.8,
                         }
        
        E = economy.EconomyEnvironment()
        
        materials, products, recipies = crafting.default()
        
        bread_recipe = recipies["Bread"]
        
        r = MyAgent.find_manufacturing_cost(E,bread_recipe,27,requirements_stocks=MyAgent.inventory)
        
        something, pricepoints = r
        
        assert len(pricepoints) == 1
        assert pricepoints[0].price == 1.8
        
        
    def test_find_manufacturing_cost_order_stock_mix(self):
        MyAgent = economy.EconomyAgent()
        
        MyAgent.inventory = {"Grain":{"amount":100}}
        MyAgent.prices = {"Grain":1}
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":100}})
        E = economy.EconomyEnvironment()
        
        
        M1 = economy.Market((0,0,0),)
        
        # the first 5 at 1, the next 10, for a sum of 15, at 2
        # and then the next 20 at a price of 3. for a total of 35
        
        O11 = economy.Order("Water",price=1,amount=5,creator=MySeller1,sell=True)
        O12 = economy.Order("Water",price=2,amount=10,creator=MySeller1,sell=True)
        O13 = economy.Order("Water",price=3,amount=20,creator=MySeller1,sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        M1.put_order(O13,MySeller1,sell=True)
        
        
        E.locations[M1.id] = M1
        
        materials, products, recipies = crafting.default()
        
        bread_recipe = recipies["Bread"]
        
        r = MyAgent.find_manufacturing_cost(E,bread_recipe,27,requirements_stocks = MyAgent.inventory)
        
        total_price, price_points = r
        assert total_price == 27*1 + 5*1 + 10*2 + 12*3
        assert total_price == 88
        assert len(price_points)==3
        assert price_points[0].amount ==5
        assert price_points[1].amount ==10
        assert price_points[2].amount ==12
        assert price_points[0].price == 2
        assert price_points[1].price == 3
        assert price_points[2].price == 4
    
    def test_find_manufacturing_cost_orders(self):
        
        MyAgent = economy.EconomyAgent()
        
        TG = economy.Tradegood
        water = TG("Water")
        wheat = TG("Grain")
        bread = TG("Bread")
        
        goods = {water.name: water, wheat.name: wheat, bread.name: bread}
        request_table = [water.name, wheat.name, bread.name]
        result_table = economy.market_health_check(goods, request_table)
        
        E = economy.EconomyEnvironment()
        
        MySeller1 = economy.EconomyAgent({"Water":{"amount":100},"Grain":{"amount":100}})
        MySeller2 = economy.EconomyAgent({"Water":{"amount":100},"Grain":{"amount":100}})
       
        # default position is (0,0,0)
        
        E = economy.EconomyEnvironment()
        
        M1 = economy.Market((0,0,0),)
        
        # the first 5 at 1, the next 10, for a sum of 15, at 2
        # and then the next 20 at a price of 3. for a total of 35
        
        O11 = economy.Order(water.name,price=1,amount=5,creator=MySeller1,sell=True)
        O12 = economy.Order(water.name,price=2,amount=10,creator=MySeller1,sell=True)
        O13 = economy.Order(water.name,price=3,amount=20,creator=MySeller1,sell=True)
        M1.put_order(O11,MySeller1,sell=True)
        M1.put_order(O12,MySeller1,sell=True)
        M1.put_order(O13,MySeller1,sell=True)
        
        # first 10 at a price of 1, the next 20 at a price of 2, for a total of 30.
        
        O21 = economy.Order(wheat.name,price=1.4,amount=10,creator=MySeller2,sell=True)
        O22 = economy.Order(wheat.name,price=2,amount=20,creator=MySeller2,sell=True)
        O23 = economy.Order(wheat.name,price=3,amount=30,creator=MySeller2,sell=True)
        M1.put_order(O21,MySeller2,sell=True)
        M1.put_order(O22,MySeller2,sell=True)
        M1.put_order(O23,MySeller2,sell=True)
        
        
        E.locations[M1.id] = M1
        
        materials, products, recipies = crafting.default()
        
        bread_recipe = recipies["Bread"]
        
        r = MyAgent.find_manufacturing_cost(E,bread_recipe,27)
        if r != None:
            total_cost, pricepoints = r
        
        assert pricepoints[0].amount == 5
        assert pricepoints[0].price == 2.4
        
        assert pricepoints[1].amount == 5
        assert pricepoints[1].price == 3.4
        
        assert pricepoints[2].amount == 5
        assert pricepoints[2].price == 4
        
        assert pricepoints[3].amount == 12
        assert pricepoints[3].price == 5
        
        total_cost_real = 5*2.4 + 5*3.4 + 5*4 + 12*5
        assert total_cost == total_cost_real
        
        matplot = False
        if matplot:
            from matplotlib import pyplot as plt
            xs = []
            ys = []
            total_amount = 0
            for x in pricepoints:
                total_amount += x.amount
                xs.append(total_amount)
                ys.append(x.price)
                
            xs = [xs[0]]+xs
            ys = [ys[0]]+ys
            
            plt.grid()
            plt.ylim(0,6)
            plt.plot(xs,ys)
            plt.show()
            
    def test_transaction_sum(self):
        
        T1 = economy.Transaction(None,"Wood",1,"money",2)
        T2 = economy.Transaction(None,"Wood",2,"money",4)
        
        T3 = T1 + T2
        
        assert T3.good_a == T1.good_a
        assert T3.amount_a == 3
        assert T3.good_a == "Wood"
        assert T3.amount_b == 6
        assert T3.good_b == "money"
        
        myid1 = str(T3.id)
        
        T4 = economy.Transaction(None,"Wood",1,"money",2)
        
        T3 += T4
        
        myid2 = str(T3.id)
        
        assert myid1 != myid2
        
        assert T3.amount_a == 4
        assert T3.good_a == "Wood"
        assert T3.amount_b == 8
        assert T3.good_b == "money"
        
    def test_figure_out_most_profitable_product(self):
        
        # so I need some list of transactions,
        # I need market prices for materials
        # and need something about demand.
        
        # if I sold out, there is more demand for product A
        # than product B, even if the % gain for product B is higher.
        
        a_market = economy.Market()
        
        my_agent = economy.EconomyAgent()
        
        my_agent.inventory = {"Food":{"amount":50},
                            "Seashell":{"amount":50},
                            "funny rock":{"amount":50},
                            "Diamond":{"amount":10},
                            }
        
        my_agent.transactions = [
        economy.Transaction(None,"Wood",1,"money",-1,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Seashell",-1,"money",1,my_agent),
        economy.Transaction(None,"Diamond",-1,"money",10,my_agent),
        ]
        
        my_order = economy.Order("Food",2.5,20,my_agent)
        my_order2 = economy.Order("Seashell",1,20,my_agent)
        my_order3 = economy.Order("funny rock",1,20,my_agent)
        my_order4 = economy.Order("Diamond",1,1,my_agent)
        
        a_market.put_order(my_order,my_agent)
        a_market.put_order(my_order2,my_agent)
        a_market.put_order(my_order3,my_agent)
        a_market.put_order(my_order4,my_agent)
        
        my_order4.amount = 0
        
        # so, when I interact with the market in a regular way.
        # I kind of want an analysis tick that 
        
        # when do i remove my old orders? probably some set time.
                
        # this is actually my highest selling product.
        # not necessarily my most profitable one.
        transaction_sum_list, sold_out = my_agent.figure_out_most_profitable_product()
        
        transaction_sum_list.sort(key= lambda x : x.amount_b, reverse=True)
        
        assert transaction_sum_list[0].good_a == "Food"
        assert transaction_sum_list[0].good_b == "money"
        assert transaction_sum_list[1].good_a == "Diamond"
        
        assert sold_out == ["Diamond"]
    
    def get_full_marketing(self):
        
        # get the best products by price / profit / volume / sales.
        
        a_market = economy.Market()
        
        my_agent = economy.EconomyAgent()
        
        my_agent.inventory = {"Food":{"amount":50},
                            "Seashell":{"amount":50},
                            "funny rock":{"amount":50},
                            "Diamond":{"amount":10},
                            }
        
        my_agent.transactions = [
        economy.Transaction(None,"Wood",1,"money",-1,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Food",-2,"money",5,my_agent),
        economy.Transaction(None,"Seashell",-1,"money",1,my_agent),
        economy.Transaction(None,"Diamond",-1,"money",10,my_agent),
        ]
        
        my_order = economy.Order("Food",2.5,20,my_agent)
        my_order2 = economy.Order("Seashell",1,20,my_agent)
        my_order3 = economy.Order("funny rock",1,20,my_agent)
        my_order4 = economy.Order("Diamond",1,1,my_agent)
        
        a_market.put_order(my_order,my_agent)
        a_market.put_order(my_order2,my_agent)
        a_market.put_order(my_order3,my_agent)
        a_market.put_order(my_order4,my_agent)
        
        my_order4.amount = 0
        
        # so, when I interact with the market in a regular way.
        # I kind of want an analysis tick that 
        
        # when do i remove my old orders? probably some set time.
                
        # this is actually my highest selling product.
        # not necessarily my most profitable one.
        transaction_sum_list, sold_out = my_agent.figure_out_most_profitable_product()
        
        transaction_sum_list.sort(key= lambda x : x.amount_b, reverse=True)
        
        assert transaction_sum_list[0].good_a == "Food"
        assert transaction_sum_list[0].good_b == "money"
        assert transaction_sum_list[1].good_a == "Diamond"
        
        assert sold_out == ["Diamond"]
        
        # also set up the manufacturing info
        
        
        a = 1
    
    def test_restock_orders(self):
        
        M = economy.Market()
        agent = economy.EconomyAgent()
        agent.inventory = {"Wood":{"amount":20},"Food":{"amount":20}}
        
        Order1 = economy.Order("Wood",1,10,self) 
        Order2 = economy.Order("Food",1,10,self) 
        
        M.put_order(Order1,agent)
        M.put_order(Order2,agent)
        
        
        assert agent.inventory["Wood"]["amount"]==10
        assert agent.inventory["Food"]["amount"]==10
        
        Order1.amount = 0
        Order2.amount = 0
        
        M.restock_order(Order1,agent)
        M.restock_order(Order2,agent)
        
        assert agent.inventory["Wood"]["amount"] == 0
        assert agent.inventory["Food"]["amount"] == 0
        
        assert Order1.amount == 10
        assert Order2.amount == 10
        
        
        
    def test_get_needed_material(self):
        # this is covered by shopping list in test_crafting.
        a=1
    
    def test_buy_from_transaction(self):
        
        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":25}}
        
        T2 = economy.EconomyAgent()
        T2.inventory = {"money":{"amount":5000}}
        
        # kind of misleading, I should...
        # make sure this isn't misunderstood... hmmmm...
        T_ob = T2.perform_buy_from_transaction(T1,"wood",15,2)
        
        assert T_ob.good_a == "wood"
        assert T_ob.amount_a == 2
        assert T_ob.good_b == "money"
        assert T_ob.amount_b == 15
        
        assert T2.inventory == {'money': {'amount': 4985}, 'wood': {'amount': 2}}
        assert T1.inventory == {'wood': {'amount': 23}, 'money': {'amount': 15}}

        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":5}}
        
        T2 = economy.EconomyAgent()
        T2.inventory = {"money":{"amount":5000}}
        
        # kind of misleading, I should...
        # make sure this isn't misunderstood... hmmmm...
        T_ob = T2.perform_buy_from_transaction(T1,"wood",15,10)
        
        # not enough wood.
        assert T_ob == False
                
        assert T2.inventory == {"money":{"amount":5000}}
        assert T1.inventory == {"wood":{"amount":5}}
        
        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":20}}
        
        T2 = economy.EconomyAgent()
        T2.inventory = {"money":{"amount":3}}
        
        T_ob = T2.perform_buy_from_transaction(T1,"wood",15,10)
        
        # not enough money
        assert T_ob == False
                
        assert T2.inventory == {"money":{"amount":3}}
        assert T1.inventory == {"wood":{"amount":20}}
        
        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":20}}
        
        T2 = economy.EconomyAgent()
        T2.inventory = {"money":{"amount":500}}
        
        T_ob = T2.perform_buy_from_transaction(T1,"iron",15,10)
        
        # good doesn't exist
        assert T_ob == False
                
        assert T2.inventory == {"money":{"amount":500}}
        assert T1.inventory == {"wood":{"amount":20}}
        
        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":20}}
        
        T2 = economy.EconomyAgent()
        T2.inventory = {}
        
        T_ob = T2.perform_buy_from_transaction(T1,"wood",15,10)
        
        # money not in inventory
        assert T_ob == False
                
        assert T2.inventory == {}
        assert T1.inventory == {"wood":{"amount":20}}
        
    def test_shop_or_stall(self):
        
        # order sales
        #ENV=economy.EconomyEnvironment()
        
        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":25}}
        T1.offered_goods = {"wood":{"amount":25}}
        
        T1.wanted_goods = {"money":{"amount":float("inf")}}
        
        T2 = economy.EconomyAgent()
        T2.wanted_goods = {"wood":{"amount":10}}
        T2.inventory = {"money":{"amount":5000}}
        
        M = economy.Market()
        M.set_up_trader(T1)
        T1.set_up_selling({"wood":1})
        
        r2 = T2.market_interaction(M)
        
        
        assert len(T1.transaction_log)==1
        assert len(T2.transaction_log)==1
        
        assert "wood" in T2.inventory
        assert T2.inventory["money"]["amount"]==4990
        assert T2.inventory["wood"]["amount"]==10
        assert T2.wanted_goods == {}
        
    
    
    def test_shop_or_stall_fail(self):
        
        # order sales
        #ENV=economy.EconomyEnvironment()
        
        T1 = economy.EconomyAgent()
        T1.inventory = {}
        T1.offered_goods = {}
        T1.wanted_goods = {"money":{"amount":float("inf")}}
        
        T2 = economy.EconomyAgent()
        T2.wanted_goods = {"wood":{"amount":10}}
        T2.inventory = {"money":{"amount":5000}}
        
        M = economy.Market()
        M.set_up_trader(T1)
        
        T1.set_up_selling({"wood":1})
        
        r2 = T2.market_interaction(M)
        
        assert len(T1.transaction_log)==0
        assert len(T2.transaction_log)==0
                
        #assert "wood" in T2.inventory
        #assert T2.inventory["wood"]["amount"]==10
        
    def test_sell_order(self):
        # order sales
        ENV = economy.EconomyEnvironment()

        T1 = economy.EconomyAgent()
        T1.inventory = {"wood": {"amount": 25}, "money": {"amount": 5000}}
        T1.wanted_goods = {"wheat": {"amount": 10}}

        T2 = economy.EconomyAgent()
        T2.inventory = {"wheat": {"amount": 25}, "money": {"amount": 5000}}
        T2.wanted_goods = {"wood": {"amount": 10}}

        # wheat=economy.Tradegood("wheat")
        # wood=economy.Tradegood("wood")

        M = economy.Market()

        O2 = economy.Order("wood", price=1, amount=10, creator=T1, sell=True)
        M.put_order(O2, T1, sell=True)

        assert T1.inventory["wood"]["amount"] == 15

        O = economy.Order("wheat", price=1, amount=10, creator=T2, sell=True)
        M.put_order(O, T2, sell=True)

        assert T2.inventory["wheat"]["amount"] == 15
        
        # these are naturally not happening simultaneously,
        # so I need 2 calls each.
        
        # buy and put in pickup
        r1 = T1.market_interaction(M)
        r2 = T2.market_interaction(M)
        
        # pickup.
        r1 = T1.market_interaction(M)
        r2 = T2.market_interaction(M)

        # the wheat and the wood should be in the collection area

        assert "wheat" in T1.inventory
        assert T1.inventory["wheat"]["amount"] == 10
        assert "wood" in T2.inventory
        assert T2.inventory["wood"]["amount"] == 10
        
        s1 = T1.sum_difference_from_transactions()
        s2 = T2.sum_difference_from_transactions()
        
        assert s1 == {'wood': -10, 'money': 0, 'wheat': 10}
        assert s2 == {'wood': 10, 'money': 0, 'wheat': -10}

    def test_buy_order(self):
        # order sales
        ENV = economy.EconomyEnvironment()

        T1 = economy.EconomyAgent()
        T1.inventory = {"wood":{"amount":25},"money":{"amount":5000}}
        T1.wanted_goods = {"wheat":{"amount":10}}
        T1.offered_goods = {"wood":{"amount":25}}

        T2 = economy.EconomyAgent()
        T2.inventory = {"wheat":{"amount":25},"money":{"amount":5000}}
        T2.wanted_goods = {"wood":{"amount":10}}
        T2.offered_goods = {"wheat":{"amount":25}}

        # wheat=economy.Tradegood("wheat")
        # wood=economy.Tradegood("wood")

        M = economy.Market()

        O = economy.Order("wheat",price=1,amount=10,creator=T1,sell=False)
        M.put_order(O, T1,sell=False)

        assert T1.inventory["money"]["amount"] == 4990
        assert T1.inventory["wood"]["amount"] == 25
        assert "wheat" not in T1.inventory

        O2 = economy.Order("wood",price=1,amount=10,creator=T2,sell=False)
        M.put_order(O2, T2,sell=False)

        assert T2.inventory["money"]["amount"] == 4990
        assert T2.inventory["wheat"]["amount"] == 25
        assert "wood" not in T2.inventory
        
        # these are naturally not happening simultaneously,
        # so I need 2 calls each.
        
        # buy and put in pickup
        r1 = T1.market_interaction(M)
        r2 = T2.market_interaction(M)
        
        #pickup.
        r2 = T2.market_interaction(M)
        r1 = T1.market_interaction(M)

        # the wheat and the wood should be in the collection area

        assert "wheat" in T1.inventory
        assert T1.inventory["wheat"]["amount"] == 10
        assert T1.inventory["wood"]["amount"] == 15
        assert "wood" in T2.inventory
        assert T2.inventory["wood"]["amount"] == 10
        assert T2.inventory["wheat"]["amount"] == 15
                
        s1 = T1.sum_difference_from_transactions()
        s2 = T2.sum_difference_from_transactions()
        
        assert s1 == {'wood': -10, 'money': 0, 'wheat': 10}
        assert s2 == {'wood': 10, 'money': 0, 'wheat': -10}
        
    def test_bartering_1(self):
        # bartering?
        ENV=economy.EconomyEnvironment()
        
        wheat=economy.Tradegood("wheat")
        wood=economy.Tradegood("wood")
        
        T1=economy.EconomyAgent()
        T1.inventory={"wood":{"amount":25}}
        T1.offered_goods={"wood":{"amount":25}}
        T1.wanted_goods={"wheat":{"amount":10}}
        
        T1.price_reference = {"wheat":4,"wood":1} # vary this
        
        T2=economy.EconomyAgent()
        T2.inventory={"wheat":{"amount":25}}
        T2.offered_goods={"wheat":{"amount":25}}
        T2.wanted_goods={"wood":{"amount":10}}
        
        T2.price_reference = {"wheat":1,"wood":4} # vary this
        
        M = economy.Market()
        # some kind of barter area
        
        M.set_up_trader(T1) # declare offered, asked
        M.set_up_trader(T2) # declare offered, asked
        M.resolve_barter_trade()
        
        # so in this trade, both traders undervalue their stuff
        # and they overvalue the stuff they want.
        # when in reality, both have equal amounts of stuff and they 
        # could just trade 1:1
        
        # so, they make a severely bad offer, and offer everything they
        # have for the other persons 10 thingies.
        # the trade will be resolved with an advantage for one person, basically randomly.
        # but the price will also drop, because the old price was 4:1
        # and 25:10 is 2.5:1
        
        ##### !!!
        # and if I repeat this, the price reference should adjust itself.
        ##### !!!
        
        # should file each other as potential trades
        
        # doing this here without a monetary background is fine, 
        # if there is no value reference, it doesn't matter much
        # and if one exists it will slowly propagate through the system.
        
        assert "wheat" in T1.inventory
        assert T1.inventory["wheat"]["amount"] >= 10
        assert "wood" in T2.inventory
        assert T2.inventory["wood"]["amount"] >= 10

def single_test():
    TE = TestEconomy()
    
    TE.test_find_manufacturing_cost_fail()
    TE.test_find_manufacturing_cost_orders()
    TE.test_find_manufacturing_cost_stocks_prices()
    TE.test_find_manufacturing_cost_order_stock_mix()
    

if __name__ == "__main__":
    #unittest.main()
    single_test()
