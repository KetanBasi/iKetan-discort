import typing

import discord
from discord.ext import commands

from modules.core.c_core import this_bot


def embed_file_imfo(attachments):
    embed = discord.Embed(
        title="Get file",
        description=f"Len: {len(attachments)}",
        colour=discord.Colour.from_rgb(r=255, g=255, b=255)
        )
    for item in attachments:
        name = item.filename
        size = item.size
        url = item.url
        embed.add_field(name=name, value=f"File: [{name}]({url})\nSize: {size}")
    return embed


class System(commands.Cog):
    """
    System-related commands, accessible to bot owner-only.
    """

    def __init__(self, client):
        self.client = client
    
    @commands.when_mentioned_or

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
        print("⇒ shutdown invoked")
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
        message = f"Msg: {ctx.message}\n\n"\
                  f"Author: {ctx.message.author}\n"\
                  f"Bot: {ctx.bot}\n"\
                  f"Args: {ctx.args}\n"\
                  f"Kwargs: {ctx.kwargs}\n"\
                  f"Prefix: {ctx.prefix}\n"\
                  f"Command: {ctx.command}\n"
        
        if ctx.message.reference:
            message += f"Reference: {ctx.message.reference.message_id}: "\
                       f"{ctx.message.reference}\n"
        
        if ctx.message.attachments:
            message += f"Attachments: {len(ctx.message.attachments)}: "\
                       f"{ctx.message.attachments}\n"
        
        await ctx.send(message)
    
    @commands.command()
    @commands.is_owner()
    async def get_file(self, ctx):
        """
        Get file link (reply / direct)
        
        ***Usage***: `[bo]get_file`
        ***Example***: `{1}get_file`
        """
        async with ctx.typing():
            attachments = ctx.message.attachments
            reference = ctx.message.reference
            
            if not attachments or not reference:
                embed = discord.Embed(
                    title="No file attached",
                    description="No attachments detected",
                    colour=discord.Colour.from_rgb(r=255, g=255, b=255)
                    )
            
            elif attachments:
                embed = embed_file_imfo(attachments)
            
            elif reference:
                message = await ctx.channel.fetch_message(reference.message_id)
                if message.attachments:
                    embed = embed_file_imfo(message.attachments)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def say_this(self, ctx):
        """
        ***Usage***: `[bo]say_this`
        ***Example***: `{1}say_this`
        """
        reference = ctx.message.reference
        if reference:
            async with ctx.typing():
                message = await ctx.channel.fetch_message(reference.message_id)
            await ctx.send(type(message.content))
            await ctx.send(message.type)
            # if isinstance(message.content, str):
            await ctx.send(message.content)
        
        else:
            await ctx.send("Can't proceed, no message")

    @commands.command()
    @commands.is_owner()
    async def read_embed(self, ctx):
        """
        read embed message
        """
        if ctx.message.reference:
            async with ctx.typing():
                message = await ctx.channel.fetch_message(
                    ctx.message.reference.message_id)
                embeds = message.embeds
                print(len(embeds))
                for item in embeds:
                    print(type(item))
                    print(item.to_dict())
                content = [str(item.to_dict()) for item in embeds]
            for item in content:
                await ctx.send(item)
    
        else:
            await ctx.send("Error: No reference given. Please reply to a msg")


def setup(bot):
    """
    add cog to bot
    """
    bot.add_cog(System(bot))
