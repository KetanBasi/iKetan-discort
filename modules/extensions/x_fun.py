import random
import statistics
from typing import Optional, Union

import discord
from discord.ext import commands

from modules.extensions.components import m_age_nation, m_bored, m_code_stats, m_tenor


class Fun(commands.Cog):
    """Some fun commands"""

    def __init__(self, client):
        self.client = client

    # ? ==================
    # ? Commands
    # ? ==================
    @commands.command(
        aliases=["gifs", "getgif", "getgifs", "findgif", "findgifs"])
    async def gif(self, ctx, *, keyword):
        """
        Get yourself a GIF

        ***Usage***:
            `[p]gif <keyword>` where [p] is bot prefix, or
            `[p]gif <keyword>|[message]`
        ***Example***: `{0}gif hugs` or `{0}gif happy birthday|Happy birthday @Jane`
        """
        async with ctx.typing():
            if "|" in keyword:
                message = keyword.split("|")[1].strip()
                keyword = keyword.split("|")[0].strip()
                embed = discord.Embed(description=message,
                                      colour=discord.Colour.green())
            else:
                embed = discord.Embed(colour=discord.Colour.green())
            embed.set_image(url=m_tenor.get_gif(keyword))
            embed.set_footer(
                text=f"Requested by {ctx.message.author.display_name}",
                icon_url=ctx.message.author.avatar_url_as(size=128),
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=["hugs"], description="Hug someone")
    async def hug(self, ctx, user: Optional[discord.User] = None):
        """
        Hugs someone

        ***Usage***: `[p]hug [user]`
        ***Example***: `{0}hug <@someone#1234>`
        """
        async with ctx.typing():
            if user is not None:
                description = f"{ctx.message.author.display_name} hugs <@!{user.id}>"

            else:
                description = f"I hug you, {ctx.message.author.display_name}"

            message = discord.Embed(description=description,
                                    colour=discord.Colour.green())
            message.set_image(url=m_tenor.get_gif("hugs"))
            message.set_footer(
                text=f"Requested by {ctx.message.author.display_name}",
                icon_url=ctx.message.author.avatar_url_as(size=128),
            )
        await ctx.send(embed=message)

    @commands.command(aliases=["slaps"], description="Slap someone")
    async def slap(self, ctx, user: Optional[discord.User] = None):
        """
        Slaps someone

        ***Usage***: `[p]slap [user]`
        ***Example***: `{0}slap <@someone#1234>`
        """
        async with ctx.typing():
            if user is not None:
                description = f"{ctx.message.author.display_name} slaps <@!{user.id}>"

            else:
                description = f"I slap you, {ctx.message.author.display_name}!"

            message = discord.Embed(description=description,
                                    colour=discord.Colour.green())
            message.set_image(url=m_tenor.get_gif("slaps"))
            message.set_footer(
                text=f"Requested by {ctx.message.author.display_name}",
                icon_url=ctx.message.author.avatar_url_as(size=128),
            )
        await ctx.send(embed=message)

    @commands.command(aliases=["flipcoin"], description="Flip a coin")
    async def coin(self, ctx, count: Optional[int] = 1):
        """
        Flip a coin

        ***Usage***: `[p]coin <number>` where [p] is bot prefix
        ***Example***: `{0}coin 3` which means *flip a coin 3 times*
        """
        async with ctx.typing():
            sides = ("head", "tail")

            if count >= 1:
                results = [random.choice(sides) for _ in range(count)]
                # await ctx.send(', '.join(results))
                embed = discord.Embed(title="Coin Flip",
                                      colour=discord.Colour.green())
                embed.add_field(name="Result:",
                                value=", ".join(results),
                                inline=False)

                if count >= 2:
                    head_count = results.count("head")
                    tail_count = results.count("tail")
                    count = f"> Head: {head_count}\n> Tail: {tail_count}"
                    embed.add_field(name="Count:", value=count, inline=False)
                embed.set_footer(
                    text=f"Flipped by {ctx.message.author.display_name}",
                    icon_url=ctx.message.author.avatar_url_as(size=128),
                )

            else:
                embed = discord.Embed(
                    title="Invalid argument",
                    description="Please insert positive value more than **0**",
                    colour=discord.Colour.red(),
                )
        await ctx.send(embed=embed)

    @commands.command(aliases=["rolldice", "diceroll"],
                      description="Roll a dice")
    async def dice(self,
                   ctx,
                   rolls: Optional[int] = 1,
                   diceSides: Optional[int] = 6):
        """
        Roll a dice

        ***Usage***: `[p]dice <rolls> [diceSide]` where [p] is bot prefix
            __rolls__: how many time you roll the dice
            __diceSide__: how many side the dice has (default: 6)
        ***Example***:
            `{0}dice 3 12` which means *roll a dice with 12 sides 3 times*
            or
            `{0}dice 5` which means *roll a dice with 6 sides 5 times*
        """
        async with ctx.typing():
            if diceSides >= 2:
                if 1 <= rolls <= 100:
                    results = [
                        random.randint(1, diceSides) for _ in range(rolls)
                    ]
                    embed = discord.Embed(title="Dice Rolls",
                                          color=discord.Colour.orange())
                    embed.add_field(
                        name="Result:",
                        value=", ".join([str(num) for num in results]),
                        inline=False,
                    )

                    if rolls > 1:
                        max_val = max(results)
                        mode = statistics.mode(results)
                        stats = f"> Max: {max_val}\n> Mode: {mode}"
                        embed.add_field(name="Statistics:",
                                        value=stats,
                                        inline=False)

                else:
                    embed = discord.Embed(
                        title="Invalid value",
                        description="Too many rolls",
                        colour=discord.Colour.red(),
                    )

            else:
                if diceSides == 1:
                    message = "Is this a joke? I don't have any mobius strip"

                elif diceSides == 2:
                    message = "Hmm, use a coin instead"

                else:
                    message = "Wait, what?"

                embed = discord.Embed(
                    title="Invalid value",
                    description=message,
                    colour=discord.Colour.red(),
                )

        await ctx.send(embed=embed)

    @commands.command()
    async def bored(self, ctx, participants: Optional[Union[int, str]], *, _):
        """
        Feel bored? Find new activity

        ***Usage***: `[p]bored [participants]`
        ***Example***: `{0}bored` or `{0}bored 3`
        """
        async with ctx.typing():
            activity = m_bored.get_activity(participants=participants)
            link = f"\nLink: {activity.link}" if activity.link != "" else ""
            embed = discord.Embed(
                title=activity.activity,
                description=f"Participants: {activity.participants}\n"
                f"Type: {activity.type}" + link,
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def agify(self, ctx, *, name: Optional[str] = None):
        """
        I'll try to predict your age from your name

        ***Usage***: `[p]agify <name>`

        ***Note***:
        ___name___: should only consist of alphabet (which means no space or symbols)

        ***Example***:
        `ketan.agify` which means predict my age from my discord name
        `ketan.agify JohnDoe` wich means predict my age from my real name (John Doe)
        """
        async with ctx.typing():
            if not name:
                name = ctx.author.display_name
            name = name.replace(" ", "")
            result = m_age_nation.get_age(name=name)
            embed = discord.Embed(title=f'Age prediction for "{name}"',
                                  description=f"Age: {result}")
        await ctx.send(embed=embed)

    @commands.command()
    async def nationalize(self, ctx, *, name: Optional[str]):
        """
        I'll try to predict your nationality from your name

        ***Usage***: `[p]nationalize <name>`

        ***Note***:
        ___name___: should only consist of alphabet (which means no space or symbols)

        ***Example***:
        `ketan.nationalize` which means predict my nationality from my discord name
        `ketan.nationalize JohnDoe` which means predict my nationality from my real name (John Doe)
        """
        async with ctx.typing():
            if not name:
                name = ctx.author.display_name
            name = name.replace(" ", "")
            result = m_age_nation.get_nation(name=name)
            embed = discord.Embed(
                title=f'Nationality prediction for "{name}"',
                description="Prediction Result:",
            )

            if len(result) > 0:
                for nation in result:
                    embed.add_field(name=nation.country_id,
                                    value=nation.probability)

            else:
                embed.add_field(name="Can't predict", value="Try other name")
        await ctx.send(embed=embed)

    @commands.command(aliases=["cs"])
    async def codestats(self, ctx, users: Optional[str]):
        """
        Get Code::Stats info

        ***Usage***: `[p]codestats [username]`
        ***Example***: `{0}codestats` or `{0}codestats KetanBasi`
        """
        async with ctx.typing():
            if not users:
                users = ctx.message.author.display_name
            stats = m_code_stats.get_user_stats(users)
            desc = (f"New XP: {stats.new_xp}\n"
                    f"Total XP: {stats.total_xp}\n"
                    f"Last Code: {stats.last_code}\n"
                    f"Highest: {stats.max_stat[0]} ({stats.max_stat[1]})")
            links = (f"[View User's Page]({stats.user_page})\n"
                     f"[Code::Stats]({m_code_stats.code_stats})")
            embed = discord.Embed(
                title=f"{stats.username}'s stats",
                description=desc,
                colour=discord.Colour.from_rgb(r=255, g=255, b=255),
            )
            embed.add_field(name="Links", value=links, inline=False)
            for lang in stats.languages:
                embed.add_field(name=lang,
                                value=f"***{stats.languages[lang]}*** xp")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
