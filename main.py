import discord, asyncio
import random
import json
import os,base64


from itertools import cycle
from discord.ext import commands, tasks
from discord.utils import get
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='//', intents=intents, case_insensitive= True, strip_after_prefix=True)
status = cycle([':)', ':('])

# LOADING AND UNLOADING COGS
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

# OTHER COMMANDS

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.guild:
        return await bot.process_commands(message)
    async def giverole():
        mauthor1 = message.author
        role = discord.utils.get(message.guild.roles, name='👑 KING OF THE HILL 👑')
        k_channel = discord.utils.get(message.guild.text_channels, name='👑︱king-of-the-hill')
        await mauthor1.add_roles(role)
            # checks through 10 chats of history for unique authors from the author of the message sent
        messagehistory = k_channel.history(limit=10, before=message)
        async for msg in messagehistory:
            if msg.author != message.author:
                # use in case you need to know what the message said     print(msg.content)
                # use in case you need to know who sent it     print(msg.author)
                # establishes an ID to the previous author of a message.
                prevauthor = msg.author.id
                prevauthormember = message.guild.get_member(prevauthor)
                # if the author has the role, it will remove it
                if role in prevauthormember.roles:
                    await prevauthormember.remove_roles(role)
                    print(f'Role has been removed from {prevauthormember} and given to {mauthor1}.')

    await bot.process_commands(message)
    if message.channel.name == '👑︱king-of-the-hill':
        await giverole()
        return


bot.run('ODk0NjQyMDA2NjAzNzUxNDk2.YVs-TA.ACMsMsIQPqJ7T9ajpsHeO2u0eHY')