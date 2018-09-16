from random import randint
from string import Template
from state import setReply

def replyByTemplate(state, str_template):
    template = Template(str_template)
    context = state["context"]
    reply = template.substitute(**context)
    setReply(state, reply)

def replyByTemplateList(state, str_template_list):
    index = randint(0, len(str_template_list) - 1)
    replyByTemplate(state, str_template_list[index])

