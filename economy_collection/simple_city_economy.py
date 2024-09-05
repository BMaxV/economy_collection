from generalcybernetics import basis
from economy_collection import crafting
from economy_collection import economy

import uuid

class city:
    """
    in terms of big picture economics.
    
    cites
    
    -consume food and resources
    -except ore, it's realistic that a city is build on top or near
    valuable minerals.
    -convert the resources into various products
    -this can be artisinal or industrial
    -there is a service industry
    -the economic situation is much more complex than in the country side
    
    
    crime can be extortion/robbery, but it can also become more
    complex due to politics.
    
    I should take a look where I put my city, crime curve.
    
    ----
    
    in terms of big picture economics:
    
    villages:
    
    produce people and area dependant resources, like
    -agricultural products
    -resources and things from woodland areas
    -fish from the ocean, rivers or lakes
    -mining although that's probably rare, a valuable mining resource
    will quickly transform the village into a city.
    
    -weaker defenses
    -less wealth
    
    there are some established differences, I think 2500 people or something
    where a village / "town" officially becomes a proper city.
    
    they will be the territory of some lord
    the land can either be owned by the lord directly, or there
    can be a deal between the peasants and the lord. especially when
    areas are supposed to be settled, it's a much more enticing deal
    to offer ownership of the land.
    
    crime takes the shape of direct extortion/robbery.
    
    I could hide the...
    stocks, production, cost, etc. a bit and make people host their
    own websites to publish the info, on github pages, codeberg, etc..
    Heck, if things get off the ground I can do it myself.
    
    """
    
    def __init__(self,location,resources = None,population = 0,special_jobs={},inventory=None):
        
        self.id = str(uuid.uuid4())
        
        self.cyber = basis.Element()
        self.cyber.payload = self
        
        self.econ_agent = economy.EconomyAgent()
        self.econ_agent.pos = location
        
        self.pos = location
        self.population = population
        if resources == None:
            self.resources = {} # let's do this as {"name":x,"available":number,"used":number}
        else:
            self.resources = resources
        
        if inventory == None:
            self.inventory = {}
        
        # I should probably just use the crafting recipies here.
        
        # this is actually stuff that belongs in a different object.
        # like a "production location".
        self.production = {} # produced stuff 
        self.production_plan = {}
        self.raw_materials_required = {}
        
        
        self.inventory = inventory # goes here
        self.consumption = {} # this is what is being subtracted.
        
        # this will be collection of recipes owned by the citizens.
        # or rather, "in memory"
        # some of them will last a long time and be more common
        # but I also want some of them to be lost.
        
        # this kind of needs an information awareness management system
        self.recipes = {}
        
        
        
        self.professionals_statistic = {}
        # hm, the stellaris model of abstracted jobs is probably a really good idea.
        
        # this doesn't just apply to an individual, it becomes
        # mass behavior / statistical and works for the entire city.
        self.economic_plans = {"basic":["make","sell","buy","fulfill need"],}
    
    def get_recipes(self):
        for x in self.named_population:
            person = self.named_population[x]
            self.recipes.update(person.recipes)
    
    def init_statistics(self):
        """all of these will be statistical distributions"""
        self.general_statistics={
            "age":None,
            "wealth":None,}

        self.job_statistics = {
            "skill":None,
            "education rate":None, # just because people have skills doesn't mean they're sharing. just means that they CAN.
            }
            
        self.political_statistics = {
            "autonomy":None, # do they leave you alone?
            "corruption":None, # serving selfish or local industrial interests over the interests of the central government, the law, the kingdom, the king, etc..
            "taxation":None,
            "secession desire":None, # if you're doing better than the capital and the central government doesn't help you, why stay?
            } 

        self.citizen_happiness_statistics = { # I could do these across wealth groups, not pops.
            "housing":None,
            "food":None,
            "job stress":None, # how much work.
            "security":None, # ...from street crime, gangs, extortion, injustice from nobles?
            "disaster stress":None, # epidemics, big fires, war, etc.. stuff you want to prevent to run things well.
            #"justice":None, ?
            
            }

        
    
    
    def secession_desire_tick(self):
        
        # why would you want to secede?
        
        # effectively independent
        # well organized
        # taxed / subjected to "bad" laws.
        # additional pressure from events
        # lack of support from central power to solve *pressing* problems
        
        # -> let's do it ourselves.
        
        a = 1
    
    def corruption_tick(self):
        
        # there is a rule / command
        # but I can bend the rule to shave a few percent off
        # and nobody will notice or punish it.
        
        # plus a little bit of greed, morally deviant behavior.
        
        # but ALSO as a counter point to bad buerocracy that overcomplicates things
        # some shortcuts are mutually and universally beneficial.
        # there is a balance.
        
        # burocracy can be intentionally created to create "space" for corruption to happen.
        
        # "opportunities make thieves"
        
        # if there is no control / oversight, it is easier to slip down the slope of thinking, "nobody cares" and "nobody will notice".
        
        a = 1
    
    def consumption_tick(self):
        for key in self.consumption:
            
            # hmmmmmm. this needs the group thing again
            # and it might be wise to integrate the rest of
            # the planning into my consumption plan
            # and then do a double check.
            # building a new dict here for specific amounts and goods
            # and reducing my plan according to the items I picked.
            
            # so, "bread" would tick down "food" and 
            # but tick up my actual consumtion
            # and then I would subtract from my inventory.
            
            self.inventory[key]["amount"] -= self.consumption[key]["amount"]
        
    def consumption_planning(self):
        """
        the consumption over here is reliable, this will be consumed
        at the end of the tick.
        """
        self.consumption["Food"] = {"amount" : self.population}
        self.consumption["Consumer Goods"] = {"amount" : self.population}
    
    def find_possible_products(self):
        possible_products = set()
        if unknown_name in crafting.groups:
            
            groupname = unknown_name
            all_group_members = set(crafting.groups[groupname])
            know_how = set(self.recipes.keys())
            
            possible_products = all_group_members.intersection(know_how)
            
            this_group_list = [groupname] + list(all_group_members)
            compare_groups[groupname] = this_group_list
            
            if len(possible_products) == 0:
                know_how_d[groupname] = False
                continue
            else:
                know_how_d[groupname] = True
                for productname in possible_products:
                    know_how_d[productname] = True
                            
        else:
            product_name = unknown_name
            if product_name not in self.recipes:
                know_how_d[product_name]=False
            else:
                possible_products = set()
                possible_products.add(product_name)
        
        return possible_products, know_how_d
    
        
        # these are not the same.
    def production_planning(self,economic_environment=None):
        
        self.planned_raw_material = {}
        self.planned_production_output = {}
        # do i do replacement?
        for x in self.resources:
            self.planned_raw_material[x] = self.resources[x]["occupied"]
        
        production_plan = {}
        buy_plan = {}
        know_how_d = {}
        
        
        # this requires a little bit more thinking about...
        # groups and categories.
        
        # so, if I need any one thing from group x
        # any one thing from group x should meet the need.
        # and tick my box.
        
        
        
        # so these are groups, actually, not specific things.
        # and actually I need to figure which products that I can
        # make, meet the needs that I have.
        
        compare_list = []
        compare_groups = {}
        for unknown_name in self.consumption:
            # this is multilayered, I shouldn't do this when I build
            # the basic steps.
            # so, I shouldn't consume "Food" I should consume "Bread", because that fits better with my 
            # setup for crafting right now.
            # "Food" is the statistic generalization?... 
            
            # but I can't switch if I do that.
            
            # this feels like overthinking.
            # this needs to be more complicated in the future, but
            # not right now.
            possible_products, know_how_d = self.find_possible_products()
            
        
            # ok, so with groups and specific stuff, 
            
            # so what I actually want is to test my needs against all 
            # possible options that could meet it and then pick the cheapest.
            # or otherwise best via a different evaluation function
            # or metric.
            
            fake_needs = {}
            for group_name in crafting.groups:
                if group_name in self.consumption:
                    for product_name in crafting.groups[group_name]:
                        if product_name in possible_products:
                            fake_needs[product_name] = self.consumption[group_name]
            
            for specific_product in possible_products:
                recipe = self.recipes[specific_product]
                
                # also I don't need to decide make or buy at every tick.
                # I can cache this. for this object, for x time.
                
                econ_env = economic_environment
                r = self.econ_agent.make_or_buy(econ_env, recipe, amount = fake_needs[specific_product]["amount"])
               
            # so to compare this, I need to have the other market data available
            # and I need to compare what's being offered
            # with what I can do.
            
            # and only if the thing that I can do is a good solution
            # for that, do I want to actually buy the ingredients and
            # make the thing.
            
            #production_plan.update(r)
        
        # I probably want
        # for the group question
        # I probably want to throw all possible
        # goods into one big list, sort by price and then get the cheapest stuff?
        for group_name in compare_groups:
            group_list = compare_groups[group_name]
            if economic_environment == None:
                continue
            
            full_offer_group_list = []
            
            for good_name in group_list:
                offers = self.econ_agent.find_cheapest_seller(economic_environment,good_name,amount=None)
                full_offer_group_list += offers
                if good_name in self.econ_agent.manufacturing_price_point_cache:
                    mpps = self.econ_agent.manufacturing_price_point_cache[good_name]
                    full_offer_group_list += mpps
                    
                    
            full_offer_group_list.sort(key=lambda x : x.price)
            
            value = self.consumption[group_name]["amount"]
            
            counter = 0
            index = 0
            total_price = 0
            relevant_objects = []
            
            while counter < value:
                my_object = full_offer_group_list[index]
                
                relevant_objects.append(my_object)
                counter += my_object.amount
                total_price = my_object.price
                index += 1
            
            # and then... I want only the manufacturing price points
            # that I have selected here to be used in my production plan
            # and I also want to translate the sell orders that I'm finding
            # here into my buy plan.
            self.add_to_procurement_plans(relevant_objects,production_plan,buy_plan)
        
        
        self.production_plan = production_plan
        self.buy_plan = buy_plan
        
        if False: # notes.
        #for x in self.production:
            
            # figure out how much I can make.
            # given time, raw material and filled jobs.
            
            # figure out what's missing and put that into the 
            # requirements that I have to organize for the next tick.
            # and I think that's crossing into my production planning system.
                        
            # in eve I had a slightly modified problem.
            
            # I had a set of products, I wanted to know what was profitable to make
            # and how much stuff to get.
            
            # in this case, I'm expecting a certain consumption.
            # I need to meet the consumption demand.
            
            # the basic production should fill stocks to 110% of demand and then
            # stock the rest. This will average out to 100% production 
            # and cycle through a 10% rest that's being kept for safety.
            
            # except for food, which will expire. # still need to think about how to do that.
            
            # anyway. I have a demand that I need to meet.
            
            # what does my output look like?
            
            # based on old prices I think...
            #   -> "good":{"make":x,"buy":y}
            # amount? It's not just about theoretical meeting of demand
            # I need to procure an amount X.
            a=1
    
    def add_to_procurement_plans(self,relevant_objects,production_plan,buy_plan):
        for my_object in relevant_objects:
            if "Manufac" in str(type(my_object)):
                # do this
                name = my_object.recipe.name
                if name not in production_plan:
                    production_plan[name] = []
                production_plan[name].append(my_object)
                
            if "Order" in str(type(my_object)):
                # do that.
                if my_object.good not in buy_plan:
                    buy_plan[my_object.good] = []
                buy_plan[my_object.good].append(my_object)
    
    def market_interaction_planning(self):
        # make or buy is nice, just buy
        
        for x in self.consumption:
            a = self.consumption[x]["amount"]
            b = self.inventory[x]["amount"]
            
            c = 0
            if x in self.production_plan:
                for myob in self.production_plan[x]:
                    c += myob.amount
            
            d = 0 
            if x in self.buy_plan:
                for myob in self.buy_plan[x]:
                    d += myob.amount
            
            diff = max(a -(b+c+d),0)
            
            # this is only if it's not already in there.
            # and I'm not making any.
            
            if diff > 0:
                self.buy_plan[x] = {"amount":diff}
        
        for x in self.raw_materials_required:
            if name not in self.buy_plan:
                self.buy_plan[name] = {"amount":0}
            self.buy_plan[name] += self.raw_materials_required[name]
            
        self.econ_agent.wanted_goods = self.buy_plan
        
    def production_tick(self, delta_t):
        """
        delta_t will factor in with how much stuff is done immediately.
        
        I think I can abstract it to the point that the entire
        production that fits into the delta_t is just done
        at once. 
        
        depending on the crafting timing.
        
        I need to translate the schedule funcs to time inputs, or
        fake them for the time.
        
        I guess the faking is what I'm doing now.
        
        so, the question is, do I have a priority for products, if so
        I'm going to make bread and food before luxury stuff. so.
        equal distribution in those areas.
        
        and then going up the chain? or maybe some math to weight it? hmm.
        filling some stuff up completely seems like a better approach.
        
        what did I say yesterday.
        
        there is always more work than people.
        work fills the planned time every time.
        there is always BS people want you to do, just to not do it
        themselves. and they don't really want to pay you for it.
        
        OOOOOK, THAT"S IT.
        
        CUSTOM SET PRIORITIES. I Don't fix them in place. I can do random stuff, as a default with some variety.
        but ultimately the estates will want more for their stuff.
        more value, more manpower, more resources, etc.
        
        ... didn't I do that before?
        
        riiiiight plan steps. not really something I need exactly here.
        buuut. good to keep them here. so.
        
        """
        
        for key in self.resources:
            my_dict = self.resources[key]
            if my_dict["produces"] not in self.inventory:
                self.inventory[my_dict["produces"]] = {"amount":0}
            self.inventory[my_dict["produces"]]["amount"] += my_dict["occupied"] # kind of like an inventory ... hm...
            
    def selling_planning_tick(self):
        
        rest = {}
        for trade_good_name in  self.inventory:
            
            # if I need some, don't sell what I need,
            if trade_good_name in self.consumption:
                diff =  self.inventory[trade_good_name]["amount"] - self.consumption[trade_good_name]["amount"]
                if diff > 0:
                    rest[trade_good_name] = diff
        
            # else sell it?
            else:
                if trade_good_name == "money":
                    continue
                
                # with some restrictions later, because I don't want
                # to sell rare, exclusive stuff that nobody else 
                # has access to nilly willy.
                rest[trade_good_name] = self.inventory[trade_good_name]["amount"]
            
        temp_fix_prices = {}
        
        for trade_good_name in rest:
            self.econ_agent.offered_goods[trade_good_name] = {"amount":rest[trade_good_name]}
            
            if trade_good_name in temp_fix_prices:
                self.econ_agent.prices[trade_good_name] = temp_fix_prices[trade_good_name]
            else:
                self.econ_agent.prices[trade_good_name] = 1
    
            
    
    def planning_step(self,delta_t):
        
        self.consumption_planning()
        self.selling_planning_tick()
        
        self.production_planning()
        self.market_interaction_planning()
        
        # converting distinct food objects into a generalized food category?
        # what's this kind of thing...
        crafting.sum_objects_by_common_purpose(self.inventory)
        crafting.sum_objects_by_common_purpose(self.production_plan)
        
        
        
        # self.pricing_tick()
        
        
        # there is a "can make" step from the crafting(?) that I need.
    
    def trading_tick(self,environment):
        """
        the environment is just a list of other city objects.
        
        that's kind of wrong, not what I built economy for, at the moment.
        
        and this is also actually doing the actual purchasing, 
        and resolving orders
        
        it's not about browsing availability.
        """
        
        if environment == None:
            return
        
        M = economy.Market()
        
        for other_city in environment:
            trader = other_city.econ_agent
            M.set_up_trader(trader)
        
        self.econ_agent.inventory = self.inventory
        self.econ_agent.market_interaction(M)
        
        
    def execution_step(self,delta_t,environment = None):
    
        self.production_tick(delta_t)
        
        self.trading_tick(environment)
        
        self.corruption_tick()
        self.secession_desire_tick()
        self.consumption_tick()
        
    def main(self):
        """
        don't do one main, do a planning and one execution step
        I can 
        """
        raise ValueError
        
        
        self.economy_tick()
        
        
        # self.crime_tick()
        
        # migration pressure via jobs, satisfaction like food/housing
        # actually do the production.
        # do the crime / independence thing.
        
        # produce some currency via gold mining
        # erase some currency via natural loss.
        
        # what do I assume?
        
        # 1 food per pop?
        # 1.5 food per farmer -> overproduction is necessary due to random failure
        # starving for two turns deletes pops
        
        # politicians / administration creates stability / control
        # over area / distance
        
        # everyone needs goods, goods need craftsmen
        
        # corruption, craftsmen skill, etc..  will be covered by statistics, as will
        
        
        
        
        # wealth distribution, job distribution, life expectancy, etc.
        # population, jobs, currency, are all floats, I'm just initializing with round numbers.
        
        a = 1

class Econ:
    def __init__(self):
        self.cyber_econ = basis.Element()
    
    def main(self):
        """simple loop that calls the main of each location."""
        
        for x in self.cyber_econ.elements:
            x.payload.planning_step(1)
        
        for x in self.cyber_econ.elements:
            x.payload.execution_step(1)
        
