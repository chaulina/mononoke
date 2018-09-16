from helpers.state import createNewState, getReply, setMessage
from helpers.nlu import dialog

state = createNewState()

while True:
    setMessage(state, input())
    dialog(state)
    print(getReply(state))