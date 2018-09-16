from .dictionaryHelper import getFrom, setTo

def createNewState():
    return {
        "intent": "",
        "context": {},
        "message": "",
        "reply": ""
    }

def getIntent(state, default_value=""):
    return getFrom(state, "intent", default_value)

def setIntent(state, intent):
    setTo(state, "intent", intent)

def getMessage(state, default_value=""):
    return getFrom(state, "message", default_value)

def setMessage(state, message):
    setTo(state, "message", message)

def getReply(state, default_value=""):
    return getFrom(state, "reply", default_value)

def setReply(state, message):
    setTo(state, "reply", message)

def getContext(state, context_key, default_value=None):
    return getFrom(state, "context." + context_key, default_value)

def setContext(state, context_key, value):
    setTo(state, "context." + context_key, value)
