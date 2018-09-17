import sys
sys.path.insert(0,'..')
from helpers.stateHelper import createNewState, getReply, setMessage
from helpers.nluHelper import dialog, fallback_nlu_config, cancel_nlu_config

nlu_config_list = [
    cancel_nlu_config,
    fallback_nlu_config,
]
state = createNewState()

while True:
    setMessage(state, input())
    dialog(state, nlu_config_list)
    print(getReply(state))