import sys
sys.path.insert(0,'..')
from helpers.stateHelper import createNewState, getReply, setMessage
from helpers.nluHelper import dialog, fallback_nlu_config, cancel_nlu_config

nlu_config_list = [
    cancel_nlu_config,

    {
        'conditions': [
            ['match_intent_by_regex', 'food.order'],
            ['missing_context', 'food'],
        ],
        'actions': [
            ['set_intent', ''],
            ['set_context_by_regex_list', ['food'], ['I want to order (.*)', '(.*)']],
            ['set_reply', ['You have just order $food', 'Your $food is coming']],
            ['set_context', 'food', None]
        ]
    },

    # order food
    {
        'conditions': [
            ['match_message_by_regex_list', ['I want to order .*']]
        ],
        'actions': [
            ['set_intent', ''],
            ['set_context_by_regex_list', ['food'], ['I want to order (.*)']],
            ['set_reply', ['You have just order $food', 'Your $food is coming']],
            ['set_context', 'food', None]
        ]
    },

    # order food
    {
        'conditions': [
            ['match_message_by_regex_list', ['.*hungry.*', '.*eat.*']]
        ],
        'actions': [
            ['set_intent', 'food.order'],
            ['set_reply', ['Any preference?', 'What do you like to eat?']]
        ]
    },

    # previously, user want to play music now he specify the query
    {
        'conditions': [
            ['match_intent_by_regex', 'music.play'],
            ['missing_context', 'music_query'],
            ['match_message_by_regex_list', ['play .* music', 'play me .*', '.*']]
        ],
        'actions': [
            ['set_intent', ''],
            ['set_context_by_regex_list', ['music_query'], ['play (.*) music', 'play me (.*)', '(.*)']],
            ['set_reply', ['Please open https://youtube.com?watch=$music_query']],
            ['set_context', 'music_query', None]
        ]
    },

    # user want to play music and already specify query
    {
        'conditions': [
            ['match_message_by_regex_list', ['play .* music', 'play me .*']]
        ],
        'actions': [
            ['set_intent', ''],
            ['set_context_by_regex_list', ['music_query'], ['play (.*) music', 'play me (.*)']],
            ['set_reply', ['Please open https://youtube.com?watch=$music_query']],
            ['set_context', 'music_query', None]
        ]
    },

    # user want to play music but not specify the query
    {
        'conditions': [
            ['match_message_by_regex_list', ['.*music.*', '.*song']]
        ],
        'actions': [
            ['set_intent', 'music.play'],
            ['set_reply', ['Any preference?', 'What do you want to play?']]
        ]
    },

    fallback_nlu_config,
]
state = createNewState()

print('Press ctrl + c to end chat')
while True:
    print('You: ', end='', flush=True)
    setMessage(state, input())
    dialog(state, nlu_config_list)
    print('Kana: ' + getReply(state))
