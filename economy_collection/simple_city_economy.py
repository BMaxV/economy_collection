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
        
        # this is how much I plan to produce.
        self.production_plan = {}
        self.raw_materials_required = {}
        
        # this is the list of order objects I plan to buy from.
        self.buy_plan = {}
        # this is the actual number of stuff that I need to buy.
        self.buy_plan_numbers = {}
        
        self.inventory = inventory # goes here
        self.demand = {} # this is what is being subtracted.
        self.consumption_plan = {} # what am I actually going to consumed, based on demand.
        
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
        """
        this needs the group thing again
        and it might be wise to integrate the rest of
        the planning into my consumption plan
        and then do a double check.
        building a new dict here for specific amounts and goods
        and reducing my plan according to the items I picked.
        
        so, "bread" would tick down "food" and 
        but tick up my actual consumption
        and then I would subtract from my inventory.
        
        right... Uhm... I buy based stuff on demand, but I'm not planning for that to be...
        consumed when I do? because the consumption plan is based on what I already have,
        not on what I am making and producing.
        
        This should function should be independent of how I planned to do things.
        I should consume from what I have, regardless of the source.
        
        the current setup works via magic numbers. I haven't actually solved the issue.
        
        """
        
        unmet_demand = {}
        
        # meet generic demands.
        #for key in self.demand:
            #if key in crafting.groups:
                #self.inventory[key]["amount"] -= self.consumption_plan[key]
        # meet specific demands
        
        for key in self.demand:
            #for gn in crafting.groups:
                #group = crafting.grous[gn]
                #if key in group:
                    #break
            #if key not in crafting.groups:
            self.inventory[key]["amount"] -= self.demand[key]["amount"]
        
        
        return unmet_demand
        
    def demand_planning(self):
        """
        the consumption over here is reliable, this will be consumed
        at the end of the tick.
        """
        self.demand["Food"] = {"amount" : self.population}
        self.demand["Consumer Goods"] = {"amount" : self.population}
    
    def find_possible_products(self, unknown_name):
        """
        this feels redundant.
        why am I doing this here and not in the economy.
        
        this builds my compare group
        
        there is a difference between the group of products that
        I want to compare over all (where I'm fine with just buying)
        and the group that I can actually make too, which is subset.
        
        local_compare_group is everything, including the groupname
        possible_products is specifically the things I can make, without the groupname.
        
        but know_how_d is the dict, where the groupname is also true
        if any member of the group can be made.
        
        """
        local_compare_group = []
        
        know_how_d = {}
        possible_products = set()
        if unknown_name in crafting.groups:
            
            groupname = unknown_name
            all_group_members = set(crafting.groups[groupname])
            know_how = set(self.recipes.keys())
            
            possible_products = all_group_members.intersection(know_how)
            
            this_group_list = [groupname] + list(all_group_members)
            local_compare_group = this_group_list
            
            if len(possible_products) == 0:
                know_how_d[groupname] = False
            else:
                know_how_d[groupname] = True
                for productname in possible_products:
                    know_how_d[productname] = True
                            
        else:
            product_name = unknown_name
            if product_name not in self.recipes:
                know_how_d[product_name] = False
                # if I can't make it I probably want 
                # to add it into the buy plan anyway.
            else:
                possible_products = set()
                possible_products.add(product_name)
            
            #... it's just one.
            local_compare_group = [unknown_name]
        
        return local_compare_group, possible_products, know_how_d
    
    
    def demand_based_actual_needs(self):
        """
        I have the group "any" vs. specific problem again.
        let's assume it's "any" for now.
        
        generic and specific objects?
        
        consumption is top down and I'm checking if I can do a
        
        bottom up sum that meets that demand.
        
        with a specical exception for if I actually have "generic objects".
        which I should also do, because it saves computations.
        
        
        how do I interpret my consumtion needs?
        I think interpret them as additions.
        
        people wouldn't say "I want some food, and it has to be a pizza"
        
        ----------
        
        this should be a general economy thing.
        """
        
        # if my specific needs have leftovers
        # I can use those to fill general needs,
        # otherwise don't do that.
        # I don't want to fill the generic stuff first.
        
        needed, specific_leftovers =  self.build_basic_needed_and_leftovers()
        self.update_generic_needs_with_leftovers(needed, specific_leftovers)
        
        self.needed = needed
        return needed
    
    def update_generic_needs_with_leftovers(self,needed,specific_leftovers):
        # update generic needs with specific inventory stuff,
        # if available.
        
        for gn in crafting.groups:
            if gn in needed:
                for specific_name in crafting.groups[gn]:
                    if specific_name in specific_leftovers or specific_name in self.inventory:
                        
                        # that's good, I can subtract that.
                        if specific_name not in specific_leftovers:
                            amount = self.inventory[specific_name]["amount"]
                        else:
                            amount = specific_leftovers[specific_name]
                        needed_there = needed[gn]
                        
                        if needed_there >= amount:
                            met = amount
                            left_over = 0
                        else:
                            met = needed_there
                            left_over = amount - needed_there
                        
                        specific_leftovers[specific_name] = left_over
                        needed[gn] -= met
                        if needed[gn]==0:
                            needed.pop(gn)
        
        return needed
    
    def build_basic_needed_and_leftovers(self):
        specific_leftovers = {}
        needed = {}
        for x in self.demand:
            
            # first of all, check if it's specific or generic.
            
            if x in crafting.groups:
                # it's generic.
                
                # do I have generic objects that meet this?
                if x in self.inventory:
                    if self.inventory[x]["amount"]>= self.demand[x]["amount"]:
                        self.consumption_plan[x] = self.demand[x]["amount"]
                        
                    else:
                        # make something generic or anything specific.
                        # and also check if specific stuff meets this.
                        needed[x] = self.demand[x]["amount"] - self.inventory[x]["amount"]
                        self.consumption_plan[x] = self.inventory[x]["amount"]
            else:
                # it's specific.
                if x in self.inventory:
                    if self.inventory[x]["amount"] >= self.demand[x]["amount"]:
                        left_over = self.inventory[x]["amount"] - self.demand[x]["amount"]
                        if left_over > 0:
                            specific_leftovers[x] = left_over
                            
                        self.consumption_plan[x] = self.demand[x]["amount"]
                    else:
                        needed[x] = self.demand[x]["amount"] - self.inventory[x]["amount"]
                        self.consumption_plan[x] = self.inventory[x]["amount"]
                        
        return needed, specific_leftovers
    
        # these are not the same.
    def production_planning(self,economic_environment=None):
        """
        What's the purpose here.
        
        I know I have certain needs and I need to figure out if
        I can make the stuff to fulfill them, how, how much it would 
        cost, what the best options are.
        
        There are groups, actually, not specific things.
        and the needs are group based needs, not specific based.
        
        I am building complete lists of make or buy price points 
        and then I am choosing the cheapest options to fulfil the group
        needs.
        
        To compare a product, I need to have the other market data
        available and I need to compare what's being offered
        with what I can do.
        """
        
        self.planned_raw_material = {}
        self.planned_production_output = {}
        
        for x in self.resources:
            self.planned_raw_material[x] = self.resources[x]["occupied"]
        
        econ_env = economic_environment
        
        production_plan = {}
        buy_plan = {}
        know_how_d = {}
        
        compare_list = []
        compare_groups = {}
        possible_products = []
                
        # I'm doing this wrong.
        # I want to do a top down thing for the needs
        # then I want to a bottom up process for what I can make
        # and then I sum up and compare.
        
        # I'm not going by need at all. is that right?
        # can prefilter? probably.
        for unknown_name in self.needed:
            local_compare_group, possible_products, know_how_d = self.find_possible_products(unknown_name)
            compare_groups[unknown_name] = local_compare_group
            
            # either... I can make stuff that fulfills it
            if know_how_d[unknown_name] == True:
                self.econ_agent.make_or_buy_option_space(self.needed, local_compare_group, self.recipes, econ_env)
            
            else: # or I HAVE TO buy it.
                self.buy_plan_numbers[unknown_name] = self.needed[unknown_name]
                
        for group_name in compare_groups:
            if economic_environment == None:
                break
            group_list = compare_groups[group_name]
            
            # I already did this.
            full_offer_group_list = self.make_full_offer_group_list(group_list, econ_env)
        
            relevant_objects = self.filter_relevant_objects(full_offer_group_list, group_name)
            
            self.add_to_procurement_plans(relevant_objects,production_plan,buy_plan)
            
            # reduce the needed amount by how much I'm making or planning to buy.
            for x in relevant_objects:
                self.needed[group_name] -= x.amount
                if self.needed[group_name] <= 0:
                    self.needed.pop(group_name)
            
        self.production_plan = production_plan
        self.buy_plan = buy_plan
        
        print("production_plan",production_plan)
        print("buyplan",buy_plan)
        
        return
        
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
    
    def filter_relevant_objects(self,full_offer_group_list,group_name):
        """
        filter what's available with my need
        """
        
        value = self.needed[group_name]
        
        counter = 0
        index = 0
        total_price = 0
        relevant_objects = []
        
        
        while counter < value:
            my_object = full_offer_group_list[index]
            
            relevant_objects.append(my_object)
            
            if "Order" in str(type(my_object)):
                if my_object.good not in self.buy_plan_numbers:
                    self.buy_plan_numbers[my_object.good] = 0
                    
                if counter+my_object.amount > value:
                    add_diff = value - counter
                else:
                    add_diff = my_object.amount
                
                #self.buy_plan_numbers[my_object.good] += add_diff
            
            counter += my_object.amount
            
            index += 1
        
        return relevant_objects
    
    
    def make_full_offer_group_list(self,group_list,econ_env):
        """
        get make or buy result data, from the environment or
        my cache, for the entire product group.
        """
        full_offer_group_list = []
        
        for good_name in group_list:
            offers = self.econ_agent.find_cheapest_seller(econ_env,good_name,amount=None)
            full_offer_group_list += offers
            if good_name in self.econ_agent.manufacturing_price_point_cache:
                mpps = self.econ_agent.manufacturing_price_point_cache[good_name]
                
                full_offer_group_list += mpps[1]
                        
        full_offer_group_list.sort(key=lambda x : x.price)
        return full_offer_group_list
    
    def add_to_procurement_plans(self,relevant_objects,production_plan,buy_plan):
        """
        I want only the manufacturing price points
        that I have selected here to be used in my production plan
        and I also want to translate the sell orders that I'm finding
        here into my buy plan.
        
        I can't run these idependently.
        
        and I'm not guaranteed to be able to do it either. particularly
        not the buying. hmmmm.
        
        I am not properly tracking what I want to buy...
        
        """
        
        for my_object in relevant_objects:
            if "Manufac" in str(type(my_object)):
                name = my_object.recipe.name
                if name not in production_plan:
                    production_plan[name] = []
                production_plan[name].append(my_object)
                
            if "Order" in str(type(my_object)):
                if my_object.good not in buy_plan:
                    buy_plan[my_object.good] = []
                buy_plan[my_object.good].append(my_object)
    
    def market_interaction_planning(self):
        # make or buy is nice, just buy
        
        for x in self.needed:
            a = self.needed[x]
            b = self.inventory[x]["amount"]
            
            c = 0
            if x in self.production_plan:
                for myob in self.production_plan[x]:
                    c += myob.amount
            
            d = 0 
            if x in self.buy_plan and x in self.buy_plan_numbers:
                lc =0 
                while d < self.buy_plan_numbers[x] and lc < len(self.buy_plan[x]):
                    my_ob = self.buy_plan[x][lc]
                    d += myob.amount
                    lc+=1
            
            diff = max(a -(b+c+d),0)
            
            # this is only if it's not already in there.
            # and I'm not making any.
            
            if diff > 0:
                self.buy_plan[x] = {"amount":diff}
        
        for x in self.raw_materials_required:
            if name not in self.buy_plan:
                self.buy_plan[name] = {"amount":0}
            self.buy_plan[name] += self.raw_materials_required[name]
        
        # buy plan was where to buy from.
        
        for x in self.buy_plan_numbers:
            self.econ_agent.wanted_goods[x]={"amount":self.buy_plan_numbers[x]}#self.buy_plan
        
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
        for trade_good_name in self.inventory:
            
            # if I need some, don't sell what I need,
            if trade_good_name in self.consumption_plan:
                diff =  self.inventory[trade_good_name]["amount"] - self.consumption_plan[trade_good_name]
                if diff > 0:
                    rest[trade_good_name] = diff
            
            # else sell it?
            elif self.inventory[trade_good_name]["amount"] > 0:
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
    
    def planning_step(self,delta_t,econ_env):
        
        # this is figuring out what I needed.
        self.demand_planning()
        self.demand_based_actual_needs()
        
        # selling off what I don't need.
        self.selling_planning_tick()
        
        # figure out what I can make and what I need.        
        self.production_planning()
        
        self.ingredient_planning(econ_env)
        # I need to redo the sell planning, because I can't sell my 
        # ingredients.
        
        # this is setting what I'm actually going to buy.
        self.market_interaction_planning()
        
        # converting distinct food objects into a generalized food category?
        # what's this kind of thing...
        #crafting.sum_objects_by_common_purpose(self.inventory)
        #crafting.sum_objects_by_common_purpose(self.production_plan)
    
    def ingredient_planning(self,environment):
        reqs = set()
        for name in self.production_plan:
            print("")
            print(name)
            print("")
            for price_point in self.production_plan[name]:
                print(price_point)
                for req in price_point.requirement_prices:
                    #recipe is basically guaranteed to exist.
                    
                    req_amount = price_point.amount * self.recipes[name].requirements[req]
                    print(req, req_amount)
                    # if I am selling, I want to reduce it.
                    if req in self.econ_agent.offered_goods:
                        self.econ_agent.offered_goods[req] -= req_amount
                    
                    elif req in self.econ_agent.orders["sell_orders"]:
                        
                        
                        # cancel / modify sell orders.
                        # that's not good at all.
                        # I don't want to create them.
                        # rather than canceling them.
                        # but I have to create them for the make_or_buy
                        
                        # one of the assumptions is wrong.
                        # if I need the orders for make or buy planning,
                        # when I already have the stuff, that's wrong.
                        # I already have prices "in mind" even without orders
                        # in practice , in my test, I am defining prices.
                        # the same would happen in other "in practice" cases.
                        # then I can make the make_or_buy decision
                        # without orders and I can delay creating orders
                        # for ingredients, until I'm sure I don't need the ingredients.
                        
                        
                        print("yo",self.econ_agent.orders["sell_orders"])
                        a=1
                    
                    # else I want to buy this, FIND IT.
                    else:
                        if req not in self.buy_plan_numbers:
                            self.buy_plan_numbers[req] = 0
                        self.buy_plan_numbers[req] += req_amount
                    
                    reqs.add(req)
        
        for req in reqs:
            if req not in self.buy_plan:
                amount = self.buy_plan_numbers[req]
                order_list = find_cheapest_seller(environment, req, amount=amount)
                self.buy_plan[req] = order_list
                    
    def trading_tick(self,environment,market=None):
        """
        the environment is just a list of other city objects.
        
        that's kind of wrong, not what I built economy for, at the moment.
        
        and this is also actually doing the actual purchasing, 
        and resolving orders
        
        it's not about browsing availability.
        """
        
        if environment == None:
            return
        
        if market == None:
            market = economy.Market()
        
        for other_city in environment:
            trader = other_city.econ_agent
            market.set_up_trader(trader)
        
        self.econ_agent.inventory = self.inventory
        self.econ_agent.market_interaction(market)
        
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
        
        self.econ_env = economy.EconomyEnvironment()
        
    def main(self):
        """simple loop that calls the main of each location."""
        
        for x in self.cyber_econ.elements:
            x.payload.planning_step(1,self.econ_env)
        
        for x in self.cyber_econ.elements:
            x.payload.execution_step(1)
        
