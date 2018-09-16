def getFrom(dictionary, dictionary_key, default_value=None):
    value = dictionary
    key_parts = dictionary_key.split(".")
    for key in key_parts:
        if key not in value:
            return default_value
        value = value[key]
    return value

def setTo(dictionary, dictionary_key, value):
    sub_dictionary = dictionary
    key_parts = dictionary_key.split(".")
    last_key = key_parts.pop()
    for key in key_parts:
        if key not in sub_dictionary:
            sub_dictionary[key] = {}
        sub_dictionary = sub_dictionary[key]
    sub_dictionary[last_key] = value