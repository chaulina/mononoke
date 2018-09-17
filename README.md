# Mononoke

Mononoke is my chatbot-framework hobby-project. This is not meant to be a serious project, since my purpose of creating this is just to learn and understanding chatbot in the details.

To achieve the quest, I will use a very minimal amount of third-party libraries.

> Trivia: Mononoke (物の怪) means spirit in Japanese.

# The Chatbot Overview

Chatbot is basically another user interface so that the program can talk and understand what user type/say, and translate it into structured command.

Every chatbot need some NLP (natural language processing) technique. Let's start with an example of a dialog with a chatbot named `Kana`:

> Trivia: `Kana` sounds like a Japanese name. But actually it is a `Malang-walikan` term for `child` (i.e: If you read `kana` backward, you will get `anak` which mean `child` in Bahasa Indonesia).

__Scenario I__

```
You: I'm hungry, can you please order me a fried chicken and softdrink
Kana: From which restaurant?
You: McD
Kana: How would you pay the bill?
You: I want to use paypal
Kana: Let me know your paypal account
You: Here it is: gofrendi@asgard.com
Kana: Okay, your fried chicken and softdrink is coming
```

__Scenario II__

```
You: Hi Kana, I want to order something from McD
Kana: What do you want to order?
You: A fried chichen and softdrink. Ah, and before you ask, here is my credit card number: xxx.xxx.xxx
Kana: Okay, your fried chicken and softdrink is coming
```

__Scenario III__
```
You: Hi Kana, I want to order something from McD
Kana: What do you want to order?
You: Umm... Let me think for a while
Kana: Take your time
You: Oh, forget it Kana, play me a Yuki Kajiura music instead.
Kana: [play music]
```

## Chatbot as User Interface

In any cases, you can see chatbot as a fun and natural layer that help the user to fill up a form. In the example, our `Kana` can serve us two things:
* Order food
* Play Music

The form for ordering food might look like this:

```
Restaurant      : __________
Item            : __________
Payment method  : __________ [Choose one: Cash, Credit Card, Paypal]
Payment account : __________
[Submit Button]
```

while the form for playing music might look like this:

```
Music genre: __________ or Artist : __________
[Play Button]
```

## The Three Elements of Chatbot

In order to do it's job, a chatbot has to know what it suppose to do, detect user's intent, and detect interesting keyword:

> Trivia: According Mikkyo Buddhism, there are `three secrets` that has to be discovered in order to make peace with the harmful spirit (Mononoke / 物の怪):  
> * Form (Katachi / 形)
> * Truth (Makoto / 誠)
> * Reason (Kotawari / 理り)

### Intent Detection (Kotawari)

We can easily understand the following texts and conclude that the writer probably want to order something from the restaurant.:
* `I want to order a pizza`
* `I am hungry, very hungry`
* `It is going to be perfect if we have fried chicken now`

But for computer, this is not something easy. Computer mostly work with numbers. It is true that in some cases, computer can understand formal languages (like Python or Java). But understanding natural language is something totally different.

Natural language change over time, influenced by culture and context, and somehow chaotic (i.e: Doesn't have a concise and simple rule).

This make intent detection a difficult task. So far, there are two approaches to detect intent:
* Predefined pattern based
* Machine learning

Predefined-pattern-based recognition is quite easy. But it is not scalable. For example, to detect  a user intent, I might make a simple if statements:

```python
intent = null
message = input()
if message == "I want to order a pizza":
    intent = "food.order"
if message == "I am hungry, very hungry":
    intent = "food.order"
if message == "It is going to be perfect if we have fried chicken now":
    intent = "food.order"
if message == "forget it":
    intent = "cancel"
if message == "play music":
    intent = "music.play"
```

Well, the program might be smart enough for hackaton, but not in real world situation. Because people can virtually invent thousands of way to say the same thing.

It is going to be better if the chatbot can learn about user's intent based on data (so that we don't need to code too much).

In machine learning, there are a lot of method that can be used to solve classification problem. SVM, Neural network, Naive Bayes, KNN, etc. We are not going to discuss the detail here, but we can always see intent-detaction as classification-problem.

Surely, some processing is required in order to change the words into numbers. You can transform a sentence into a vector by simply calculating how many words in the sentence. Example:

```
D1: I want to order a pizza`
D2: I am hungry, very hungry`
D3: It is going to be perfect if we have fried chicken now`

        D1  D2  D3
I       1   1   0
want    1   0   0
to      1   0   0
order   1   0   0
a       1   0   0
pizza   1   0   0
am      0   1   0
hungry  0   2   0
very    0   1   0
It      0   0   1
is      0   0   1
going   0   0   1
be      0   0   1
...     .........
```

This vectorization process is quite easy, yet it come with a lot of problem. To begin with, you see many `0` in the vector. It means that it is a sparse matrix, and you need to allocate a lot of memory slots to represent nothingness.

To overcome this, I see some people prefer CNN (Convulational Neural Network) or RNN (Recurrent Neural Network). Until the day this article is written, I only have a very shallow understanding about the methods, and I will complete this article once I know better.

### Slotting and Named Entity Recognition (Makoto)

After a chatbot understand user's intent, it needs to get the entities. The process to acquired the entity is named NER (Named Entity Recognition).

The purpose of NER is to transform this message:

```
I want to order 2 pan pizza
```

into:

```
{
    "food": "pizza",
    "quantity": 2
}
```

The easiest way for slotting is of course by using hard-coded regex as follow:

```python
import re
message = 'I want to order 2 pan pizza'
pattern = re.compile('i want to order ([0-9]*) pan (.*))
match = pattern.match(message)
if match:
    print("food " + match.group(2))
    print("quantity " + match.group(1))
```

But again, this approach doesn't scale quite well. NER is a quite difficult topic. Nowadays people try to solve this problem by combining machine learning + semantics.

### The Flow (Katachi)

Let's see again at our third scenario. In the scenario, you ask Kana to order fast-food. But, in the middle of the conversation, you change your mind, and you want to listen Kajiuran music instead.

In order to make the chatbot able to handle the possibilities, the chatbot creator has to first define the dialog flow.

I guess, in general, our chatbot can be written as [kana.py](example/kana.py):

```python
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

```

## Chatbot in Action

Okay, now let's see our `Kana` do the real job:

```
gofrendi@asgard:~/Projects/mononoke/example$ python3 kana.py
Press ctrl + c to end chat
You: Hi
Kana: Sorry I don't understand 'Hi'
You: it is going to be nice if we have music
Kana: What do you want to play?
You: forget it
Kana: Ok, let's start something new
You: I'm hungry now
Kana: Any preference?
You: burger
Kana: You have just order burger
You:
```

Good enough for a chatbot based on regex, isn't it?

# Final

I write this article so that I can learn better about chatbot as well as teaching others. However, if you are are interested to build your own smart-functional-chatbot, you can visit:

* [Kata.ai](https://kata.ai/) for building Bahasa Indonesia chatbot.
* [Dialog Flow](https://dialogflow.com/) for building English and any other language based chatbot.