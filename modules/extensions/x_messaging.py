import random
from typing import Optional, Union

import discord
from discord.ext import commands


class Messaging(commands.Cog):
    """Messaging commands"""

    def __init__(self, client):
        self.client = client
        self.hi_msg = [line.strip() for line in open("assets/hi").readlines()]

    @commands.command()
    async def say(self, ctx, target: Optional[Union[discord.User,
                                                    discord.Guild]], *,
                  message: str):
        """
        Too shy to say something? I'll say it for you

        ***Usage***: `[p]say [target] <messages>` where ___[p]___ is bot prefix
        ***Example***:
            `{0}say Hello world`, or
            `{0}say #public_room Hello guys`, or
            `{0}say @mylove Good morning`
        """
        if target:
            await target.send(message)

        else:
            await ctx.send(message)

    @commands.command()
    async def hi(self, ctx, *, _):
        """
        Say hi

        ***Usage***: `[p]hi`
        ***Example***: `{0}hi`
        """
        message = random.choice(self.hi_msg)
        await ctx.send(message)

    @commands.command()
    async def delete(self, ctx, target: Optional[Union[str, int]], *, _):
        """
        Delete a message either with message ID, url, or reply to the message

        ***Usage***:
            `[p]delete [message_id]` either with message_id or reply the target
        ***Example***:
            `{0}delete 987654321987654321`, or
            reply with `{0}delete` to the message target
        """
        # TODO: Delete these three lines for "delete" command
        not_implemented = True
        if not_implemented:
            raise NotImplementedError("delete command is not implemented")
        
        if target:
            async with ctx.typing():
                # location = ctx.message.
                if isinstance(target, str) and target.startswith("https://"):
                    target = target.split("/")[-1]
    
                # message = commands.MessageConverter.convert(ctx=ctx, argument=target)
                # message.delete()
            await ctx.message.delete()

    # @commands.command()
    # async def up(self, ctx):
    #     """
    #     Cover the things you don't want to see
    #
    #
    #     """


def setup(bot):
    bot.add_cog(Messaging(bot))
