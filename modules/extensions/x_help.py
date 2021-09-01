# ? Source: https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
import discord
from discord.ext import commands

from modules.core.c_core import this_bot
from modules.extensions.components import m_tenor

help_colour = discord.Colour.blurple()


class Help(commands.Cog):
    """
    Help commands
    """

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *keyword):
        """
        Shows all available category and its commands

        ***Usage***:
        `[p]help` where ___[p]___ is bot prefix,
        `[p]help [category]`, or
        `[p]help [command]`

        ***Example***:
        `{0}help fun` or `{0}help gif`
        """
        async with ctx.typing():
            description = (f"{this_bot.name} v{this_bot.version}" +
                           f" by {this_bot.owner}\n" + this_bot.description)

            # ? If the 'keyword' variable has no value(s)
            if not keyword:
                cog_desc = ""
                for cog in self.client.cogs:
                    cog_doc = self.client.cogs[cog].__doc__
                    try:
                        cog_doc = cog_doc.strip()
                    except AttributeError:
                        pass
                    cog_desc += f" ► `{cog}` {cog_doc}\n"
                cog_desc += f"\nUse `{this_bot.prefix}keyword <category>` to gain more information"
                embed = discord.Embed(title="Command Categories",
                                      color=help_colour)
                embed.add_field(name="Categories",
                                value=cog_desc,
                                inline=False)

                # ? Get all uncategorized commands
                uncategorized = ""
                for command in self.client.walk_commands():
                    if not command.cog_name and not command.hidden:
                        command_help = command.help
                        try:
                            command_help = command_help.format(
                                this_bot.prefix, this_bot.admin_prefix)

                        except AttributeError:
                            pass

                        finally:
                            uncategorized += f"\n ► `{command.name}` {command_help}"

                if uncategorized:
                    embed.add_field(
                        name="Uncategorized commands",
                        value=uncategorized.format(this_bot.prefix),
                        inline=False)

                # ? Add bot description
                embed.add_field(name="About", value=description, inline=False)

            elif len(keyword) == 1:

                for cog in self.client.cogs:

                    # ? If user requested info about a category / cog
                    if cog.lower() == keyword[0].lower():
                        available_commands = ""
                        for command in self.client.get_cog(cog).get_commands():
                            if not command.hidden:
                                available_commands += f"\n ► {command.name}"

                        embed = discord.Embed(
                            title=f"Category: {cog}",
                            description=self.client.cogs[cog].__doc__,
                            colour=help_colour)
                        embed.add_field(
                            name="Available Commands:",
                            value=available_commands,
                            inline=False)
                        break

                    command_found = False
                    for command in self.client.get_cog(cog).get_commands():
                        if (not command.hidden) and (command.name.lower()
                                                     == keyword[0].lower()):
                            command_help = command.help
                            try:
                                command_help = command_help.format(
                                    this_bot.prefix, this_bot.admin_prefix)

                            except AttributeError:
                                pass

                            command_found = True
                            embed = discord.Embed(
                                title=f"Command: {command.name}",
                                value=command.help,
                                inline=False)
                            embed.add_field(
                                name=f"{this_bot.prefix}{command.name}",
                                value=command_help,
                                inline=False)
                            break

                    if command_found:
                        break

                # ? If user's request not found
                else:
                    embed = discord.Embed(
                        title="Unknown category / command",
                        description="Please try another available" +
                        " command or report it to bot's" + " owner",
                        colour=help_colour)

            # ? If user gives more keyword than expected
            elif len(keyword) > 1:
                description = (
                    "Too much keyword. Currently, I could only give you" +
                    " information about one command at a time.")
                embed = discord.Embed(title="Too much keyword",
                                      description=description,
                                      colour=help_colour)
                embed.set_image(url=m_tenor.get_gif("Confused"))

            # ? If something we don't know happened
            else:
                embed = discord.Embed(
                    title="It's a magical place",
                    description="I don't know how you got here.\n" +
                    "Would you mind to report this to" +
                    " my creator, please?",
                    colour=help_colour)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def about(self, ctx):
        """
        About this bot
        
        ***Usage***: `[p]about`
        ***Example***: `{0}about`
        """
        async with ctx.typing():
            embed = discord.Embed(
                title=this_bot.name,
                description=this_bot.description,
                colour=help_colour)
            embed.add_field(
                name="Bot owner",
                value=this_bot.owner)
            embed.add_field(
                name="Bot version",
                value=this_bot.version)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def contact(self, ctx):
        """
        Contact bot owner
        
        ***Usage***: `[p]contact`
        ***Example***: `{0}contact`
        """
        async with ctx.typing():
            embed = discord.Embed(
                title="Contact",
                description="",
                colour=help_colour
                )
            embed.add_field(
                name="Discord",
                value=this_bot.owner
                )
        await ctx.send(embed=embed)


def setup(bot):
    """
    add cog to bot
    """
    bot.add_cog(Help(bot))
