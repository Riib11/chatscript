from Conversation import *

# file settings
ident = "moon_story"
filepath = f"conversations/shortstory/{ident}.json"
filepath_output = f"conversations/shortstory/{ident}.md"

# story settings
author = "Isaac Asimov"

# create an empty Conversation at the filepath if doesn't already exist
if not path.exists(filepath):
    convo = Conversation(ident, [])
    convo.save(open(filepath, "w+"))

convo = Conversation.load(open(filepath, "r+"))

convo.update([
    system(
        "You are a creative and knowledgeable writing assistant for a short story author. The author wants to write innovative, unique, original short stories that appeal to niche audiences and not necessarily to the general public."
    ),
    user(
        f"I am writing a science fiction short story about the invention of time travel technology in a near-future setting. Write a list of interesting, original, and thematic ideas that I could use for my story."
    ),
    assistant(None),
    user(
        """
Write a detailed summary of a short story that ties together these ideas:
- Problems with identity: Time travel raises questions about identity. Are you identical to your past self, even if you can go back in time and experience the same world from a different perspective?
- Surveillance and control: With the power to manipulate time and history, who gains control over information? Could time travel be used for surveillance or manipulation of individuals or entire societies?
The summary should include a description of the setting, an introduction to the main characters, the main plot points, and a conclusion.
- Time travel as addiction: Could the ability to visit the past and potentially change our own outcomes become addictive? What are the consequences of such an addiction?
- Time as a finite resource: What happens when we run out of time travel opportunities? What sort of impact might this have on society and scientific exploration?
"""
    ),
    assistant(None),
    user(
        f"Write a revised version of that summary. Include more details about Sarah's loss of self due to meeting many other versions of herself time-traveling. Include an explanation of why Michael recognizes that Sarah's journey is a way out of his job. Include an interesting logical explanation for why time becomes a finite resource for Sarah at the climax of the story. Make the conclusion tragic, and with more existential dread."
    ),
    assistant(None),
    user(
        f"Write a short story in the style of {author} and based on that summary. Make sure the story is around 2500 words. The story should first introduce the setting and main characters, then flush out the details of and transition smoothly between all the plot points, and then finish the story with the conclusion."
    ),
    assistant(None),
    user(
        "Write a revised version of that short story. Use more stylized and poetic language. Include vivid descriptions of the environment as events happen. Use metaphors when describing the environment or the main character's thoughts. Include more unique details about the setting and characters. Use dialogue more frequently. Make the revised story under 2000 words."
    ),
    assistant(None),
])
convo.submit()

convo.write(open(filepath_output, "w+"))
convo.save(open(filepath, "w+"))
