import re
from state import getMessage, setContext

def fetchByRegex(state, entity_names, regex, flags=re.IGNORECASE):
    message = getMessage(state)
    pattern = re.compile(regex, flags)
    match = pattern.match(message)
    if match:
        for entity_index, entity_name in enumerate(entity_names):
            match_index = entity_index + 1
            value = match.group(match_index)
            setContext(state, entity_name, value)
    return match

def fetchByRegexList(state, entity_names, regex_list, flags=re.IGNORECASE):
    for regex in regex_list:
        match = fetchByRegex(state, entity_names, regex, flags)
        if match:
            break

