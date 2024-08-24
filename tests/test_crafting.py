from economy_collection import crafting
import unittest

class CraftingTest(unittest.TestCase):
    """
    
    this is also partially covered by the test in test_NPC
    
    """
    def test_can_craft(self):

        E = crafting.CraftingObject("Iron")
        H = crafting.CraftingObject("Wood")

        inv = {E: {"amount": 20}, H: {"amount": 20}}

        P = crafting.CraftingObject("Sword")
        R = crafting.Recipe("Sword")
        W = crafting.Workplace("Forge")
        R.requirements[E] = 1
        R.requirements[H] = 1
        R.output = [P]

        can = R.check_requirements(inv)
        assert can
        inv = {E: {"amount": 20}}
        can = R.check_requirements(inv)
        assert not can
        
    def test_defaults(self):
        crafting.default()
    
    def test_shopping_list(self):
        E = crafting.CraftingObject("Iron")
        H = crafting.CraftingObject("Wood")

        inv = {E.name: {"amount": 15}, H.name: {"amount": 20}}
        R = crafting.Recipe("Sword")
        P = crafting.CraftingObject("Sword")
        R.requirements[E.name] = 1
        R.requirements[H.name] = 1
        R.output = [P]
        
        shopping = crafting.get_shopping_list_for(R,20,inv)
        
        assert shopping == {'Iron': 5}


def single_test():
    a=1
if __name__=="__main__":
    unittest.main()
