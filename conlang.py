from Conversation import *

Conversation.interact(
    dir="conversations/conlang/",
    ident="conlang1",
    values=[
        system(
            "You are a helpful assistant for designing constructed written languages. You are an expert on the grammar and semantics of existing natural languages as well as many constructed languages. You are an expert in linguistics theory."
        ),
        user(
          "I am designing a new constructed langauge. The language must use the English alphabet. The main new idea for this language is that each modifier, such as an adjective or adverb, is combined with the modified word. List some ideas for unique language features to include in my language."
        ),
        assistant(),
        user(
          "Give some examples of sentences in a new constructed language that includes some of the language features you listed above. Also include the English translation of each sentence."
        ),
        assistant()
    ]
)
