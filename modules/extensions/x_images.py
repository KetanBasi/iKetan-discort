# import random
import discord
from discord.ext import commands
from typing import Optional

from modules.extensions.components import m_unsplash


def make_embed(pic, title, image_info, image_links):
    embed = discord.Embed(
        title=title,
        description=pic.desc,
        color=discord.Color.from_rgb(
            r=pic.color.red,
            g=pic.color.green,
            b=pic.color.blue
            )
        )
    embed.add_field(
        name="Image Info",
        value=image_info
        )
    embed.add_field(
        name="Links",
        value=image_links
        )
    embed.set_image(url=pic.link.thumbnail)
    embed.set_footer(
        text=f"Photo by {pic.author.name} on Unsplash",
        icon_url=pic.author.profile_pic
        )
    return embed


class Images(commands.Cog):
    """Image search"""
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=["image"])
    async def pic(self, ctx, *, keyword):
        """
        Search image from [Unsplash](https://unsplash.com/?utm_source=iKetan-dct&utm_medium=referral)
        
        ***Usage***: `[p]pic <keyword>`
        ***Example***: `{0}pic cute` or `{0}pic beach`
        """
        async with ctx.typing():
            content_filter = "low" if ctx.channel.nsfw else "high"
            pic = m_unsplash.find_image(
                keyword=keyword,
                content_filter=content_filter
                )
            title = f"Search result for {keyword}"
            image_info = f"Dimension: {pic.dimension.__str__()}\n" \
                         f"Likes: {pic.likes}\n" \
                         f"Tags:"
            for tag in pic.tags:
                image_info += f" `{tag}`"
            image_links = f"[View Image]({pic.link.source})\n" \
                          f"[See Full Resolution Image]({pic.link.download})\n" \
                          f"[Go to Photographer's Page]({pic.link.author})\n" \
                          f"[Go to Unsplash]({m_unsplash.unsplash_link})"
            embed = make_embed(pic, title, image_info, image_links)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["rpic"])
    async def random_pic(self, ctx, *, keyword: Optional[str] = ""):
        """
        Get random image from [Unsplash](https://unsplash.com/?utm_source=iKetan-dct&utm_medium=referral)
        
        ***Usage***: `[p]random_pic` or `[p]rpic`
        ***Example***: `{0}random_pic` or `{0}rpic`
        """
        async with ctx.typing():
            content_filter = "low" if ctx.channel.nsfw else "high"
            pic = m_unsplash.find_image(
                keyword=keyword,
                content_filter=content_filter,
                _random=True
                )
            title = "Random search result"
            image_info = f"Dimension: {pic.dimension.__str__()}\n" \
                         f"Likes: {pic.likes}\n"
            image_links = f"[View Image]({pic.link.source})\n" \
                          f"[See Full Resolution Image]({pic.link.download})\n" \
                          f"[Go to Photographer's Page]({pic.link.author})\n" \
                          f"[Go to Unsplash]({m_unsplash.unsplash_link})"
            embed = make_embed(pic, title, image_info, image_links)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
