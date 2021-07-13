import typing
import discord
from discord.ext import commands


class Messaging(commands.Cog):
    """Messaging commands"""
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self,
                  ctx,
                  channel: typing.Optional[discord.TextChannel] = None,
                  user: typing.Optional[discord.Member] = None,
                  *,
                  text: typing.Optional[str] = None):
        """
        Make the bot say something

        Command: `[p]say [target/location] <your words>` where [p] is bot prefix
        Example: `{0}say Hi!` or `{0}say #bot Hello!`
        """
        if text is not None:
            if channel is not None:
                await channel.send(text)
            elif user is not None:
                await user.send(text)
            else:
                await ctx.send(text)
        else:
            await ctx.send('No message assigned')

    @commands.command()
    async def hi(self, ctx):
        """
        Say hi to the bot

        Command: `[p]hi` where [p] is bot prefix
        Example: `{0}hi`
        """
        await ctx.send(f'Hi, {ctx.message.author.display_name}!')


def setup(bot):
    bot.add_cog(Messaging(bot))
