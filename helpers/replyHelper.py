import re
from random import randint
from string import Template
from .dictionaryHelper import getFrom
from .stateHelper import setReply, getMessage

def reply(state, str_template):
    template = Template(str_template)
    context = getFrom(state, "context")
    reply = template.substitute(**context)
    setReply(state, reply)

def setReplyByTemplateList(state, str_template_list):
    index = randint(0, len(str_template_list) - 1)
    reply(state, str_template_list[index])

def setReplyByRegex(state, str_template_list, regex=".*", flags=re.IGNORECASE):
    message = getMessage(state)
    pattern = re.compile(regex, flags)
    match = pattern.match(message)
    if match:
        index = randint(0, len(str_template_list) - 1)
        reply(state, str_template_list[index])
    return match

def setReplyByRegexList(state, str_template_list, regex_list = [], flags = re.IGNORECASE):
    for regex in regex_list:
        match = setReplyByRegex(state, str_template_list, regex, flags)
        if match:
            break

