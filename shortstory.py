from Conversation import *


def shortstory(ident, genre, theme, main_idea, author):
    filepath = f"conversations/shortstory/{ident}.json"
    filepath_output = f"conversations/shortstory/{ident}.md"

    # create an empty Conversation at the filepath if doesn't already exist
    if not path.exists(filepath):
        convo = Conversation(ident, [])
        convo.save(open(filepath, "w+"))

    convo = Conversation.load(open(filepath, "r+"))

    convo.update([
        system(
            "You are a creative and knowledgeable writing assistant for a short story author. The author wants to write innovative, unique, original stories that appeal to niche audiences and not necessarily to the general public."
        ),
        user(
            f"I am writing a {genre} short story with this theme: {theme}. Write a list of interesting, original, and thematic ideas that would be interesting to include in my short story."
        ),
        assistant(None),
        user(
            "Write a brief summary of a short story that ties together a few of the ideas that you listed above. The summary should include a description of the setting, an introduction to the main characters, the main plot points, and a conclusion."
        ),
        assistant(None),
        user(
            f"Write a revised version of that summary which uses most of the same details, but also makes sure to include this main idea: {main_idea}."
        ),
        assistant(None),
        user(
            f"Write a short story in the style of {author} and based on that summary. Make sure the story is around 2500 words. The story should first introduce the setting and main characters, then flush out the details of and transition smoothly between all the plot points, and then finish the story with the conclusion."
        ),
        assistant(None),
        user(
            "Write a revised version of that short story. Use more stylized language with vivid descriptions and a few metaphors, include more unique details about the setting and characters, and use dialogue more frequently. Make the revised story under 2000 words."
        ),
        assistant(None),
    ])
    convo.submit()

    convo.write(open(filepath_output, "w+"))
    convo.save(open(filepath, "w+"))


shortstory(
    "test3-moon",
    genre="science fiction",
    theme="in a near-term future where many civilians live and work on the moon, a top secret spy operation is conducted in an international lunar colony",
    main_idea="political intrigue between spies of different nation-companies that are vying for influence in the lunar colony",
    author="Isaac Asimov"
)
