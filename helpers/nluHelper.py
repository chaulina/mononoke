import re
from .entityFetcherHelper import fetchByRegex as fetchEntityByRegex, fetchByRegexList as fetchEntityByRegexList
from .intentDetectorHelper import fetchByRegex as fetchIntentByRegex, fetchByRegexList as fetchIntentByRegexList
from .replierHelper import replyByTemplate, replyByTemplateList
from .stateHelper import getIntent
from .dictionaryHelper import getFrom, setTo

fallback_nlu_config = {
    "old_intent": ".*",
    "new_intent": "",
    "actions": {
        "intent": {
            "method": "regex",
            "params": [".*"]
        },
        "entity": {
            "method": "regex",
            "params": [["unknown_input"], "(.*)"]
        },
        "reply": {
            "method": "template_list",
            "params": [
                ["Sorry I don't understand '$unknown_input'", "Could you please describe '$unknown_input'?"]
            ]
        }
    }
}

default_action_config = {
    "intent": {
        "regex": fetchIntentByRegex,
        "regex_list": fetchIntentByRegexList
    },
    "entity": {
        "regex" : fetchEntityByRegex,
        "regex_list": fetchEntityByRegexList
    },
    "reply": {
        "template": replyByTemplate,
        "template_list": replyByTemplateList
    }
}

def normalizeActionConfig(action_config = {}):
    for action_group in default_action_config:
        for action_name in default_action_config[action_group]:
            key = action_group + "." + action_name
            value = getFrom(default_action_config, key)
            if getFrom(action_config, key) == None:
                setTo(action_config, key, value)

def normalizeNluConfigList(nlu_config_list = []):
    if len(nlu_config_list) == 0:
        nlu_config_list.append(dict(fallback_nlu_config))

def processIntent(state, nlu_config = {}, action_config = {}):
    new_intent = getFrom(nlu_config, "new_intent")
    method_name = getFrom(nlu_config, "actions.intent.method")
    if method_name:
        params = getFrom(nlu_config, "actions.intent.params")
        method = getFrom(action_config, "intent." + method_name)
        method(state, new_intent, *params)

def processEntity(state, nlu_config = {}, action_config = {}):
    method_name = getFrom(nlu_config, "actions.entity.method")
    if method_name:
        params = getFrom(nlu_config, "actions.entity.params")
        method = getFrom(action_config, "entity." + method_name)
        method(state, *params)

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
        old_intent = getFrom(nlu_config, "old_intent")
        current_intent = getIntent(state)
        pattern_match = False
        if old_intent != None and current_intent != None:
            pattern_match = re.compile(old_intent).match(current_intent)
        if pattern_match:
            processIntent(state, nlu_config, action_config)
            processEntity(state, nlu_config, action_config)
            processReply(state, nlu_config, action_config)
