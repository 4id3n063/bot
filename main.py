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

def memory_read(filename="memory.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return "(no memory yet)"

def memory(data, filename="memory.txt"):
    one_line = data.replace('\n', ' ').strip()
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'a') as f:
        f.write(one_line + "\n")

def memory_storing():
            global completion_memory
            completion_memory = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": "Please extremely summarize what this said. Include important details. Everything before 'ai:' is what the user said, while everything after is what the ai said." + completion.choices[0].message.content #always messes this up, ai sucks
                }
            ],
        model="llama3-8b-8192",
            )

@clientdiscord.event
async def on_ready():
    print(f'We have logged in as {clientdiscord.user}')

@clientdiscord.event
async def on_message(message):
    if message.author == clientdiscord.user:
        return

    if message.content.startswith('$test'):
        global completion
        completion = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": "YOU'RE A WOKE MOTHERFUCKER WHO LOVES EATTING CORN AND RANTING ABOUT HOW THE CIA GLOWIES ARE IN YOUR WALLS. this is what they said:" + message.content + memory_read()
                }
            ],
        model="llama3-8b-8192",
        )
        #what the fuck
        await message.channel.send(completion.choices[0].message.content)
        ai_response = completion.choices[0].message.content
        memory_storing()
        #what the fuck is even going on here, i genuninely have no clue how i ever got this to function
        memory(completion_memory.choices[0].message.content)
        print(completion.choices[0].message.content)
        print(completion_memory.choices[0].message.content)

clientdiscord.run(os.environ.get("DISCORD_BOT_TOKEN"))
#holy fuck, i removed the token yet it still flagged it???