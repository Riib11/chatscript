from chatscript.OpenAIClient import OpenAIClient
from chatscript.Conversation import Conversation
from os import path
import os

story_name = "Tempus Crucis"


# make story_name unique, them mkdir
story_name_base = story_name
n = 1
while path.exists(story_name):
    story_name = f"{story_name_base} - {n}"
os.mkdir(story_name)

# ==============================================================================
# init
# ==============================================================================


client = OpenAIClient()


class World:
    def __init__(self, desc: str):
        self.desc = desc
        self.convo: Conversation = Conversation(f"{story_name}/world", client)
        self.convo.system(f"""
You are the gamemaster for a multiplayer RPG. {desc}

Instructions:
- Your task is to facilitate an interesting and exciting story and game world for the players.
- The user will say you what a particular player in the game wants to do next.
- You should respond with a detailed vivid description of what the player does, and then tell what happens immediately next.
- Sometimes create obstacles for the players that they must overcome to achieve their goals.
- Make sure that the players stay relatively nearby to earch other so that they can interact.
- Do now allow players to do overpowered actions. Each player should be only as powerful as a slightly above-average person in the game world.
- Always use 3rd person point of view.
- Always refer to a player by their name, never use pronoun "you".
""")


class Player:
    def __init__(self, world: World, name: str, desc: str):
        self.world = world
        self.name = name
        self.desc = desc
        self.convo = Conversation(f"{story_name}/player - {name}", client)
        self.convo.system(f"""
You are a player in a multiplayer RPG. Your character is named {name}. {desc}

RPG world description: {world.desc}

Instructions:
- Your task is to accurately role-play your character in the game world.
- The user will say what is happening in the game world, and then ask you what you want to do next.
- You should respond with a short description of what you want your character to do next.
""")


# ==============================================================================
# config
# ==============================================================================

world: World = World("""
Enter Tempus Crucis, a world where time bends mysteriously, braided with the silver strands of temporal sorcery in a New York City beyond imagination. Time traveling lawyers, known as Chrono-Advocates, navigate the uncertain terrain of this metropolis, their duty centered around disputes that span seconds, minutes, and on rare occasions, entire lifetimes. In this dimension, time is a precious commodity and an enigmatic force, as volatile as it is valuable. The mercurial power of the Time Gates lines the city's nexus, yet it unravels predictably only in the hands of the few who dare to fathom its conundrums. Chrono-Advocates persistently tread upon the fractal boundaries of temporal authority, bound by ancient laws and a code of ethics to ensure their deployment of time manipulation remains just and honorable. The skyline of this New York City is entrenched in arcane glyphwork, testimony to the civilization that harnessed and secured the very fabric of time around its structures. The crux of this society's purpose lies within the towering Temporal Courthouse, a staggering marvel bridging the chasm between human ingenuity and supernatural forces. Chrono-Advocates gamble with fate, delving into the labyrinthine corridors of frayed moments and fractured memories. Each case is a chess game played on an invisible board, where shifting between temporal dimensions serves as the ultimate strategy to preserve truth and deliver justice. However, the rule of 'short temporal distances only' is an unforgiving reminder that they too must dance cautiously with time, lest they misstep and stumble straight into uncharted abysses. When emergencies arise, the stakes are raised, and the lines of morality blur, leaving Chrono-Advocates to tip the scales delicately between bending the laws of time and falling from grace. In Tempus Crucis, as the inexorable clock ticks forward, these guardians of chronology raise their gavels, poised to defend reality and safeguard the ticking arteries of a city pulsating at the edge of existence.
""")


players: list[Player] = [
    Player(world, "Cassandra Novak", """
Meet Cassandra Novak, a seasoned Chrono-Advocate, whose fiercely intuitive mind allows her to unravel the mysteries of time like no other. Her obsidian hair, contrasted with the piercing silver of her calculating eyes, embodies the interwoven dichotomy of chaos and control that defines her daily life. Graced with a stoic demeanor, her voice resonates with authority, echoing through the Temporal Courthouse and demanding respect for her unwavering pursuit of justice. Within the confines of her arcane office, she spends hours strategizing and theorizing, surrounded by walls of temporal artifacts, each whispering secrets of bygone eras. With every measured step through Time Gates, Cassandra bears the weight of raw reality, her conscience a fluent dance between the past and the future, as she safeguards the fragile moments that make up the heart of Tempus Crucis.
"""),
    Player(world, "Tempus Rex", """
In the shadows of Tempus Crucis, there lies a whispered legend of Tempus Rex, the infamous outlaw with a penchant for manipulating time's tender strings. Possessing a ruthless intellect and a mastery over the enigmatic art of temporal sorcery, this elusive figure strikes fear into the hearts of Chrono-Advocates and citizens alike. Always clad in a cloak woven from stolen moments, the outlaw remains a ghostly presence on the periphery of time. Tempus Rex defies the very laws that bind the world, conducting audacious heists through the intricate web of history and the unknown. Driven by a relentless thirst for vengeance against the arcane system, this enigmatic renegade is both a harbinger of chaos and a symbol of rebellion that lurks beneath the ceaseless ticking of Tempus Crucis.
"""),
    Player(world, "Lord Julius Chronister", """
Lord Julius Chronister, Chief Magistrate of the Temporal Courthouse, is a figure both revered and feared in Tempus Crucis. A cogent blend of wisdom and cunning, he strides down the hallways of power, gilded robes leaving trails of whispered rumors and awe in their wake. Ominous stories depict him as stern and unyielding, yet in the quiet corners of his chambers, he pores over ancient tomes that bridge the past with the future, seeking to ensure the delicate balance within temporal boundaries. His astute gaze dissects every time-bound intricacy that falls within his jurisdiction. Chronister's lips carry the wisdom of millennia, sharing only the sparsest fragments with his closest subordinates, especially the gifted Chrono-Advocates. In this enigmatic realm, Lord Julius Chronister safeguard the hands of time while leading it forward, ever vigilant and resolute in his quest to uphold the sanctity of his beloved New York City.
""")
]


n_rounds = 1


# ==============================================================================
# loop
# ==============================================================================

for _ in range(n_rounds):

    # for each player
    for player in players:
        # player:
        # - user: asks player what they do next
        # - assistant: player says what they do next
        player.convo.user(f"""
  What does {player.name} do next?
  """)
        print(f"player [{player.name}] action...")
        player_action = player.convo.assistant()
        player.convo.save()
        player.convo.write()

        # world:
        # - user: says what this player does next
        # - assistant: world says what the player dooes, and then what happens
        #   immediately next
        print(f"updating world about player [{player.name}] action")
        world.convo.user(f"""
  {player.name}: {player_action}
  """)
        print("world action...")
        world_action = world.convo.assistant()
        world.convo.save()
        world.convo.write()

        # other_player:
        # - assistant: world says what happens next
        for other_player in players:
            print(f"updating (other) player [{other_player.name}] about player [{player.name}] action")
            other_player.convo.assistant(world_action)
            other_player.convo.save()
            other_player.convo.write()


