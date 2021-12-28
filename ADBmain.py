import discord, appcommands, asyncio
import random, requests
import json
from datetime import datetime as dt_
import os,base64
os.environ["JISHAKU_HIDE"]="t"
os.environ["JISHAKU_NO_UNDERSCORE"]="t"
os.environ["JISHAKU_RETAIN"]="t"
os.environ["JISHAKU_NO_DM_TRACEBACK"]="t"
os.environ["JISHAKU_FORCE_PAGINATOR"]="t"

from itertools import cycle
from tortoise import Tortoise
from discord.ext import commands, tasks
from discord.utils import get
intents = discord.Intents.all()

from tortoise.backends.base.config_generator import expand_db_url

tortoise = {
  "connections": {
    "default": expand_db_url(
      "postgres://postgres:rrTFof0O6LhkLOkw1VrK@containers-us-west-9.railway.app:5794/railway"
    ),
  },
  "apps": {
    "default": {
      "models": [
        "models"
      ]
    }
  }
}
tortoise["connections"]["default"]["credentials"]["ssl"] = "disable"

class Bot(appcommands.Bot):
  async def init(self):
    await Tortoise.init(config=tortoise)
    await Tortoise.generate_schemas(safe=True)

  def host(self):
    self.loop.run_until_complete(self.init())
    self.run("ODk0NjQyMDA2NjAzNzUxNDk2.YVs-TA.Le57Fqg8U-jttOAv1WkugzEWhLo")

bot = Bot(command_prefix='>>', intents=intents, case_insensitive= True, strip_after_prefix=True)
status = cycle([':)', ':('])

# LOADING AND UNLOADING COGS
# >>jsk load Cogs.cog
# >>jsk unload Cogs.cog

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

bot.owner_ids=[326903703422500866, 730454267533459568]
bot.load_extension("jishaku")
bot.host()
