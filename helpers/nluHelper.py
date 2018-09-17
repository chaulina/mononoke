import re
from .contextHelper import setContextByRegex, setContextByRegexList
from .intentHelper import setIntentByRegex, setIntentByRegexList
from .replyHelper import setReplyByRegex, setReplyByRegexList
from .stateHelper import getIntent
from .dictionaryHelper import getFrom, setTo

cancel_nlu_config = {
    "old_intent": ".*", # match all intent
    "actions": [
        {
            "method": "set_intent_by_regex_list",
            "params": [
                "",                             # new intent
                [".*forget.*", ".*cancel.*"]    # message pattern
            ]
        },
        {
            "method": "set_reply_by_regex_list",
            "params": [
                ["Ok", "Ok, let's start something new"],
                [".*forget.*", ".*cancel.*"]
            ]
        }
    ]
}

fallback_nlu_config = {
    "old_intent": ".*", # match all intent
    "actions": [
        {
            "method": "set_intent_by_regex",
            "params": [
                "",     # new intent
                ".*"    # message pattern
            ]
        },
        {
            "method": "set_context_by_regex",
            "params": [
                ["unknown_input"],  # set matched group as unknown_input 
                "(.*)"
            ]
        },
        {
            "method": "set_reply_by_regex_list",
            "params": [
                ["Sorry I don't understand '$unknown_input'", "Could you please describe '$unknown_input'?"],
                ".*"
            ]
        }
    ]
}

default_action_config = {
    "set_intent_by_regex": setIntentByRegex,
    "set_intent_by_regex_list": setIntentByRegexList,
    "set_context_by_regex" : setContextByRegex,
    "set_context_by_regex_list": setContextByRegexList,
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

def processReply(state, nlu_config = {}, action_config = {}):
    method_name = getFrom(nlu_config, "actions.reply.method")
    if method_name:
        params = getFrom(nlu_config, "actions.reply.params")
        method = getFrom(action_config, "reply." + method_name)
        method(state, *params)

def dialog(state, nlu_config_list = [], action_config = {}):
    normalizeActionConfig(action_config)
    normalizeNluConfigList(nlu_config_list)
    for nlu_config in nlu_config_list:
        # detect whether old_intent pattern match current_intent
        old_intent = getFrom(nlu_config, "old_intent")
        current_intent = getIntent(state)
        pattern_match = False
        if old_intent != None and current_intent != None:
            pattern_match = re.compile(old_intent).match(current_intent)
        if pattern_match:
            # fetch action and method
            for action in getFrom(nlu_config, "actions"):
                method_name = getFrom(action, "method")
                if method_name:
                    params = getFrom(action, "params")
                    method = getFrom(action_config, method_name)
                    method(state, *params)
            break
