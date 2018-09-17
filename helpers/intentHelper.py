import re
from .stateHelper import getMessage, setIntent

def setIntentByRegex(state, new_intent, regex, flags=re.IGNORECASE):
    message = getMessage(state)
    pattern = re.compile(regex, flags)
    match = pattern.match(message)
    if match:
        setIntent(state, new_intent)
    return match

def setIntentByRegexList(state, new_intent, regex_list, flags=re.IGNORECASE):
    for regex in regex_list:
        match = setIntentByRegex(state, new_intent, regex, flags)
        if match:
            break

