import sys
sys.path.insert(0,'..')
from helpers.stateHelper import createNewState, getReply, setMessage
from helpers.nluHelper import dialog, fallback_nlu_config, cancel_nlu_config

nlu_config_list = [
    cancel_nlu_config,
    {
        "conditions": [
            ["match_intent_by_regex_list", ["I want to order .*"]]
        ],
        "actions": [
            ["set_intent", "food.order"],
            ["set_context_by_regex_list", ["food"], ["I want to order (.*)"]],
            ["set_reply", ["You have just order $food", "Your $food is coming"]]
        ]
    },
    fallback_nlu_config,
]
state = createNewState()

while True:
    setMessage(state, input())
    dialog(state, nlu_config_list)
    print(getReply(state))