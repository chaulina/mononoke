# Mononoke

Mononoke is my chatbot-framework hobby-framework. This is not meant to be a serious project, since my purpose of creating this is just for learning and understanding chatbot in the details.

To achieve the quest, I will use a very minimal amount of third-party libraries.

> Trivia: Mononoke (物の怪) means spirit in Japanese.

# The Chatbot Overview

Chatbot is basically another user interface so that the program can talk and understand what type/say, and translate it into structured command.

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

A human can easily understand this texts and conclude that the writer probably want to order something from the restaurant.:
* `I want to order a pizza`
* `I am hungry, very hungry`
* `It is going to be perfect if we have fried chicken now`

As for computer, this is not something easy. Computer mostly work with numbers. Altough in some cases, computer can understand formal languages (like Python or Java), it is not an easy task to understand a natural language.

Natural language change over time, influenced by culture and context, and somehow chaotic (i.e: Doesn't have a concise and simple rule).

This make intent detection a difficult task. There are two approaches to detect intent:
* Predefined pattern based
* Machine learning

Predefined pattern based is quite easy. But it is not scalable. For example, to detect  a user intent, I might make a simple if statements:

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

After a chatbot understand user's intent, it needs to

### The Flow (Katachi)

Let's see again at our third scenario. In the scenario, you ask Kana to order fast-food. But, in the middle of the conversation, you change your mind, and you want to listen Kajiuran music instead.

In order to make the chatbot able to handle the possibilities, the chatbot creator has to first define the dialog flow.

I guess, in general, our chatbot will looks like this:


# Final

I write this article so that I can learn better about chatbot as well as teaching others. However, if you are not interested to build your own chatbot from scratch, yet you want to have a fully functional bot, you can visit:

* [Kata.ai](https://kata.ai/) for building Bahasa Indonesia chatbot. They have bot studio as well as nl studio. And I work there as backend-engineer (which is awesome) :)
* [Dialog Flow](https://dialogflow.com/) for building English and any other language based chatbot.