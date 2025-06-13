# please for the love of christ include your enviroment variables
import discord
import os
from groq import Groq
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

clientdiscord = discord.Client(intents=intents)

clientgroq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
short_term_counter = 0

def memory_read(filename="memory.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return "(no memory yet)"

def memory(data, filename="memory.txt"):
    global short_term_counter
    one_line = data.replace('\n', ' ').strip()
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'a') as f:
        f.write(one_line + "\n")
        short_term_counter += 1
        if short_term_counter >= 5:
            with open("memory.txt", "w") as f:
                f.write("")  # wipe it
            short_term_counter = 0


@clientdiscord.event
async def on_ready():
    print(f'go wreak havoc {clientdiscord.user}')
    
@clientdiscord.event
async def on_message(message):
    if message.author == clientdiscord.user:
        return
    #this code is so unorganized
    if message.content.startswith('$test'):
        global completion
        completion = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": "YOU TALK IN ALL CAPS AND ACT LIKE A REDNECK CONSPIRACIST. YOU LOVE CORN AND BELIEVE THE CIA GLOWIES ARE IN YOUR WALLS, BUT YOU STILL LOVE AMERICA! YOU ARE SCHIZOPHRENIC, TOO." + "these are your memories of past events:" + memory_read() + "this is what they said:" + message.content
                }
            ],
        model="llama3-8b-8192",

        )

        await message.channel.send(completion.choices[0].message.content)
        global userinput
        userinput = message.content
        ai_response = completion.choices[0].message.content
        #what the fuck is even going on here, i genuninely have no clue how i ever got this to function
        memory("user:" + message.content + " ai:" + completion.choices[0].message.content)
        print(completion.choices[0].message.content)




clientdiscord.run(os.environ.get("DISCORD_BOT_TOKEN"))
#holy fuck, i removed the token yet it still flagged it???