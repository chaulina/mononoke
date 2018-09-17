import re
from .stateHelper import getIntent, getMessage, setIntent

def matchIntentByRegex(state, regex, flags=re.IGNORECASE):
    message = getIntent(state)
    pattern = re.compile(regex, flags)
    return pattern.match(message)

def matchMessageByRegex(state, regex, flags=re.IGNORECASE):
    message = getMessage(state)
    pattern = re.compile(regex, flags)
    return pattern.match(message)

def matchMessageByRegexList(state, regex_list, flags=re.IGNORECASE):
    for regex in regex_list:
        match = matchMessageByRegex(state, regex, flags)
        if match:
            return True
    return False
    
def setIntentByRegex(state, new_intent, regex, flags=re.IGNORECASE):
    match = matchIntentByRegex(state, regex, flags)
    if match:
        setIntent(state, new_intent)
    return match

def setIntentByRegexList(state, new_intent, regex_list, flags=re.IGNORECASE):
    for regex in regex_list:
        match = setIntentByRegex(state, new_intent, regex, flags)
        if match:
            break
