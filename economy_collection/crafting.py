

# I can introduce a simple decision making tree here
# to learn about material properties

# maybe

# otherwise it's just slow trading, where you can either get the money
# and buy something from a trader, or you can gather the resources and
# make something yourself, but that will take some time.

# looks like there is no functional difference between these, that's
# good news.

# I think objects as materials is overdesigned for now.
# even later it might be easier to refer to things by string name
# and look up properties in specialized dictionaries rather
# than shoving it all into objects.

class CraftingObject:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        s = "< crafting object "+str(id(self))+" "+self.name+" >"
        return s

# hm this is like the cybernetics stuff maybe?
target_components = {
            "sword": ["handle", "blade"],
            "spear": ["shaft", "tip"], 
            "bow": ["body"]
            }
materials = ["wood", "MEGAwood", "iron", "MEGAiron"]


# ok, so clearly, there are groups where exchaning one part or material
# for another isn't a problem
# and then there are products where it really is a problem.
# so, I can't replace hammers with saws. 
# but I can replace Bread with Fish if it's about "having anything to eat".

groups = {"Food":["Bread","Fish"],
            "Consumer Goods":["Clothing"], # clothing could be it's own thing.
            "Tools":["Hammer","Shovel"]}

class Component:
    def __init__(self, name, possible_materials):
        self.possible_materials = ["Wood","Iron"]

class Recipe:
    def __init__(self, name, requirements=None, output=None):
        self.name = name
        # object: how many
        if requirements == None:
            self.requirements = {}
        else:
            self.requirements = requirements
        if output == None:
            self.output = {}
        else:
            self.output = output
        
        self.make_process_cost = 0

    def to_dict(self):

        d1 = {}
        for x in self.requirements:
            d1[x.name] = self.requirements[x]
        d2 = {}
        for x in self.output:
            d2[x.name] = self.output[x]

        d = {"name": self.name,
             "requirements": d1,
             "output": d2}

        return d

    @classmethod
    def from_dict(self, d):
        r = Recipe(d["name"], d["requirements"], d["output"])
        return r

    def check_requirements(self, inventory):
        """
        return the lowest number of possible products, given the 
        input inventory
        """
        
        lowest_ns = []
        for itemname in self.requirements:
            if itemname in inventory:
                have_n = inventory[itemname]["amount"]
                lowest = have_n.__floordir__(self.requirements[itemname])
                lowest_ns.append(lowest)
        
        lowest = min(lowest_ns)
        
        return lowest

class Workplace:
    def __init__(self, name):
        self.name = name

class ProductionLocation:
    """
    should have an inventory, recipes, etc.
    basically a collection object that's not
    a city
    a company
    a person
    a single workstation
    """
    def __init__(self, name):
        self.recipes = {}

class Process:
    def __init__(self, name):
        self.name = name
        self.requirements = []

def get_shopping_list_for(recipe,amount,inventory):
    needed = {}
    for name in recipe.requirements:
        have = inventory[name]["amount"]
        needed_i = recipe.requirements[name]*amount
        value = max(0, needed_i - have)
        if value > 0:
            needed[name] = value
    
    return needed


def sum_objects_by_common_purpose(inventory_like_dict,groups=None):
    
    if groups == None:
        groups = {"Food":["Bread","Fish"],
                "Consumer Goods":["Clothing"], # clothing could be it's own thing.
                "Tools":["Hammer","Shovel"]}
        
    my_sum = {}
    for name in inventory_like_dict:
        for group_name in groups:
            if name in groups[group_name]:
                if group_name not in my_sum:
                    my_sum[group_name] = 0
                my_sum[group_name] += inventory_like_dict[name]["amount"]
                
    return my_sum
    

def default():
    """I feel like these should be saved in a file with a more sensible syntax."""

    grain = CraftingObject("Grain")
    water = CraftingObject("Water")
    iron = CraftingObject("Iron")
    ore = CraftingObject("Ore")
    coal = CraftingObject("Coal")
    wood = CraftingObject("Wood")
    stone = CraftingObject("Stone")
    HPMIX = CraftingObject("Healing Potion base mix")
    HP = CraftingObject("Healing Potion")
    stone = CraftingObject("Stone")

    meat = CraftingObject("Meat")
    veggie = CraftingObject("Vegetable")
    leather = CraftingObject("Leather")
    wool = CraftingObject("Wool")
    
    Bread =  CraftingObject("Bread")
    
    materials = {water.name: water,
                 iron.name: iron,
                 wood.name: wood,
                 stone.name: stone,
                 meat.name: meat,
                 veggie.name: veggie,
                 grain.name: grain,
                 ore.name: ore,
                 coal.name: coal,
                 HPMIX.name: HPMIX,
                 HP.name:HP,
                 "Bread":Bread,
                }
    
    
    
    
    # ------
    mill = Workplace("Mill")
    F = CraftingObject("Flour")
    Fr = Recipe("Flour")

    Fr.requirements[grain] = 3
    Fr.output = {F: 1}
    # ------

    # ------
    M = CraftingObject("Metal")
    Mr = Recipe("Metal")

    Mr.requirements[ore] = 3
    Mr.requirements[coal] = 3
    Mr.output = {M: 1}
    # ------

    W = Workplace("Forge")

    GS = CraftingObject("Greatsword")
    GSr = Recipe("Greatsword")

    GSr.requirements[iron] = 3
    GSr.requirements[wood] = 3
    GSr.output = {GS: 1}

    SW = CraftingObject("Sword")
    SWr = Recipe("Sword")

    SWr.requirements[iron] = 2
    SWr.requirements[wood] = 2
    SWr.output = {SW: 1}

    D = CraftingObject("Dagger")
    Dr = Recipe("Dagger")

    Dr.requirements[iron] = 1
    Dr.requirements[wood] = 1
    Dr.output = {D: 1}

    CP = Workplace("Cookingplace")

    Steak = CraftingObject("Steak")
    Steakr = Recipe("Steak")

    Steakr.requirements[meat] = 1
    Steakr.requirements[wood] = 1
    Steakr.output = {Steak: 1}

    Soup = CraftingObject("Soup")
    Soupr = Recipe("Soup")
    
    HPr = Recipe("Healing Potion")
    HPr.requirements[water] =1 
    HPr.requirements[HPMIX]=1
    HPr.output = {HP: 1}
    
    Breadr = Recipe("Bread")
    Breadr.requirements[water] = 1
    Breadr.requirements[grain] = 1
    Breadr.output = {Bread: 1}
    Breadr.make_process_cost = 0
    

    Soupr.requirements[meat] = 1
    Soupr.requirements[water] = 3
    Soupr.requirements[veggie] = 3
    Soupr.output = {Soup: 1}

    products = {Soup.name: Soup,
                Steak.name: Steak,
                GS.name: GS,
                D.name: D,
                SW.name: SW,
                F.name: F,
                M.name: M,
                HP.name:HP,
                }

    recipes = {Soupr.name: Soupr,
               Steakr.name: Steakr,
               GSr.name: GSr,
               Dr.name: Dr,
               SWr.name: SWr,
               Fr.name: Fr,
               Mr.name: Mr,
               HPr.name:HPr,
               Breadr.name:Breadr,
               }

    return materials, products, recipes





if __name__ == "__main__":
    # test()
    default()
