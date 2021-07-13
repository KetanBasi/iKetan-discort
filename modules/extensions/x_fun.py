import random
import statistics
import typing
import discord
from discord.ext import commands

from modules.core import c_gif


class Fun(commands.Cog):
    """Some fun commands"""
    def __init__(self, client):
        self.client = client

    # ? ==================
    # ? Commands
    # ? ==================
    @commands.command(aliases=['gifs', 'getgif', 'getgifs', 'findgif', 'findgifs'],
                      descriptiom='Find a GIF')
    async def gif(self,
                  ctx,
                  *,
                  keyword):
        """
        Get yourself a GIF

        Command: `[p]gif <keyword>` where [p] is bot prefix,
                or
                `[p]gif <keyword>|[message]`
        Example: `{0}gif happy birthday` or `{0}gif hugs`
        """
        if '|' in keyword:
            message = keyword.split('|')[1].strip()
            keyword = keyword.split('|')[0].strip()
            embed = discord.Embed(description=message,
                                  colour=discord.Colour.green()
                                  )
        else:
            embed = discord.Embed(colour=discord.Colour.green())
        embed.set_image(url=c_gif.getGif(keyword))
        embed.set_footer(text=f'Requested by {ctx.message.author.display_name}',
                         icon_url=ctx.message.author.avatar_url_as(size=128))
        await ctx.send(embed=embed)

    @commands.command(aliases=['hugs'],
                      description='Hug someone')
    async def hug(self,
                  ctx,
                  user: typing.Optional[discord.User] = None
                  ):
        """
        Hugs someone

        Command: `[p]hug [user]`
        Example: `{0}hug <@someone#1234>`
        """
        if user is not None:
            description = f'{ctx.message.author.display_name} hugs <@!{user.id}>'
        else:
            description = f'I hug you, {ctx.message.author.display_name}'
        message = discord.Embed(description=description,
                                colour=discord.Colour.green()
                                )
        message.set_image(url=c_gif.getGif('hugs'))
        message.set_footer(text=f'Requested by {ctx.message.author.display_name}',
                           icon_url=ctx.message.author.avatar_url_as(size=128))
        await ctx.send(embed=message)

    @commands.command(aliases=['slaps'],
                      description='Slap someone')
    async def slap(self,
                   ctx,
                   user: typing.Optional[discord.User] = None
                   ):
        """
        Slaps someone

        Command: `[p]slap [user]`
        Example: `{0}slap <@someone#1234>`
        """
        if user is not None:
            description = f'{ctx.message.author.display_name} slaps <@!{user.id}>'
        else:
            description = f'I slap you, {ctx.message.author.display_name}!'
        message = discord.Embed(description=description,
                                colour=discord.Colour.green()
                                )
        message.set_image(url=c_gif.getGif('slaps'))
        message.set_footer(text=f'Requested by {ctx.message.author.display_name}',
                           icon_url=ctx.message.author.avatar_url_as(size=128))
        await ctx.send(embed=message)

    @commands.command(aliases=['flipcoin'],
                      description='Flip a coin'
                      )
    async def coin(self,
                   ctx,
                   count: typing.Optional[int] = 1
                   ):
        """
        Flip a coin

        Command: `[p]coin <number>` where [p] is bot prefix
        Example: `{0}coin 3` which means *flip a coin 3 times*
        """
        sides = ('head', 'tail')
        results = []
        if count >= 1:
            for i in range(count):
                results.append(random.choice(sides))
            # await ctx.send(', '.join(results))
            embed = discord.Embed(title='Coin Flip',
                                  colour=discord.Colour.green()
                                  )
            embed.add_field(name='Result:',
                            value=', '.join(results),
                            inline=False
                            )
            if count >= 2:
                headCount = results.count('head')
                tailCount = results.count('tail')
                count = f'> Head: {headCount}\n> Tail: {tailCount}'
                embed.add_field(name='Count:',
                                value=count,
                                inline=False
                                )
            embed.set_footer(text=f'Flipped by {ctx.message.author.display_name}',
                             icon_url=ctx.message.author.avatar_url_as(size=128)
                             )
            await ctx.send(embed=embed)
        else:
            await ctx.send('Invalid argument, please insert positive value more than **0**')

    @commands.command(aliases=['rolldice', 'diceroll'],
                      description='Roll a dice')
    async def dice(self,
                   ctx,
                   rolls: typing.Optional[int] = 1,
                   diceSides: typing.Optional[int] = 6
                   ):
        """
        Roll a dice

        Command: `[p]dice <rolls> [diceSide]` where [p] is bot prefix
        **rolls**: how many time you roll the dice
        **diceSide**: how many side the dice has (default: 6)
        Example:
            `{0}dice 3 12` which means *roll a dice with 12 sides 3 times*
            or
            `{0}dice 5` which means *roll a dice with 6 sides 5 times*
        """
        if diceSides >= 2:
            if 1 <= rolls <= 100:
                embed = discord.Embed(title='Dice Rolls',
                                      color=discord.Colour.orange()
                                      )
                results = [random.randint(1, diceSides) for _ in range(rolls)]
                embed.add_field(name='Result:',
                                value=', '.join([str(num) for num in results]),
                                inline=False
                                )
                if rolls > 1:
                    maxVal = max(results)
                    mode = statistics.mode(results)
                    stats = f'> Max: {maxVal}\n> Mode: {mode}'
                    embed.add_field(name='Statistics:',
                                    value=stats,
                                    inline=False,
                                    )
                embed.set_footer(text=f'Dice rolls by {ctx.message.author.display_name}',
                                 icon_url=ctx.message.author.avatar_url_as(size=128))
                await ctx.send(embed=embed)
            else:
                await ctx.send('I\'m confused, too many rolls')
        else:
            if diceSides == 1:
                message = 'Is this a joke? I don\'t have any mobius strip'
            elif diceSides == 2:
                message = 'Hmm, use a coin instead'
            else:
                message = 'Wait, what?'
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Fun(bot))
