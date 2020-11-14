import discord
import discord.ext
import components.modules

client = discord.Client()

command_prefix = "$"
mcon = components.modules

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(command_prefix):
        commands = message.content.split()
        command = commands[0][1:].lower()

        if command == "say" and commands:
            # await message.channel.send(commands[1:])
            await message.channel.send(mcon.say(commands[1:]))

        elif command == "knock":
            await message.channel.send("Who's there?")

client.run()

await client.change_presence(activity=discord.Game(name="KetanBot Beta Ver."))
