# This example requires the 'message_content' intent.

import discord
import os
from groq import Groq
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

clientdiscord = discord.Client(intents=intents)

clientgroq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@clientdiscord.event
async def on_ready():
    print(f'We have logged in as {clientdiscord.user}')

@clientdiscord.event
async def do_a_mario(message):
    if message.author == clientdiscord.user:
        return

    if message.content.startswith('$test'):
        completion = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": "why is j33z such a sigma (make up information)" #+ prompt + memory_read() for use later
                }
            ],
        model="llama3-8b-8192",
        )
        #what the fuck
        await message.channel.send(completion.choices[0].message.content)

clientdiscord.run(api_key=os.environ.get("DISCORD_BOT_TOKEN"))
#holy fuck, i removed the token yet it still flagged it???