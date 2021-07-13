import typing

import discord
from discord.ext import commands

from main import botName
from modules.core.c_core import is_owner


class System(commands.Cog):
    """System-related commands"""

    def __init__(self, client):
        self.client = client

    # ? ==================
    # ? Commands
    # ? ==================
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        Shutdown the bot

        Command: `[bo]shutdown`
        Example: `{1}shutdown`
        """
        await ctx.send(f"Shutting down {botName}")
        await self.client.close()

    @commands.command()
    @commands.is_owner()
    async def runEval(self, ctx, *, evalCommand):
        """
        Evaluate commands

        Command: `[bo]runEval print(int('1') + int('1'))`
        Example: `{1}runEval print(int('1') + int('1'))`
        """
        await ctx.send(f"> Your eval result:\n```{eval(evalCommand)}```")

    @commands.command()
    @commands.is_owner()
    async def get_id(self, ctx, *, user: typing.Optional[discord.User] = None):
        """
        Get Discord user ID

        Command: `[bo]get_id <@someone#1234>`
        Example: `{1}get_id <@someone#1234>`
        """
        if user is not None:
            _id = user.id
        else:
            _id = ctx.message.author.id
        await ctx.send(f"id: `{_id}`")

    @commands.command()
    @commands.is_owner()
    async def get_ctx(self, ctx):
        """
        See what the bot receive when someone sends something

        Command: `[bo]get_ctx [something]`
        Example: `{1}get_ctx [something]`
        """
        await ctx.send(f"""Msg: {ctx.message}\n
        Author: {ctx.message.author}
        Bot: {ctx.bot}
        Args: {ctx.args}
        Kwargs: {ctx.kwargs}
        Prefix: {ctx.prefix}
        Command: {ctx.command} 
""")


def setup(bot):
    bot.add_cog(System(bot))
