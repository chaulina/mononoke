import unittest
import sys

sys.path.insert(0,'..')
from mononoke.helpers.state import *

class Test_helper_state(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_create_new_state(self):
        expected = {
            "intent": None,
            "context": {},
            "message": "",
            "reply": ""
        }
        state = createNewState()
        self.assertDictEqual(state, expected)
    
    def test_get_from(self):
        dictionary = {"a": 5}
        # get existing key from dictionary
        value = getFrom(dictionary, "a")
        self.assertEqual(value, 5)
        # get non-existing key from dictionary
        value = getFrom(dictionary, "b")
        self.assertEqual(value, None)
        # get non-existing key from dictionary with defaultValue
        value = getFrom(dictionary, "b", "defaultValue")
        self.assertEqual(value, "defaultValue")
    
    def test_intent(self):
        state = createNewState()
        # get intent from new state
        intent = getIntent(state)
        self.assertEqual(intent, None)
        # set intent and re-fetch it
        setIntent(state, "food.order")
        intent = getIntent(state)
        self.assertEqual(intent, "food.order")
    
    def test_message(self):
        state = createNewState()
        # get message from new state
        message = getMessage(state)
        self.assertEqual(message, "")
        # set message and re-fetch it
        setMessage(state, "hi")
        message = getMessage(state)
        self.assertEqual(message, "hi")
    
    def test_context(self):
        state = createNewState()
        # get context from new state
        context = getContext(state, "location")
        self.assertEqual(context, None)
        # set context and re-fetch it
        setContext(state, "location", "Malang")
        context = getContext(state, "location")
        self.assertEqual(context, "Malang")
        # set context with subkey and re-fetch it
        setContext(state, "food.name", "pudding")
        setContext(state, "food.quantity", 5)
        context = getContext(state, "food")
        self.assertDictEqual(context, {"name": "pudding", "quantity": 5})


if __name__ == '__main__':
    unittest.main()