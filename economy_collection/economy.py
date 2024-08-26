import math
import uuid

class ManufacturingPricePoint:
    def __init__(self, price, amount,recipe):
        self.requirement_prices = {} # requirement_name : price
        self.price = price
        self.amount = amount
        self.recipe = recipe
    
    def __repr__(self):
        return f"<gamedevstuff.economy.ManufacturingPricePoint {self.recipe.name} price:{self.price} n:{self.amount}>"

class Order:
    """this kind of a weak object, it's a python object for something
    that will mostly exist in list or database form. I am not
    certain I even need this type at all. Ah well. I might.
    
    Maybe when creating one for UI.
    """
    def __init__(self,good,price,amount,creator,sell=True,creation_time=None,minimum_amount=1):
        
        self.sell = sell
        self.good = good
        self.price = price
        self.amount = amount
    
        self.creator = creator
        
        self.minimum_amount = minimum_amount
        self.creation_time  = creation_time
        
        self.location = None # filled by put_order ?
        
    def __repr__(self):
        return f"<gamedevstuff.economy.Order {self.good} price:{self.price} n:{self.amount}>"
            
    def adjust_price(self,percent_increase):
        """
        increases or decreases the price, input is assumed positive (1.1, 1.2), so for negative
        changes enter values small than 1
        """
        self.price      = math.floor(self.price*percent_increase)
        self.ask_amount = math.ceil(self.price*self.offer_amount)
        
     
class Transaction:
    """
    simpler form of a trade, any exchange is always an exchange against
    money.
    
    I kind of want another object, that acts like a diff / commit.
    
    party_a has all values applied to it normally.
    
    party_b has everything inverted ?
    
    """
    def __init__(self,date,good_a,amount_a,good_b,amount_b,party_a=None,party_b=None):
        self.date = date
        self.good_a = good_a
        self.amount_a = amount_a
        self.party_a = party_a
        
        self.good_b = good_b
        self.amount_b = amount_b
        self.party_b = party_b
    
    def __repr__(self):
        s="<gamedevstuff.economy.Transaction"
        s+=f" {self.good_a} x {self.amount_a} exchanged for {self.good_b} x {self.amount_b} at {self.date}"
        s+=">"
        return s

class Trade:
    """
    trade_dict should be {"offered":[], "asked":[]}
    
    
    dealing with raw items is difficult

    the approach would be to "cast" it into a value environment
    that would factor in how difficult it is to move physically 
    to the market,
    
    how big the demand is and whether the goods can be sold
    and things like that.
    
    So this is really basically just a glorified list with
    
    side a
    side b
    
    goods. :/
    
    what's the excpected flow of this?
    
    
    self will bring some idea of value, probably a past
    market value record.
    
    self will look for someone willing to buy or sell whatever he needs
    but doing the buy of self's goods first, to generate the money.
    
    alternatively direct trades according to market value is acceptable as well.
    
    
    1. self will come to a trader or market and will either
    1.1 want to buy something
    1.2 want to sell something
    1.3 or both.
    
    2. person a sees something where trading is possible and
    initiates a trade offer
    2.1 haggling can ensue where an initial offer is being made
    and the actual trade is postponed, when searching for a different offer.
    2.2 this will optionally hold until some point in the future
    e.g. "make the round, look at the offers" or get accepted immediately
    
    depending on who thinks they can still get a better deal, or how well they are doing,
    how urgent it is to them to generate income, they will have a different "haggling weight"?
    
    how would I express this?
    
    if I have already traded well today and can meet my needs, I would not be under pressure to agree to further trades.
    if I already know I'm giving a good offer relative to market rate and the customer will return eventually.
    
    however, if I have not yet acquired what I need and the supply is 
    going down, time limit is close I would be under pressure
    if there is nearly no supply anywhere and the good is very rare, and I really need it.
    
    if the offer made is already really really good, I wouldn't want to risk that the partner rejects the trade.
    
    ###
    
    there should be some kind of identification/type check that allows for
    trading "junk" that's actually highly valuable.
    
    that means I can't really do it by object type. or I have to build something
    into the object type that would alter it's true appearance to the 
    holder.
    
    ###
    
    none of that is relevant for order based trading.
    
    order based trading will be different depending on how much time
    you have, what the access fee is like, what kind of risk people
    are willing to take for selling.
    
    this also should be expressed in some value.
    
    and you move away from haggling when just moving more product results
    in more gains. either because of the volume being traded, or because
    haggling takes too much time. WHICH MEANS
    I can express the haggling as approaching each others ideal prices
    in weights and times,until point t where one party no longer wants to wait o
    r waiting becomes not profitable on average.
    
    and barter trading is better when the exchange rate of the barter
    trade is better than eating the margin of one trader for selling
    what you have and eating the margin from another trader when
    buying what you need.
    
    ######################
    so the optimal case would be a competitive environment
    with fixed price over the counter business.
    
    look for those first.
    ###
    
    if that's not available
    
    look for someone who has what you want.
    
    ### on a market, a big city, or ask around where it's available
    
    check their price.
    
    offer to barter
    
    if they accept see where that goes
    
    else negotiate a trade
    
    then scratch up that money somehow.
    
    
    """
    def __init__(self,trader,trade_dict=None):
        
        # where does this exist
        
        self.trader_a = trader
        self.trader_b = None
        
        self.trade_dict = trade_dict
        
        self.trader_a_confirmed = False
        self.trader_b_confirmed = False
    
    def depr_value_against(self, market_or_market_record, margin=0.25):
        """
        this is meant to be used by agents in the sense that 
        they will have or bring an idea of a market with them.
        
        and do
        
        some_trade = Trade()
        my_market = my_agent.default_market
        is_deal, left_overs = some_trade.value_against(my_market)
        
        For example. you may build a shopping list for your village at home
        keeping in mind the prices people are willing/able to pay. you
        bring this idea to another market have to evaluate whether the trade 
        you are about to conduct will make sense when you come back home
        and want to sell your stuff.
        """
        # there is some idea of "less than market price"
        # but there is also "this is worth nothing to me if I keep it"
        # so, the value one is willing to accept goes down if 
        # driven by external forces/priorities.
        
        market = market_or_market_record
        
        fictional_value = 0
        not_tradeable = {}
        sell_value,ns_goods = depr_evaluate_trade_side(market,sell=True)
        buy_value,nb_goods = depr_evaluate_trade_side(market,sell=False)
        leftovers =  {"not sold":ns_goods,"not bought":nb_goods}
        # if I am an asshole, I would charge more for the sell value
        # and offer less for the buy value
        
        # if the *trader* is doing this, apply the margins
        # if you are the customer, you just have to take it or leave it.
        
        if sell_value*(1+margin) > buy_value*(1-margin):
            good_trade = True
        else:
            good_trade = False
        
        return good_trade, leftovers
        
    def depr_evaluate_trade_side(self, market, sell=True):
        """
        by default sell=true, iterate over my "selling" goods
        and see if there are compatible "buy" orders on the market
        
        not tradeable will by filled, because nobody is buying and you
        can't sell.
        
        otherwise, the reverse, iterating over goods you want to buy,
        checking for buy orders and not_tradeable will be filled if goods
        you couldn't buy.
        """
        # I guess it doesn't really matter what the market defining
        # good, material or service is. the value will be determined
        # against it anyway, I just need to take that I don't
        # accidentally compare markets with the wrong "base"
        
        kw_one="sell"
        kw_two="buy"
        if not sell:
            kw_one,kw_two = kw_two,kw_one #invert
        fictional_value = 0
        not_tradeable = {}
        for x in self.trade_dict[kw_one]:
            if x in market.orders[kw_two]:
                a = self.trade_dict[kw_one][x]["amount"]
                rest_amount = a
                good_market_value = 0
                for order in market.orders[kw_two][x]:
                    if order.minimum_amount < rest_amount < order.amount:
                        price = order.price
                        
                        if rest_amount < order.amount:
                            value = price*rest_amount
                            good_market_value+=value
                            rest_amount = 0
                            break # no more volume to sell.
                        else:
                            value = price*order.amount
                            rest_amount-=order.amount
                            good_market_value+=value
            
                if rest_amount != 0:
                    not_tradeable[kw_one][x]=rest_amount
        
        return value, not_tradeable
        
    #this is stuff for threads.
    def confirm(self,trader):
        if trader == self.trader_a:
            self.trader_a_confirmed=True

    def __repr__(self):
        s="---\n"
        for obs in self.objects_a:
            s+= str(obs)+" "+str(self.objects_a[obs])+"\n"
        s+="---\noffers vs. wants\n---\n"
        for obs in self.objects_b:
            s+= str(obs)+" "+str(self.objects_a[obs])+"\n"
        s+="---"
        return s
        
    def create_log(self):
        s=""
        s+=str(self.offered.d)
        s+=";"
        s+=str(self.requested.d)
        s+="\n"
        return s

class Tradegood:
    def __init__(self,name,id=None):
        self.name=name
        self.id=id
        self.weekly_sell_volume=0
        self.sell_order_volume=0
        
        self.weekly_buy_volume=0
        self.buy_order_volume=0
        
        self.average_sell=0
        self.average_buy=0
     
    def __repr__(self):
        return "<Tradegood:"+self.name+">"
    
    def __eq__(self,other):
        if type(other) ==type(self):
            if self.name==other.name:
                return True
                
        return False
        
def market_health_check(goods,request_table):
    
    result_table={}
    for goodname in request_table:
        if goodname not in goods:
            continue
        
        good=goods[goodname]
        result_table[goodname]={}
        
        re=result_table[goodname]
        #the weekly stuff may be unkown?
        
        if good.weekly_sell_volume==0:
            re["sell state"]="not sold"
        else:
            if good.sell_order_volume > good.weekly_sell_volume:
                re["sell volume"]=1
            else:
                frac=good.sell_order_volume / good.weekly_sell_volume
                re["sell volume"]=frac
                
        if good.weekly_buy_volume==0:
            re["buy state"]="not bought"
        else:
            if good.buy_order_volume > good.weekly_buy_volume:
                re["buy volume"]=1
            else:
                frac=good.buy_order_volume / good.weekly_buy_volume
                re["buy volume"]=frac
                
        if good.weekly_sell_volume==0 and good.weekly_buy_volume==0:
            continue
        
        #prices
        
        if good.average_sell * 1.10 > good.desired_sell > good.average_sell*0.9:
            re["sell state"]="healthy"
        elif good.average_sell * 1.10 < good.desired_sell:
            re["sell state"]="undervalued"
        elif good.average_sell * 0.9 > good.desired_sell:
            re["sell state"]="overpriced"
            
        
        if good.average_buy * 1.10 > good.desired_buy > good.average_buy*0.9:
            re["buy state"]="healthy"
        elif good.average_buy * 1.10 < good.desired_buy:
            re["buy state"]="undervalued"
        elif good.average_buy * 0.9 > good.desired_buy:
            re["buy state"]="overpriced"
            
    return result_table


def perform_direct_barter_trade(trader1,trader2,offer):
    """this is for when an offer has been evaluated and judged good
    the system has to perform this, not the traders.
    so don't call this directly on UI action.
    
    reduce the amounts.
    
    raise value errors if values go below 0
    
    offer format is
    {trader:{offered_good:amount},trader:{offered_good:amount}}
    
    """
    
    for g in offer[trader1]:
        amount=offer[trader1][g]
        trader1.inventory[g]["amount"]-=amount
        trader1.offered_goods[g]["amount"]-=amount
        if g not in trader2.inventory:
            trader2.inventory[g]={"amount":0}
        trader2.inventory[g]["amount"]+=amount
        trader2.wanted_goods[g]["amount"]-=amount
        
        #remove stuff, ensure I'm not going negative.
        if trader1.inventory[g]["amount"]==0:
            trader1.inventory.pop(g)
        elif trader1.inventory[g]["amount"]<0:
            raise ValueError
            
        if trader1.offered_goods[g]["amount"]==0:
            trader1.offered_goods.pop(g)
        elif trader1.offered_goods[g]["amount"]<0:
            raise ValueError
            
        if trader2.wanted_goods[g]["amount"]<=0:
            trader2.wanted_goods.pop(g)
            #I got more than I needed.
        
    for g in offer[trader2]:
        amount=offer[trader2][g]
        trader2.inventory[g]["amount"]-=amount
        trader2.offered_goods[g]["amount"]-=amount
        if g not in trader1.inventory:
            trader1.inventory[g]={"amount":0}
        trader1.inventory[g]["amount"]+=amount
        trader1.wanted_goods[g]["amount"]-=amount
        
        #remove stuff, ensure I'm not going negative.
        if trader2.inventory[g]["amount"]==0:
            trader2.inventory.pop(g)
        elif trader2.inventory[g]["amount"]<0:
            raise ValueError
            
        if trader2.offered_goods[g]["amount"]==0:
            trader2.offered_goods.pop(g)
        elif trader2.offered_goods[g]["amount"]<0:
            raise ValueError
            
        if trader1.wanted_goods[g]["amount"]<=0:
            trader1.wanted_goods.pop(g)
            # I got more than I needed.
            
        # I could add these to offered goods instead
        return

def calculate_profit_from_trades(tlist,measure="gold"):
    """calculate"""
    d={}
    for t in tlist:
        if measure==t.good_a:
            good=t.good_b
            good_m=t.amount_b
            money=t.amount_a
        
        elif measure == t.good_b:
            good=t.good_a
            good_m=t.amount_a
            money=t.amount_b
        
        if good not in d:
            d[good]={"amount":0,"profit":0}
        
        d[good]["amount"]+=good_m
        d[good]["profit"]+=money
    return d


class plan:
    def __init__(self,agent):
        
        self.agent    = agent
        self.worktime = 0
        
        self.evalu()
        
    def evalu(self):
        
        #for now, farming should be "make as much as you can, eat some and sell the rest"
        #crafting should be, "craft as much as you can, sell it and buy what you need"
        
        fs=self.agent.skills["farming"]#farming_skill
        cs=self.agent.skills["crafting"]#crafting_skill
        
        w     = self.agent.watched_goods["wheat"]
        w_in  = w.inflow
        w_out = w.outflow
        
        m     = self.agent.watched_goods["gold"]
        m_in  = m.inflow
        m_out = m.outflow
        
        self.timeframe = self.agent.env.timeob.get_var_translations()
        #goal for survival is to get my the wheat inflow on the same level as the 
        #wheat outflow
        
        #will I need to do something at all?

        if w_in<w_out:
            #yes,eventually
            diff=w_out-w_in
            
            #make or buy it?
            if fs>cs:
                self.agent.worktype = "farming"
                make                = True
                buy                 = False
                
                self.agent.watched_goods["crafts"].in_demand = True
                
            else:
                
                self.agent.worktype = "crafting"
                make                = False
                buy                 = True
            
            if buy:
                self.agent.produce  = "crafts"
                self.agent.worktype = "crafting"
                #increase the perceived price, because now the good is in
                #demand, I want it and I'm ready to pay a little more to get it.
                
                #w.pov_price += 1.05 *w.market_price
                
                #this is not the price I'll pay in every case,
                #this is price this agent is willing to pay
                
                #ok so 
                #start at market price
                #if I have enough money
                
                #WHAT THE FUCK.
                #if "gold" in self.agent.watched_goods:
                #    if self.agent.watched_goods["gold"].stock>w.market_price:
                #        order(self.agent.env,self.agent,w.name,m.name,w.market_price,10,1)
                
                #if "crafts" in self.agent.watched_goods:
                 #   c=self.agent.watched_goods["crafts"]
                #    order(self.agent.env,self.agent,m.name,c.name,c.market_price,1,15)
                
                
            if make:
                self.agent.produce  = "wheat"
                self.agent.worktype = "farming"
                
    def reeval(self):
        self.evalu()

class good_perception:
    """
    It is easier to have a record of old market behavior and use
    that as a basis for calculating a value, rather than creating
    a new "history" object that does the same, but with more types
    and not recoverable.
    
    I might want to do the same thing still, but with the twist
    that Agents may not understand the Tradegood they own and e.g.
    sell actually valuable minerals as "rocks" or rare herbs as "weeds"
    
    
    
    since I'm doing trading, it pays off to have local models
    of my goods from the perspective of the agent.
    
    That means I can value things on an individual basis and different
    guys will behave differently, but I can still do some statistical
    analysis of it and summ my population up and later restore it."""
    
    def __init__(self,env,agent,name,stock=0,stock_opened=0,inflow=0,outflow=0):
        
        #ok so I have a stock of goods, if I open them
        #I can no longer sell them.
        #it's like "eaten", you're not hungry anymore, 
        #but you can't resell the food
        global_good        = env.goods[name]
        self.env           = env
        self.agent         = agent
        self.name          = name
        self.stock         = stock
        self.stock_opened  = stock_opened
        self.inflow        = inflow
        self.outflow       = outflow
        self.market_price  = global_good.market_price
        self.pov_price     = global_good.market_price
        self.market_orders = {"sell":[],"buy":[]} #"sell_orders","buy_orders","pay with" modes
        self.traded        = False
        self.in_demand     = False #does the agent want this stuff?
        
    def trade(self):
        if self.name in self.env.marketplace["sell_orders"]:
            #get the cheapest:
            best_offer     = self.env.cheapest(self.name)
            if best_offer!=None:
                r=best_offer.accept(self.agent)
                #ok what
                if r:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
                    
    def check(self):
        """check whether I have to do something about this good"""
        #do I have to open anything?
        if self.stock_opened <= self.outflow and self.stock>0:
            self.stock+=(-1)
            self.stock_opened+=1
            
        #should I trade?
        if self.stock < self.outflow*5:
            
            self.trade()
        if self.in_demand:
            self.trade()
        self.stock_opened+=(-self.outflow)
        if self.stock_opened <0 and self.name=="wheat":
            return "dead"
            
    def increase_price(self):
        """someone bought my shit, increase the price"""
        self.pov_price=self.pov_price*1.05
        
    def decrease_price(self):
        """nobody is buying my shit, decrease price"""
        self.pov_price=self.pov_price*0.95

class EconomyAgent:
    """
    single agent
    
    Agents ultimately produce and consume goods and services.
    but in terms of the market, they are mostly interested in valueing
    different thigns against each other, buying, selling, bartering,
    haggling.
    
    They will have externally defined wants and needs and the market
    is the place where they exchange what they have for something
    different that might get them closer to where they want to be in
    terms of planning.
    
    """
    def __init__(self, inventory=None, action_time_cost=None):
        
        self.inventory = inventory#{"wood":{"amount":25}}
        self.offered_goods = {} # keep a separate list from inventory
        self.prices = {}
        self.wanted_goods = {}#{"wheat":{"amount":10}}
        self.fitting_offers = []
        
        self.urgency = {} # how badly do I need this thing?
        # things will never be in wanted and offered at the same time, right?
        # no I can resell stuff. so this should be
        # done per buy and per sell. hm.
        
        
        self.trades = []
        self.action_time_costs = {"walk":0.5,"mill":1,"bake":2,"haggle":0.5,"trade":0.1}
        self.price_reference = {} # some sort of price history, good:price
        self.trade_bases = {} # not sure what this is
        
        #formatted as good.name:action
        self.strategies = {}
        self.dists = []
        
        self.wage = 1
        
        #formatted as good.name:log?
        self.transactions = {}
        self.transaction_log = [] # make it a list for now,
        # in practice I will do database operations with this.
        # so... this list is a temporary holder for objectified data
        # that is actually more table - like.
        
        # this is for comparing general categories and 
        # different products
        self.manufacturing_price_point_cache = {}
        
        # didn't have a positon? what?
        self.pos = (0,0,0)
        
    def __repr__(self):
        return "< econagent "+str(id(self))[-5:]+">"
    
    def scan_market(self,market):
        
        trade_partners=[]
        
        for x in market.traders:
            for g in x.wanted_goods:
                if g in self.offered_goods:
                    if x not in trade_partners:
                        trade_partners.append(x)
                        
        self.potential_barter_trade_partners=trade_partners
    
    def set_up_selling(self,optional_prices=None):
        
        self.prices.update(optional_prices)
        
        no_price_set=[]
        
        for x in self.offered_goods:
            if x not in self.prices:
                no_price_set.append(x)
        
        return no_price_set
                
    
    def depr_consider_trade(self,trade):
        """
        
        
        I need some sort of function for this, although I don't
        think it will work like that."""
                
        good_trade,left_over = trade.depr_value_against(self.market_context)
        
        
    def ensure_d_list(self,env):
        """make sure a location distance list exists."""
        dists = []
        for loc in env.locations:
            loc1 = env.locations[loc]
            
            dists.append((distance(list(loc1.pos)+[0],list(self.pos)+[0]),loc1))
        
        dists.sort(key=lambda x : x[0])
        self.dists = dists
    
    def calc_distance_cost(self,distance):
        
        return self.wage*self.action_time_costs["walk"]*distance
        
    def find_cheapest_seller(self,env,good,amount=None):
        """assome goods are just strings."""
        p_list = []
        
        self.ensure_d_list(env)
        
        for d_loc in self.dists:
            if good in d_loc[1].orders["sell_orders"]:
                p_list += d_loc[1].orders["sell_orders"][good]
                
        p_list.sort(key = lambda x : x.price)
        
        if p_list == []:
            return p_list
        elif amount == None:
            return [p_list[0]]
        else:
            return p_list
                
    def find_closest_market(self):
        return self.dists[0][1]
    
    
    def get_stocks_prices(self,good_recipe,requirements_stocks,env):
        stocks_prices = {}
        for x in good_recipe.requirements:
            if x in requirements_stocks and x in env.avg_prices:
                stocks_prices[x] =  env.avg_prices[x]
            
            elif x in requirements_stocks and x not in env.arg_prices:
                # can't really evaluate it, specify a custom price
                # to assume stuff.
                # and I can't really automate this, which is bad for...
                # AI
                
                if x in custom_set_values:
                    a = 1
                #else:
                # give UI feedback to define some custom prices.
                # or guess.
                
                a = 1
            elif x not in requirements_stocks:
                continue
        return stocks_prices
    
    def get_coverage_relevant_orders(self, env, good_recipe, amount):
        """
        filter my market environemnt for relevant sell orders for ingredients
        for my the recipe and the amount
        """
        all_amount_covered = []
        all_product_amounts_covered = []
        price_point_breaks = []
        relevant_orders = {}
        requirements_cost = 0
        
        for req in good_recipe.requirements:
            product_amount_covered = 0
            cheapest_sellers = self.find_cheapest_seller(env,req.name,amount)
            
            if cheapest_sellers == None:
                continue
                
            elif type(cheapest_sellers) == list:
                # ... I know it's a list of orders and I'm dealing with an amount.
                
                req_target = amount * good_recipe.requirements[req]
                
                req_met = 0
                order_counter = 0
                # while I still need to look things up
                # and there are orders left to do it with.
                while req_met < req_target and order_counter < len(cheapest_sellers):
                    
                    # this is not elegant...? I'm catching that
                    # in the other function and using it as 
                    # a break condition if it stays None
                    next_price = None
                    
                    my_order = cheapest_sellers[order_counter]
                    if order_counter +1 < len(cheapest_sellers):
                        next_order = cheapest_sellers[order_counter+1]
                        # ...and isn't overwritten here.
                        next_price = next_order.price
                        
                    # if I'm below the limit...
                    if my_order.amount + req_met < req_target:
                        req_met += my_order.amount
                        amount_I_can_cover = req_met /  good_recipe.requirements[req]
                        
                        requirements_cost += my_order.price * my_order.amount
                        
                        break_point = (amount_I_can_cover, req, next_price)
                        price_point_breaks.append(break_point)
                        
                    else:
                        missing_amount = req_target - req_met
                        amount_I_can_cover = amount
                        
                        requirements_cost += my_order.price * missing_amount
                        
                        break_point = (amount_I_can_cover, req, next_price)
                        price_point_breaks.append(break_point)
                        
                    order_counter += 1
                
                product_amount_covered = req_met / good_recipe.requirements[req]
                all_product_amounts_covered.append(product_amount_covered)
                
            relevant_orders[req.name] = cheapest_sellers
        
        price_point_breaks.sort(key= lambda x :x[0])
                
        return all_amount_covered, all_product_amounts_covered, price_point_breaks, relevant_orders, requirements_cost
        
    def find_manufacturing_cost(self, env, good_recipe, amount = 1, requirements_stocks = None, custom_set_values = None):
        """
        This is a function, that wants to phrase manufacturing costs
        according to inputs like sell orders.
        
        The output are a final price, and a list of
        "Manufacturing price points" that return 
        how many of the product can be at a certain price
        and volume.
        
        e.g. 
        
        the first  5 for 2
        the next   5 for 2.5
        
        so if you want 10, it will cost 5*2 + 5*2.5 =  10+12.25
        
        22.25/10 = 2.225 average
        
        If you want 5, it will cost 5*2 = 10
        
        10/5 = 2 average.
        
        Does this have a false?
        """
        make_p, manufacturing_price_points, amount_covered = 0,[],0
        #for requirements
        if requirements_stocks == None:
            requirements_stocks = {} # init to empty.
            
        requirements_cost = 0
        
        stocks_prices  = self.get_stocks_prices(good_recipe, requirements_stocks, env)
        
        # whenever 
        output = self.get_coverage_relevant_orders(env, good_recipe, amount)
        
        if output == None:
            return make_p, manufacturing_price_points, amount_covered
        
        all_amount_covered, all_product_amounts_covered, price_point_breaks, relevant_orders, requirements_cost = output
        
        manufacturing_price_points = self.get_manufacturing_price_points(output, good_recipe, amount)
        
        if len(all_product_amounts_covered) > 0:
            amount_covered = min(all_product_amounts_covered)
        else:
            amount_covered = 0
        
        
        
        # the cost is probably wrong.
        total_cost = requirements_cost + good_recipe.make_process_cost
        
        total_cost = self.calculate_cost_from_price_points(manufacturing_price_points, amount)
    
        return total_cost, manufacturing_price_points, amount_covered
    
    def calculate_cost_from_price_points(self, manufacturing_price_points, amount):
        
        counter = 0
        m_amount_covered = 0
        total_price = 0
        other_m = len(manufacturing_price_points)
        
        while m_amount_covered < amount and counter < other_m:
            my_object = manufacturing_price_points[counter]
            
            if ( m_amount_covered  + my_object.amount ) > amount:
                r_amount = amount - m_amount_covered 
            else:
                r_amount = my_object.amount
            total_price += my_object.price * r_amount
            m_amount_covered += my_object.amount
            counter += 1
        
        return total_price
    
    def get_manufacturing_price_points(self,coverage_output,good_recipe,amount):
        """
        the point of this function is to create an equivalent to market orders, for manufacturing.
        
        so "I can make n objects for x money"
        
        I'm doing this by reusing the inputs from the market orders to
        get the prices for the ingredients and at any point where any
        ingredient market order volume ends, I'm inheriting that
        into my manufacturing price points
        
        ingredients volumes with prices:
        |-|---|-|
        |--|-|--|
        
        product volumes with prices:
        |-||-||-|
        
        """
        all_amount_covered, all_product_amounts_covered, price_point_breaks, relevant_orders, requirements_cost = coverage_output
        manufacturing_price_points = []
        
        for req in good_recipe.requirements:
            if req.name not in relevant_orders:
                return []
            elif len(relevant_orders[req.name])==0:
                return []
        
        if amount > 1:
            base_price = 0
            prices = {}
            total_number = 0
            
            # so I have a price dict.
            # and I'm updating the price dict. at the breakpoints.
            
            for req in good_recipe.requirements:
                price = relevant_orders[req.name][0].price
                prices[req] = price * good_recipe.requirements[req]
            
            old_number = 0
                        
            for break_point in price_point_breaks:
                
                (new_number, req, next_price) = break_point
                product_diff = new_number - old_number
                
                if product_diff == 0:
                    prices[req] = next_price
                    continue
                
                old_number = new_number
                price = 0
                for ingredient_name in prices:
                    price += prices[ingredient_name] * good_recipe.requirements[ingredient_name]
                                
                MPP = ManufacturingPricePoint(price,product_diff,recipe=good_recipe)
                manufacturing_price_points.append(MPP)
                prices[req] = next_price
                
                total_number += product_diff
                if total_number > amount:
                    break
                if next_price == None:
                    break
        
        return manufacturing_price_points
    
    def tick_strategies(self,strat):
        for goodname in strat:
            #does it exist
            if goodname in self.strategies:
                #has it changed
                if strat[goodname]==self.strategies[goodname]:
                    return False
                else:
                    self.strategies.update(strat)
                    return True
            else:
                self.strategies.update(strat)
                return True
    
    def sum_difference_from_transactions(self):
        my_dict = {}
        for T in self.transaction_log:
            
            if T.good_a not in my_dict:
                my_dict[T.good_a] = 0
            if T.good_b not in my_dict:
                my_dict[T.good_b] = 0
            
            if T.party_a == self:
                my_dict[T.good_a] += T.amount_a
                my_dict[T.good_b] -= T.amount_b
                
            else:
                my_dict[T.good_a] -= T.amount_a
                my_dict[T.good_b] += T.amount_b
        
        return my_dict
    
    def interact_with(self,trader):
        """
        this is already figuring out good we can exchange.
        """
        s1 = set(trader.offered_goods.keys())
        s2 = set(self.wanted_goods.keys())
        
        # record the time to view everything
        
        time1 = len(trader.offered_goods)
        keys = s1.intersection(s2)
        
        payment_time = 0
        pay_i_time = 1
        for key in keys:
            if key not in trader.prices:
                raise ValueError
            
            payment, trade_amount = self.automatic_transaction(trader,key)
            self.wanted_goods[key]["amount"] -= trade_amount
            
            if self.wanted_goods[key]["amount"] <= 0:
                self.wanted_goods.pop(key)
            
            payment_time += pay_i_time

    def automatic_transaction(self,trader,key):
        """
        for a given good key, this function figures
        out maximum transfer and executes it.
        
        don't mess with it, it works exactly as intended.
        
        it is easier to adapt the inventory structure and reuse the same
        structure than to change these functions.
        """
        payment, trade_amount = self.figure_out_payment_and_amount(trader,key)
        self.perform_buy_from_transaction(trader,key,payment, trade_amount)
        
        return payment, trade_amount
    
    def figure_out_payment_and_amount(self,trader,key):
        trade_amount = 0
        payment = 0
        trade_amount = self.wanted_goods[key]["amount"]
        
        if trader.offered_goods[key]["amount"] < self.wanted_goods[key]["amount"]:
            trade_amount = trader.offered_goods[key]["amount"]
            
        if self.inventory["money"]["amount"] < self.wanted_goods[key]["amount"]*trader.prices[key]:
            trade_amount = self.inventory["money"]["amount"].__floodiv__(trader.prices[key])
            
        payment = trade_amount * trader.prices[key]
        return payment, trade_amount
        
    def perform_buy_from_transaction(self,trader,key,payment,trade_amount=1,exchange_good="money"):
        """
        the idea is that a player or agent approaches a trader
        and manually creates a transaction via the UI and then this
        function performs the exchange of material and currency.
        """
        
        if key not in trader.inventory:
            return False
        if exchange_good not in self.inventory:
            return False
        
        if trade_amount > trader.inventory[key]["amount"]:
            return False
        if payment > self.inventory[exchange_good]["amount"]:
            return False
            
        trader.inventory[key]["amount"]-=trade_amount
        if key not in self.inventory:
            self.inventory[key] = {"amount":0}
        self.inventory[key]["amount"]+=trade_amount
        
        if exchange_good not in trader.inventory:
            trader.inventory[exchange_good] = {"amount":0}
        trader.inventory[exchange_good]["amount"]+=payment
        self.inventory[exchange_good]["amount"]-=payment
        
        T_ob = Transaction("now",key,trade_amount,exchange_good,payment,self,trader)
        
        self.transaction_log.append(T_ob)
        trader.transaction_log.append(T_ob)
        
        return T_ob
        

    def market_interaction(self,M):
        """
        this is (at least for shops and stalls, because
        that's what I'm testing for in the test.
        """
        
        for trader in M.traders:
            self.interact_with(trader)
        
        M.customer_order_interaction(self,sell_orders=True)
        M.customer_order_interaction(self,sell_orders=False)
        
        M.let_pick_up(self)
        
        return 
    
    
    def make_or_buy(self, env, good_recipe, amount = 1, historical_price_data = None):
        """
        Ok, so actually, I would prefer to build a flow chart
        put weights and costs on there and evaluate whether
        to make or buy from that. This here probably works, but... eh...
        
        I want to figure whether it's cheaper to buy or to make them
        and at which points, for which quantities.
        
        ...(in a given area / environment,)
        
        for a specific object / crafting recipe
        
        (TODO) and taking into account historical pricing data or not.
        """
        
        # hm this is where I need to apply astar somewhere.
        # or is it...
        
        self.ensure_d_list(env)
        
        # the price list can be not correct
        # because it only represents what is available not
        # what you can actually do,
        # so a historical list of prices that was actually achieved
        # is preferable.
        
        price_list = []
        if amount == None:
            buy_p = self.find_cheapest_seller(env, good_recipe.name)
        else:
            price_list = self.find_cheapest_seller(env,good_recipe.name,amount)
            
        r = self.find_manufacturing_cost(env, good_recipe, amount)
        
        make_p, manufacturing_price_points, amount_covered = r 
        
        self.manufacturing_price_point_cache[good_recipe.name] = manufacturing_price_points
                
        amount_bought = 0
        amount_made = 0
        
        total_buy_cost = 0
        total_make_cost = 0
        
        my_amount_covered = 0
        sale_offer_index = 0
        
        manufacturing_price_point_index = 0
        can_manufacture = manufacturing_price_point_index < len( manufacturing_price_points)
        can_buy = sale_offer_index < len(price_list)
        
        while (amount_bought + amount_made) < amount and (can_buy or can_manufacture):
            
            # as long as I can do both, I want to compare
            # and figure out the optimal solution.
            # (...)
                        
            if (can_manufacture and can_buy):
                sale_offer = price_list[sale_offer_index]
                price_point = manufacturing_price_points[manufacturing_price_point_index]
                
                if sale_offer.price < price_point.price and can_buy:
                    amount_bought += sale_offer.amount
                    total_buy_cost += sale_offer.price * sale_offer.amount
                    sale_offer_index += 1
                
                elif sale_offer.price > price_point.price and can_manufacture:
                    amount_made += price_point.amount
                    
                    total_make_cost += price_point.price * price_point.amount
                    
                    manufacturing_price_point_index += 1
                
                can_manufacture = manufacturing_price_point_index < len( manufacturing_price_points)
                can_buy = sale_offer_index < len(price_list)
            
                continue
            
            # (...) and that loop part is up there.
            
            # (...) and if I can't compare them anymore,
            # because I have run out of either the option to buy the
            # material and make it
            # or because I have run out of options to buy it
            # I have no other choice, but to just add this stuff.
            
            if can_buy:
                sale_offer = price_list[sale_offer_index]
                amount_bought += sale_offer.amount
                total_buy_cost += sale_offer.amount * sale_offer.price
                sale_offer_index += 1
                can_buy = sale_offer_index < len(price_list)
                continue
            
            if can_manufacture:
                price_point = manufacturing_price_points[manufacturing_price_point_index]
                amount_made += price_point.amount
                total_make_cost += price_point.price * price_point.amount
                manufacturing_price_point_index += 1
                can_manufacture = manufacturing_price_point_index < len( manufacturing_price_points)
                continue
        
        if amount_bought + amount_made >= amount:
            # I'm good
            a = 1
        
        else:
            # I should give feedback that it didn't work?
            a = 1
        
        output_dict = {"make":{"total cost":total_make_cost,"amount":amount_made},
                        "buy":{"total price":total_buy_cost,"amount":amount_bought},
                        }
        
        return output_dict
    
    def buy(self,good,price):
        """this is causing sideeffects"""
        m=self.find_closest_market()
        O=order(good.name,price*0.9,10)
        m.put_order(O,True,self)
        
    def sell(self,good,make_p):
        """this is causing sideeffects"""
        m=self.find_closest_market()
        O=order(good,make_p*1.10,10)
        m.put_order(O,False,self)
        
            
class Market:
    """
    location where structured trading is done by agents.
    
    This can take different forms:
    * Agents putting up stalls selling goods directly
    * Agents acting as traders/aggregators and "small supermarkets"
    * Markets can be structured places for bartering
    * or be the location for more modern forms of abstractions of trade:
    orders, options, bundled objects.
    
    For the purpose of the economics of it, it's a mostly immaterial place
    real world restrictions slightly influence behavior.
    
    Agents propose Trades of Tradegoods
    Agents accept Trades creating a Transaction
    Agents can put up Orders, accepted by other Agents acting as brokers
    Agents can fulfill Orders, creating a Transaction
    
    Records can be created for each tradegood
    for each actor, for each market and for the system as a whole.
    
    The market should be abstracted to an agent in some cases.
    I want to be able to treat it as a single actor that I can just
    buy from in bulk at some prices and volume.
    
     
    """
    def __init__(self,pos=(0,0,0),shape=None):
        
        #this is something I should not do here later...
        #like, this is just for testing, later I will have locations
        #that will have a market and I can pathfind to them that way.
        #self.physical_properties = {"pos":}
        
        self.id = str(uuid.uuid4())
        
        self.pos = pos
        self.shape = shape
        #do I still need this? probably...
        
        self.traders = []
        self.goods = {}
        self.price_data= {"banana":{
                            "avg_price":4,
                            "buyprice":2,
                            "sellprice":6,
                            "averagevolume":1},
                        "apple":{
                            "avg_price":1,
                            "buyprice":0.5,
                            "sellprice":1.5,
                            "averagevolume":20}}
        # because of the nature of how this is, it makes more sense
        # to keep the data in a nested dictionary than to create
        # custom objects or attributes.
        
        self.orders = {"sell_orders":{},"buy_orders":{}}#this is where offers go...
        
        
        # the market actually need an inventory
        # for the orders.
        self.inventory ={}
        
        # I could also structure it by goods...
        # fuck I'm not sure what's superior. let's create a flip function
        # that can invert on demand.
        
        # if trades where completed on behalf of someone else,
        # this is where the new owners can collect their respective goods
        
        # "owner":"object"
        self.pickup_area = []
        
        self.transactions = []
        
        
        # let's pretend the market is actually an actor with
        # fixed prices and volumes that you can just buy from.
        
        self.fake_actor = None
    
    def __repr__(self):
        return "< econmarket >"
    
    def set_up_trader(self,trader):
        self.traders.append(trader)
    
    def flip_order_data_structure(self):
        
        goods = {}
        
        for g in self.orders["sell_orders"]:
            if g not in goods:
                goods[g] = {}
            goods[g]["sell_orders"] = self.orders["sell_orders"][g]
        
        for g in self.orders["buy_orders"]:
            if g not in goods:
                goods[g] = {}
            goods[g]["buy_orders"] = self.orders["buy_orders"][g]
        
        return goods
    
    def resolve_barter_trade(self):
        
        for x in self.traders:
            x.scan_market(self)
            for g in x.wanted_goods:
                if g not in x.urgency:
                    x.urgency[g]=1 
        
        c=0
        m=10
        while c < m:
            # I take the perspective of x, x2 is the other guy
            
            offer_for = self.make_barter_offers()
            self.process_barter_offers(offer_for)
            
            for x in self.traders:
                x.scan_market(self)
                for g in x.wanted_goods:
                    if g in x.urgency:
                        x.urgency[g]+=1
                    else:
                        x.urgency.pop(g)
                
            # and I want to break when every has gotten what they want
            # or there is only one trader left.
            # or the time limit is reached.
            c+=1
    
    def process_barter_offers(self, offer_for):
        for x in self.traders:
            if x in offer_for:
                for offer in offer_for[x]:
                    
                    traders = list(offer.keys())
                    traders.remove(x)
                    other = traders[0]
                    all_good=True
                    for g in offer[x]:
                        if g not in x.offered_goods:
                            all_good=False
                            break
                    for g in offer[other]:
                        if g not in other.offered_goods:
                            all_good=False
                    
                    if not all_good:
                        continue
                    
                    # ok, reconstruct the prices, same method.
                    
                    # this is what you give.
                    
                    giving_value = 0
                    for g in offer[x]:
                        old_price = x.price_reference[g]
                        amount = offer[x][g]
                        good_price = old_price*amount
                        giving_value += good_price
                        
                    # this is what you get. If full other is bigger
                    # than full_price, that's good.
                    
                    #full_price *= (0.5 + 0.1*combined_urgency**2)
                    combined_urgency = 0
                    getting_value = 0
                    for g in offer[other]:
                        old_price = x.price_reference[g]
                        amount = offer[other][g]
                        good_price = old_price*amount
                        getting_value += old_price*amount
                        combined_urgency += x.urgency[g] * good_price
                    
                    # right, how much 
                    combined_urgency = combined_urgency / getting_value
                    
                    getting_value*=1.1**combined_urgency
                    # and I don't want to reduce this, I think?
                    # I want to reduce *mine* because it's a direct trade
                    # and if I give *less* that's better for me.
                    
                    
                    # another option would be to scale down what
                    # i'm getting so I'm not getting more than I want.
                    
                    if getting_value > giving_value :
                        # accept and make the trade
                        perform_direct_barter_trade(x,other,offer)
                    else:
                        
                        # up the urgency, go into the next loop to make a counter offer.
                        
                        # verify that the traders are still valid
                        # If one offer gets accepted
                        # that can invalidate a lot of offers.
                        # this is also something that makes trading in barter
                        # economies really inefficient.
                        # I can up the time cost that's required to negotiate
                        a = 1
            
    def make_barter_offers(self):
        offer_for ={}
        for x in self.traders:
            for x2 in x.potential_barter_trade_partners:
                # so, both parties have an expected "old price"
                # that they will reference for both parts.
                
                # bartering is about offering a high price when selling
                # and offering a low price when buying
                # and then approaching each other.
                
                # and I need to always ensure both parties have the quantities.
                
                # so, fetch something I want. make a virtual price
                # for what x thinks it's worth.
                full_price = 0
                trade_offer={x:{},x2:{}} # and then {good:amount}
                combined_urgency = 0
                for g in x.wanted_goods:
                    if g in x2.offered_goods:
                        amount = x.wanted_goods[g]["amount"]
                        old_price = x.price_reference[g]
                        # this is my reference price.
                        good_price = amount * old_price
                        full_price += good_price
                        trade_offer[x2][g] = amount
                        combined_urgency = x.urgency[g] * good_price
                        
                
                # that should be doing it right?
                combined_urgency = combined_urgency / full_price
                
                # and I want to make the other guy an offer, that's
                # 0.5 or than that, from my perspective. and then increase over time.
                # so the "full price" of my goods is fake low.
                
                #fac = (10*0.9**combined_urgency)
                
                full_price *= (0.5+0.1*combined_urgency)
                
                for g in x.offered_goods:
                    if g in x2.wanted_goods:
                        # something to limit the maximum value?
                        
                        # get something the other guy wants.
                        # calculate how many that is.
                        old_price = x.price_reference[g]
                        amount = full_price.__floordiv__(old_price)+1
                        
                        if amount < x.offered_goods[g]["amount"]:
                            # single good can compensate for all wants
                            # trade.
                            trade_offer[x][g] = amount
                            break
                        else:
                            # all I have
                            # set the offer to x
                            trade_offer[x][g] = x.offered_goods[g]["amount"]
                            
                            # reduce my fake price by 
                            full_price -= amount * old_price
                            if full_price < 0:
                                break
                            # math.
                            a=1
                
                if x2 not in offer_for:
                    offer_for[x2]=[]
                offer_for[x2].append(trade_offer)
        
        return offer_for
    
    def put_order(self,order,owner,sell=True,verbose=False):
        
        order.location = self
        
        if sell:
            key="sell_orders"
            deposit_type = order.good
            deposit_amount = order.amount
        else:
            key = "buy_orders"
            deposit_type = "money"
            deposit_amount = order.amount * order.price
        
        # if you don't have enough, you can't "file" the order
        if owner.inventory[deposit_type]["amount"] < deposit_amount:
            return
        
        # else take from owner, put into market.
        owner.inventory[deposit_type]["amount"] -= deposit_amount
        if deposit_type not in self.inventory:
            self.inventory[deposit_type]={"amount":0}
        self.inventory[deposit_type]["amount"] += deposit_amount
                
        if order.good not in self.orders[key]:
            self.orders[key][order.good]=[]
            
        self.orders[key][order.good].append(order)
        self.orders[key][order.good].sort(key = lambda x : x.price, reverse=(not sell))
        
    def resolve(self):
        
        #ok check for overlap between sell orders and buy orders
        
        sell_goods = self.orders["sell_orders"].keys()
        buy_goods = self.orders["buy_orders"].keys()
        sell_goods = set(sell_goods)
        buy_goods = set(buy_goods)
        good_intersection = sell_goods.intersection(buy_goods)
        
        for gkey in good_intersection:
            #there can be lists of orders. 
            #and they can change, so...
            while True:
                #are there orders that can be filled?
                lowest_sell=self.orders["sell_orders"][gkey][0].price
                highest_buy=self.orders["buy_orders"][gkey][0].price
                
                #ok, if the buy price is higher than the sell price...
                if lowest_sell <= highest_buy:
                    #sale!
                    s=self.orders["sell_orders"][gkey][0]
                    b=self.orders["buy_orders"][gkey][0]
                    buy_amount=None
                    sell_money=None
                    if b.amount <= s.amount:
                        self.orders["buy_orders"][gkey].pop(0)
                        s.amount-=b.amount
                        
                        if b.amount == s.amount:
                            self.orders["sell_orders"][gkey].pop(0)
                        
                        #order owner gets goods
                        #sell gets some money
                        sell_money=b.amount*b.price
                        buy_amount=b.amount
                        
                    #if b.amount == s.amount:
                        #self.orders["buy_orders"][gkey].pop(0)
                        #self.orders["sell_orders"][gkey].pop(0)
                        
                        #sell_money=b.amount*b.price
                        #buy_amount=b.amount
                        
                    if b.amount > s.amount:
                        self.orders["sell_orders"][gkey].pop(0)
                        b.amount -= s.amount
                        sell_money=s.amount*b.price
                        buy_amount=s.amount
                    
                    #seller of the sell order gets sell_money
                    #buyer gets buy_amount
                    
                    buyer=self.order_owner_map.pop(b)
                    #buyer .give stuff
                    
                    seller=self.order_owner_map.pop(s)
                    #seller .give money
                else:
                    break
    
    def customer_order_interaction(self,customer,sell_orders=True,verbose=False):
        """the key is to not think about the orders as sell or buy
        there is always a "sell" happening, the difference is
        who buyer and seller are.
        
        The market takes the role of whoever can't be there.
        But acts 100% as intermediary, goods exchange end up in the
        markets inventory and then get transfered.
        """
        if sell_orders:
            personal_goods = customer.wanted_goods
            key = "sell_orders"
            buyer = customer
            seller = self
        else:
            personal_goods = customer.offered_goods
            key = "buy_orders"
            seller = customer
            buyer = self
        
        for good in personal_goods:
            if  good in self.orders[key]:
                # should I assume they're sorted? Sure.
                # cheapest sell order, highest buy order should be top
                
                # while I want to buy or sell things.
                while personal_goods[good]["amount"] > 0 :
                    
                    if good not in self.orders[key]:
                        break
                    
                    if sell_orders:
                        offered_good = "money"
                        received_good = good
                        
                    else:
                        offered_good = good
                        received_good = "money"
                    
                    if customer.inventory[offered_good]["amount"] <= 0:
                        break
                    
                    best_order = self.orders[key][good][0]
                    trade_amount = personal_goods[good]["amount"]
                    
                    # if the order allows me to interact with it.
                    if trade_amount > best_order.minimum_amount:
                        
                        # cap the trade amount to how much money is
                        # available and how much is remaining in the order.
                        if trade_amount * best_order.price > buyer.inventory["money"]["amount"]:
                            trade_amount = buyer.inventory["money"]["amount"].__floordiv__(best_order.price)
                            
                        if trade_amount > best_order.amount:
                            trade_amount = best_order.amount
                        
                        payment = trade_amount * best_order.price 
                        
                        if "money" not in seller.inventory:
                            seller.inventory["money"]={"amount":0}
                        if good not in buyer.inventory:
                            buyer.inventory[good]={"amount":0}
                        
                        buyer.inventory["money"]["amount"] -= payment
                        seller.inventory["money"]["amount"] += payment
                        
                        buyer.inventory[good]["amount"] += trade_amount
                        seller.inventory[good]["amount"] -= trade_amount
                        
                        # reduce the amount so that the loop will eventually end.
                        personal_goods[good]["amount"]-=trade_amount
                        best_order.amount -= trade_amount
                        
                        M_t={"good":good,"buyer":buyer,"seller":seller,"amount":trade_amount,"price":best_order.price}
                        
                        self.transactions.append(M_t)
                        if sell_orders:
                            self.pickup_area.append([best_order.creator,"money",payment])
                        else:
                            self.pickup_area.append([best_order.creator,good,trade_amount])
                        
                        if self.orders[key][good][0].amount==0:
                            self.orders[key][good].pop(0)
                            if len(self.orders[key][good])==0:
                                self.orders[key].pop(good)
                        
     
    def let_pick_up(self,customer):
        
        rml=[]
        for my_list in self.pickup_area:
            customerx,thing,amount = my_list
            if customerx == customer:
                if thing not in customer.inventory:
                    customer.inventory[thing]={"amount":0}
                customer.inventory[thing]["amount"]+=amount
                rml.append(my_list)
        for x in rml:
            self.pickup_area.remove(x)
                
    def make_abstracted_actor(self):
        
        self.fake_actor =  EconomyAgent()
        
    
    
    def calculate_price_on_market(self,date=None,name=None):
        """if name is None, do it for everything.
        
        maybe date should be a date range
        
        if date is none, do it for all transactions on record.
        """
        
        prices = {}
        
        transactions=[]
        for x in transactions:
            
            # if it's through barter trade...
            # hmmm I would have to get some kind of 
            # external evaluation... sum of one side, sum of other side
            
            # if it's a sell order
            # or if it's a buy order
            
            # multiply by volume, 
            
            if x.good.name not in prices:
                prices[x.good.name]={"transactions":[]}
            prices[x.good.name]["transactions"].append(x.amount,x.price)
        
        for good_name in prices:
            
            prices[good_name]["sum_volume"]=0
            for transaction in prices[good_name]["transactions"]:
                prices[good_name]["sum_volume"]+=transaction.amount
            
            prices[good_name]["avg_price"]=0
            for transaction in prices[good_name]["transactions"]:
                frac_amount = transaction.amount/prices[good_name]["sum_volume"]
                prices[good_name]["avg_price"]+=frac_amount * transaction.price
        return prices
    
class EconomyEnvironment:
    """ biggest thing.
    
    contains markets as well as agents.
    
    serves as basic "container system" for markets to exist and 
    agents to move around in.
    """
    
    def __init__(self):
        
        #ok, so this solves *what* to do,
        #it doesn't solve when or how to do it.
        
        self.locations = {} # trading places can be in cities,
        # but they don't have to be .
        self.agents = []
        self.cities = {}
        
        
                    
    def add_locations(self,num=5):
        #this is just for testing
        c=0
        while c < num:
            self.locations.update({c:Market()})
            c+=1
    
    def main_tick(self,external_time_object,input_d={"sim agents":True,"sim_locations":True},):
        
        ret_d={}
        if "create default goods" in input_d:
            
            # I think I have some crafting data somewhere else.
            # I could/should reuse that.            
            
            self.goods={}
            
            self.goods.update({"water":good("water",0.1)})
            self.goods.update({"wheat":good("wheat",1)})
            self.goods.update({"flour":good("flour",3)})
            self.goods.update({"bread":good("bread",35)})
            
            # this is crafting stuff and doesn't really belong here.
            # maybe as a shortcut.
            # probably as an output from other considerations.
            self.goods["flour"].requirements=["wheat"]
            self.goods["flour"].make_process_cost=0.1
            self.goods["bread"].requirements=["flour","water"]
            self.goods["bread"].make_process_cost=0.5
            
        if "create locations" in input_d:
            ids = input_d["create locations"]
            for id in ids:
                if id not in self.locations:
                    self.locations.update({id:Market()})
                
        if "create agents" in input_d:
            l=[]
            for id in input_d["create agents"]:
                self.agents.append(EconAgent(id))
                l.append(id)
            ret_d.update({"agents created":l})
        
        if "sim agents" in input_d:
            agent_d={}
            for a in self.agents:
                r=a.live(self)
                if r!={}:
                    agent_d.update({a.id:r})
            if agent_d!={}:
                ret_d.update({"agent_d":agent_d})
        
        if "sim locations":
            for m in self.locations:
                r=self.locations[m].resolve()
                if r!=None:
                    ret_d.update({"econ location result":r})
            
        if ret_d=={}:
            return None
        return ret_d
    
def get_basic_resources():
    l = {"field":"grain","forest":"wood","rocks":"stone","mine":"iron"}

def get_basic_buildings():
    #I can just spawn bigger rectangles
    #there should be a circle bigger than
    l = {"mill":{"purpose":"workstation"},
        "forge":{"purpose":"workstation"},
        "warehouse":{"purpose":"storage","capacity":80},
        }


def distance(p1,p2):
    """the euclidian distance between two points"""
    
    x = (p1[0]-p2[0])**2
    y = (p1[1]-p2[1])**2
    z = (p1[2]-p2[2])**2
    
    d = (x+y+z)**0.5
    
    return d

if __name__=="__main__":
     test_bartering()
     test1()
