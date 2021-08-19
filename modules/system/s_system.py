import ast
import typing

import discord
from discord.ext import commands

from modules.core.c_core import this_bot


class System(commands.Cog):
    """
    System-related commands, accessible to bot owner-only.
    """

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

        ***Usage***: `[bo]shutdown`
        ***Example***: `{1}shutdown`
        """
        print(f"⇒ shutdown invoked")
        await ctx.send(f"Shutting down {this_bot.name}")
        await self.client.close()

    @commands.command()
    @commands.is_owner()
    async def evl(self, ctx, *, evalCommand):
        """
        Evaluate command

        ***Usage***: `[bo]eval <command>`
        ***Example***: `{1}eval print(int('1') + int('1'))`
        """
        evalResult = eval(evalCommand)
        print(f"⇒ eval invoked: {evalCommand}")
        print(f"⇒   result: {eval(evalCommand)}")
        await ctx.send(f"> Your eval result:\n```{evalResult}```")

    @commands.command()
    @commands.is_owner()
    async def xec(self, ctx, *, execCommand):
        """
        Exec a command

        ***Usage***: `[bo]xec <command>`
        ***Example***: `{1}xec my_name = "you"`
        """
        print(f"⇒ exec invoked: {execCommand}")
        try:
            exec(execCommand)
            print("⇒    exec success")
        except Exception as error:
            ctx.send(error)
            print(f"⇒    exec error: {error}")

    @commands.command()
    @commands.is_owner()
    async def get_id(self, ctx, *, user: typing.Optional[discord.User] = None):
        """
        Get Discord user ID

        ***Usage***: `[bo]get_id <@someone#1234>`
        ***Example***: `{1}get_id <@someone#1234>`
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

        ***Usage***: `[bo]get_ctx [something]`
        ***Example***: `{1}get_ctx [something]`
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
    """
    add cog to bot
    """
    bot.add_cog(System(bot))
