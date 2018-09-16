import entityFetcher
import intentDetector
import replier
from state import getIntent
from dictionary import getFrom

default_nlu_config = {
    "old_intent": None,
    "new_intent": None,
    "actions": {
        "intent": {
            "method": "regex",
            "params": [".*"]
        },
        "entity": {
            "method": "regex",
            "params": ["(.*)", ["unknown_input"]]
        },
        "reply": {
            "method": "template_list",
            "params": [
                "Sorry I don't understand '$unknown_input'",
                "Could you please describe '$unknown_input'?",
            ]
        }
    }
}

default_action_config = {
    "intent": {
        "regex" : intentDetector.fetchByRegex,
        "regex_list": intentDetector.fetchByRegexList
    },
    "entity": {
        "regex" : entityFetcher.fetchByRegex,
        "regex_list": entityFetcher.fetchByRegexList
    },
    "replier": {
        "template": replier.replyByTemplate,
        "template_list": replier.replyByTemplateList
    }
}

def normalizeActionConfig(action_config = {}):
    for action_group in default_action_config:
        for action_name in default_action_config[action_group]:
            key = action_group + "." + action_name
            if getFrom(action_config, key) == None:
                action_config[action_group][action_name] = default_action_config[action_group][action_name]

def normalizeNluConfigList(nlu_config_list = []):
    if len(nlu_config_list) == 0:
        nlu_config_list.append(dict(default_nlu_config))

def dialog(state, nlu_config_list = [], action_config = {}):
    normalizeActionConfig(action_config)
    normalizeNluConfigList(nlu_config_list)
    current_intent = getIntent(state)
    for nlu_config in nlu_config_list:
        old_intent = getFrom(nlu_config, "old_intent")
        if (old_intent != None) and  (old_intent != current_intent):
            continue
        new_intent = getFrom(nlu_config, "new_intent")
