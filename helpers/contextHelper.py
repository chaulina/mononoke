import re
from .stateHelper import getContext, getMessage, setContext

def resetContext(state):
    state["context"] = {}

def hasContext(state, context_key):
    return getContext(state, context_key) != None

def missingContext(state, context_key):
    return getContext(state, context_key) == None

def removeContext(state, context_key):
    setContext(state, context_key, None)

def setContextByRegex(state, context_keys, regex = "(.*)", flags = re.IGNORECASE):
    message = getMessage(state)
    pattern = re.compile(regex, flags)
    match = pattern.match(message)
    if match:
        for entity_index, context_key in enumerate(context_keys):
            match_index = entity_index + 1
            value = match.group(match_index)
            setContext(state, context_key, value)
    return match

def setContextByRegexList(state, context_keys, regex_list = [], flags = re.IGNORECASE):
    for regex in regex_list:
        match = setContextByRegex(state, context_keys, regex, flags)
        if match:
            break

