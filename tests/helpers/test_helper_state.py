import unittest
import sys

sys.path.insert(0,'..')
from mononoke.helpers.stateHelper import createNewState, getIntent, setIntent, getContext, setContext, getMessage, setMessage, getReply, setReply

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

    def test_intent(self):
        state = createNewState()
        # get intent from new state
        intent = getIntent(state)
        self.assertEqual(intent, "")
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

    def test_reply(self):
        state = createNewState()
        # get reply from new state
        reply = getReply(state)
        self.assertEqual(reply, "")
        # set reply and re-fetch it
        setReply(state, "hi")
        reply = getReply(state)
        self.assertEqual(reply, "hi")
 
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