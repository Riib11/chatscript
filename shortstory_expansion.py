from Conversation import *


Conversation.interact(
    dir="conversations/shortstory/",
    ident="expansion1",
    values=[
        system(
            "You are a creative and knowledgeable writing assistant for a short story author. The author wants to write innovative, unique, original short stories that appeal to niche audiences."
        ),
        user(
            "Write a few paragraphs for the first part of the story Introduce the world. Introduce the main character, who is an adventurer living in a small town on the outskirts of a large kingdom."
        ),
        assistant(),
        user(
            "Write a revised version of those paragraphs. Use more stylized and poetic language. Include vivid descriptions of the environment as events happen. Include more unique details about the setting and characters. Use dialogue more frequently. Use a few metaphors, but not too many."
        ),
        assistant(),
        user(
            "Write a few more paragraphs that continue the story: A disaster happens in the main character's town, which many of the main character's loved ones and friends. The main character becomes motivated to go on an adventure to find and take vengeance on those responsible for the disaster."
        ),
        assistant(),
        user(
            "Write a few more paragraphs of the story. During the adventure, the main character and the griffin encounter several obstacles to their progress. These obstacles include: battle with a magical beast, conflict with a trickster wizard, and imprisonment by a totalitarian king."
        ),
        assistant(),
        user(
            "Rewrite those paragraphs. Use more stylized and poetic language. Include vivid descriptions of the environment as events happen. Include more unique details about the setting and characters. Use dialogue more frequently. Use a few metaphors, but not too many. Include a reason for why the king doesn't want the main character to complete their quest. Include a reason why the guard is willing to help the main character and the griffin escape. Include more details about how the main character and the griffin overcome each obstacle."
        ),
        assistant(),
        user(
            "Write a few more paragraphs of the story: The main character and the griffin encounter a old wise and powerful wizard, who is sympathetic to the rebels' desire for vengeance against the king. The wizard gives the main character a powerful artifact that can inflict great destruction."
        ),
        assistant(),
        user(
            "Rewrite those paragraphs. Use more stylized and poetic language. Include vivid descriptions of the environment as events happen. Include more unique details about the setting and characters. Use dialogue more frequently. Use a few metaphors, but not too many. Include some hints that the wise wizard has ulterior motives that the main character doesn't notice. Include a more vivid description of how the artifact works and how it destroys the king's armies."
        ),
        assistant(),
        user(
            "Write the ending paragraphs of the story. The wizard turns out to be evil. The wizard wanted to overthrow the king, but without causing himself to be blamed, so use the main character as a scapegoat. The wizard lies and claims that he tried to stop the main character from wrecking the kingdom. The main character is weak after his energy is siphoned by the artifact weapon, and cannot defend himself against accusations of treason in court. The griffin tries to help defend the main character, but the wizard casts a curse on the griffin that causes it to shrink slowly until it dissapears entirely. Finally, the story ends with the evil wizard becoming the new king."
        ),
        assistant()
    ],
)

# get the output of one the assistant calls
# upadte the list of messages
# recall Covnersation.update(..)
