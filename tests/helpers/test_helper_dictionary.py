import unittest
import sys

sys.path.insert(0,'..')
from mononoke.helpers.dictionaryHelper import *

class Test_helper_dictionary(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_from_and_set_to(self):
        state = {}
        # get context from new state
        location = getFrom(state, "location")
        self.assertEqual(location, None)
        # set context and re-fetch it
        setTo(state, "location", "Malang")
        location = getFrom(state, "location")
        self.assertEqual(location, "Malang")
        # set context with subkey and re-fetch it
        setTo(state, "food.name", "pudding")
        setTo(state, "food.quantity", 5)
        food = getFrom(state, "food")
        self.assertDictEqual(food, {"name": "pudding", "quantity": 5})
        self.assertDictEqual(state, {"food": {"name": "pudding", "quantity": 5}, "location": "Malang"})


if __name__ == '__main__':
    unittest.main()