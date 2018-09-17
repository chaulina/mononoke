import re
from .stateHelper import getIntent, getMessage, setIntent

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
