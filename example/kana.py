import sys
sys.path.insert(0,'..')
from helpers.stateHelper import createNewState, getReply, setMessage
from helpers.nluHelper import dialog, fallback_nlu_config, cancel_nlu_config

nlu_config_list = [
    cancel_nlu_config,
    {
        "conditions": [
            {
                "method": "match_intent_by_regex_list",
                "params": [["I want to order .*"]]
            }
        ],
        "actions": [
            {
                "method": "set_intent",
                "params": ["food.order"]
            },
            {
                "method": "set_context_by_regex_list",
                "params": [["food"], ["I want to order (.*)"]]
            },
            {
                "method": "set_reply",
                "params": [
                    ["You have just order $food", "Your $food is coming"]
                ]
            },
        ]
    },
    fallback_nlu_config,
]
state = createNewState()

while True:
    setMessage(state, input())
    dialog(state, nlu_config_list)
    print(getReply(state))