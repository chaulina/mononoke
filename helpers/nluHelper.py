import re
from .contextHelper import hasContext, missingContext, setContextByRegex, setContextByRegexList, resetContext, removeContext
from .dictionaryHelper import getFrom, setTo
from .intentHelper import matchIntentByRegex, setIntentByRegex, setIntentByRegexList
from .messageHelper import matchMessageByRegex, matchMessageByRegexList
from .replyHelper import setReplyByRegex, setReplyByRegexList, setReplyByTemplateList
from .stateHelper import getIntent, setIntent, setContext, setReply

cancel_nlu_config = {
    "conditions": [
        ["match_message_by_regex_list", [".*forget.*", ".*cancel.*"]]
    ],
    "actions": [
        ["set_intent", ""],
        ["set_reply", ["Ok", "Ok, let's start something new"]],
        ["reset_context"]
    ]
}

fallback_nlu_config = {
    "conditions": [
        ["match_intent_by_regex", ".*"]
    ],
    "actions": [
        ["set_context_by_regex", ["unknown_input"], "(.*)"],
        ["set_reply", ["Sorry I don't understand '$unknown_input'", "Could you please describe '$unknown_input'?"]]
    ]
}

default_action_config = {
    "match_intent_by_regex": matchIntentByRegex,
    "match_message_by_regex": matchMessageByRegex,
    "match_message_by_regex_list": matchMessageByRegexList,
    "set_intent": setIntent,
    "set_intent_by_regex": setIntentByRegex,
    "set_intent_by_regex_list": setIntentByRegexList,
    "reset_context": resetContext,
    "has_context": hasContext,
    "missing_context": missingContext,
    "remove_context": removeContext,
    "set_context": setContext,
    "set_context_by_regex" : setContextByRegex,
    "set_context_by_regex_list": setContextByRegexList,
    "set_reply": setReplyByTemplateList,
    "set_reply_by_regex": setReplyByRegex,
    "set_reply_by_regex_list": setReplyByRegexList,
}

def normalizeActionConfig(action_config = {}):
    for action_name in default_action_config:
        value = getFrom(default_action_config, action_name)
        if getFrom(action_config, action_name) == None:
            setTo(action_config, action_name, value)

def normalizeNluConfigList(nlu_config_list = []):
    if len(nlu_config_list) == 0:
        nlu_config_list.append(dict(fallback_nlu_config))

def dialog(state, nlu_config_list = [], action_config = {}):
    normalizeActionConfig(action_config)
    normalizeNluConfigList(nlu_config_list)
    for nlu_config in nlu_config_list:
        # detect whether condition met
        match = True
        for condition in getFrom(nlu_config, "conditions"):
            method_name = condition[0]
            params = condition[1:]
            method = getFrom(action_config, method_name)
            if not method(state, *params):
                match = False
                break
        if match:
            # fetch action and method
            for action in getFrom(nlu_config, "actions"):
                method_name = action[0]
                params = action[1:]
                method = getFrom(action_config, method_name)
                method(state, *params)
            break
