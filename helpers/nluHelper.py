import re
from .contextHelper import setContextByRegex, setContextByRegexList, resetContext
from .intentHelper import matchIntentByRegex, matchIntentByRegexList, setIntentByRegex, setIntentByRegexList
from .replyHelper import setReplyByRegex, setReplyByRegexList, setReplyByTemplateList
from .stateHelper import getIntent, setIntent, setContext, setReply
from .dictionaryHelper import getFrom, setTo

cancel_nlu_config = {
    "conditions": [
        {
            "method": "match_intent_by_regex_list",
            "params": [
                [".*forget.*", ".*cancel.*"]
            ]
        }
    ],
    "actions": [
        {
            "method": "set_intent",
            "params": [""]
        },
        {
            "method": "set_reply",
            "params": [
                ["Ok", "Ok, let's start something new"],
            ]
        },
        {
            "method": "reset_context",
            "params": []
        }
    ]
}

fallback_nlu_config = {
    "conditions": [
        {
            "method": "match_intent_by_regex",
            "params": [".*"]
        }
    ],
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
    "match_intent_by_regex": matchIntentByRegex,
    "match_intent_by_regex_list": matchIntentByRegexList,
    "set_intent": setIntent,
    "set_intent_by_regex": setIntentByRegex,
    "set_intent_by_regex_list": setIntentByRegexList,
    "reset_context": resetContext,
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
            method_name = getFrom(condition, "method")
            if method_name:
                params = getFrom(condition, "params")
                method = getFrom(action_config, method_name)
                if not method(state, *params):
                    match = False
                    break
        if match:
            # fetch action and method
            for action in getFrom(nlu_config, "actions"):
                method_name = getFrom(action, "method")
                if method_name:
                    params = getFrom(action, "params")
                    method = getFrom(action_config, method_name)
                    method(state, *params)
            break
