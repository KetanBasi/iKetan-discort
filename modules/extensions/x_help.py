# ? Source: https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
import discord
from discord.ext import commands

from modules.core.c_core import this_bot
from modules.extensions.components import m_tenor

helpColour = discord.Colour.blurple()


class Help(commands.Cog):
    """
    Show this help message
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
            description = f"{this_bot.name} v{this_bot.version}" \
                          + f" by {this_bot.owner}\n"+this_bot.description

            # ? If the 'keyword' variable has no value(s)
            if not keyword:
                cog_desc = ''
                for cog in self.client.cogs:
                    cog_doc = self.client.cogs[cog].__doc__
                    cog_desc += f" ► `{cog}` {cog_doc.strip()}\n"
                cog_desc += f"\nUse `{this_bot.prefix}keyword <category>` to gain more information"
                embed = discord.Embed(
                    title="Command Categories",
                    color=helpColour
                    )
                embed.add_field(
                    name="Categories",
                    value=cog_desc,
                    inline=False
                    )
    
                # ? Get all uncategorized commands
                uncategorized = ""
                for command in self.client.walk_commands():
                    if not command.cog_name and not command.hidden:
                        command_help = command.help
                        try:
                            command_help = command_help.format(this_bot.prefix, this_bot.admin_prefix)
                        
                        except AttributeError:
                            pass
                        
                        finally:
                            uncategorized += f"\n ► `{command.name}` {command_help}"
                
                if uncategorized:
                    embed.add_field(
                        name="Uncategorized commands",
                        value=uncategorized.format(this_bot.prefix),
                        inline=False
                        )
                
                # ? Add bot description
                embed.add_field(
                    name="About",
                    value=description,
                    inline=False
                    )
    
            elif len(keyword) == 1:
    
                for cog in self.client.cogs:
                    
                    # ? If user requested info about a category / cog
                    if cog.lower() == keyword[0].lower():
                        availableCommands = ""
                        for command in self.client.get_cog(cog).get_commands():
                            if not command.hidden:
                                availableCommands += f"\n ► {command.name}"

                        embed = discord.Embed(
                            title=f"Category: {cog}",
                            description=self.client.cogs[cog].__doc__,
                            colour=helpColour
                            )
                        embed.add_field(
                            name="Available Commands:",
                            value=availableCommands,
                            inline=False
                            )
                        break
    
                    # ? If user requested info about a specific command
                    else:
                        commandFound = False
                        for command in self.client.get_cog(cog).get_commands():
                            if (not command.hidden)\
                                    and (command.name.lower() == keyword[0].lower()):
                                command_help = command.help
                                try:
                                    command_help = command_help.format(this_bot.prefix, this_bot.admin_prefix)
                                
                                except AttributeError:
                                    pass
                                
                                commandFound = True
                                embed = discord.Embed(
                                    title=f"Command: {command.name}",
                                    value=command.help,
                                    inline=False
                                    )
                                embed.add_field(
                                    name=f"{this_bot.prefix}{command.name}",
                                    value=command_help,
                                    inline=False
                                    )
                                break
                        
                        if commandFound:
                            break
    
                # ? If user's request not found
                else:
                    embed = discord.Embed(
                        title="Unknown category / command",
                        description="Please try another available"
                                    + " command or report it to bot\'s"
                                    + " owner",
                        colour=helpColour
                        )
    
            # ? If user gives more keyword than expected
            elif len(keyword) > 1:
                description = "Too much keyword. Currently, I could only give you"\
                              + " information about one command at a time."
                embed = discord.Embed(
                    title="Too much keyword",
                    description=description,
                    colour=helpColour
                    )
                embed.set_image(url=m_tenor.get_gif("Confused"))
    
            # ? If something we don't know happened
            else:
                embed = discord.Embed(
                    title="It\'s a magical place",
                    description="I don\'t know how you got here.\n"
                                + "Would you mind to report this to"
                                + " my creator, please?"
                    )

        await ctx.send(embed=embed)


def setup(bot):
    """
    add cog to bot
    """
    bot.add_cog(Help(bot))
