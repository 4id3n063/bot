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
prompt = "you are nothing"

def memory_read(filename="memory.txt"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return "(no memory yet)"
#This is really just short-term memory.
def memory(data, filename="memory.txt"):
    one_line = data.replace('\n', ' ').strip()
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # Read all lines
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
    else:
        lines = []

    # Append the new line
    lines.append(one_line + "\n")

    # If more than 5 lines, remove the oldest
    if len(lines) > 5:
        lines.pop(0)

    # Write updated lines back to file
    with open(filepath, 'w') as f:
        f.writelines(lines)


@clientdiscord.event
async def on_ready():
    print(f'go wreakhavoc {clientdiscord.user}')
    
@clientdiscord.event
async def on_message(message):
    global prompt
    if message.author == clientdiscord.user:
        return
    #this code is so unorganized
    if message.content.startswith('$test'):
        global completion
        completion = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": prompt + "these are your memories of past events. They are not apart of the user's response.:" + memory_read() + "this is what the user said:" + message.content[len('$test '):].strip()
                }
            ], 
        model="llama3-8b-8192",

        )

        await message.channel.send(completion.choices[0].message.content)
        global userinput
        userinput = message.content[len('$test '):].strip()
        ai_response = completion.choices[0].message.content
        #what the fuck is even going on here, i genuninely have no clue how i ever got this to function
        memory("user:" + message.content[len('$test '):].strip() + " ai:" + completion.choices[0].message.content)
        print(completion.choices[0].message.content)
    
    if message.content.startswith('$wipe'):
        def wipe(filename="memory.txt"):
                   filepath = os.path.join(os.path.dirname(__file__), filename)
                   with open(filepath, "w") as f:
                        f.write("")
        wipe()
        await message.channel.send('fuck...')
        print("memory wiped, what the fuck you monster")
    
    if message.content.startswith('$prompt'):
        prompt = message.content[len('$prompt '):].strip()
        print("Prompt set to " + prompt)
        await message.channel.send("Prompt set to " + prompt)




clientdiscord.run(os.environ.get("DISCORD_BOT_TOKEN"))
#holy fuck, i removed the token yet it still flagged it???