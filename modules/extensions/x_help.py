# ? Source: https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2
import discord
from discord.ext import commands

from main import adminPrefix, botDescription, botName, botOwner, botVersion, prefix
from modules.core import c_gif

helpColour = discord.Colour.blurple()


class Help(commands.Cog):
    """Show this help message"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, *input):
        """Shows all available category and its commands"""
        description = f"{botName} v{botVersion}" + \
            f" by {botOwner}\n" + botDescription

        if not input:  # ? Means "if the 'input' variable has no member"
            embed = discord.Embed(title="Command Categories", color=helpColour)
            cog_desc = ""
            for cog in self.client.cogs:
                cog_desc += f" ► `{cog}` {self.client.cogs[cog].__doc__}\n"
            cog_desc += f"\nUse `{prefix}input <category>` to gain more information"

            embed.add_field(name="Categories", value=cog_desc, inline=False)

            # ? Get all uncategorized commands
            uncategorized = ""
            for command in self.client.walk_commands():
                if not command.cog_name and not command.hidden:
                    command_help = command.help
                    try:
                        command_help = command_help.format(prefix, adminPrefix)
                    except AttributeError:
                        pass
                    uncategorized += f"\n ► `{command.name}` {command_help}"
            if uncategorized:
                embed.add_field(
                    name="Uncategorized commands",
                    value=uncategorized.format(prefix),
                    inline=False,
                )
            embed.add_field(name="About", value=description, inline=False)

        elif len(input) == 1:

            for cog in self.client.cogs:
                # ? If user requested info about a category / cog
                if cog.lower() == input[0].lower():
                    embed = discord.Embed(
                        title=f"{cog} - Commands",
                        description=self.client.cogs[cog].__doc__,
                        colour=helpColour,
                    )
                    availableCommands = ""
                    for command in self.client.get_cog(cog).get_commands():
                        if not command.hidden:
                            availableCommands += f"\n ► {command.name}"
                    embed.add_field(name=f"\n ► {command.name}",
                                    value="",
                                    inline=False)
                    break
                else:
                    # ? If user requested info about a specific command
                    commandFound = False
                    for command in self.client.get_cog(cog).get_commands():
                        if (not command.hidden) and (command.name.lower()
                                                     == input[0].lower()):
                            command_help = command.help
                            try:
                                command_help = command_help.format(
                                    prefix, adminPrefix)
                            except AttributeError:
                                pass
                            embed = discord.Embed(
                                title=f"{command.name} - Command",
                                value=command.help,
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{prefix}{command.name}",
                                value=command_help,
                                inline=False,
                            )
                            commandFound = True
                            break
                    if commandFound:
                        break
            else:
                # ? If user's request not found
                embed = discord.Embed(
                    title="Unknown category / command",
                    description="Please try another available" +
                    " command or report it to bot's" + " owner",
                    colour=helpColour,
                )
        elif len(input) > 1:
            # ? If user gives more input than expected
            description = ("Too much input. Currently, I could only give you" +
                           " information about one command at a time.")
            embed = discord.Embed(title="Too much input",
                                  description=description,
                                  colour=helpColour)
            embed.set_image(url=c_gif.getGif("Confused"))

        else:
            # ? If something we don't know happened
            embed = discord.Embed(
                title="It's a magical place",
                description="I don't know how you got here.\n" +
                "Would you mind to report this to" + " my creator, please?",
            )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
