import asyncio

import discord
import random
from discord.ext import commands
import json


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Discord bot is ready.')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def status(self, ctx, *, status):
        game = discord.Game(status.replace('playing', ''))
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(f"King of the Bots is now playing {status.replace('playing ', '')}.")

    @commands.command(aliases=['ip'])
    async def get_ip(self, ctx):
        if ctx.message.author == self.bot.user:
            return
        else:
            rightchannel = self.bot.get_channel(858550836560003082)
            print(ctx.channel.id)
            if str(ctx.channel.id) == '858550836560003082':
                await ctx.send("Please respond with your exact username in game.")
                try:
                    username = await self.bot.wait_for(event="message", timeout=30.0)
                    owner = self.bot.get_user(326903703422500866)
                    await owner.send(f"User: {username.content} would like to be added to the whitelist.")
                    embed = discord.Embed(title="The IP is: 104.143.2.59:25590", description="Please wait to be whitelisted.", color=discord.Color.green())
                    await ctx.author.send(embed=embed)
                except asyncio.TimeoutError:
                    await ctx.send("You ran out of time.")
            else:
                await ctx.send(f"Bro go use this in the {rightchannel.mention} chat...")


def setup(bot):
    bot.add_cog(FunCommands(bot))
