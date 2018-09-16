import sys
sys.path.insert(0,'..')
from helpers.stateHelper import createNewState, getReply, setMessage
from helpers.nluHelper import dialog

state = createNewState()

while True:
    setMessage(state, input())
    dialog(state)
    print(getReply(state))