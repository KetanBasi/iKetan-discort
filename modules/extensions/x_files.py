from typing import Optional

import discord
from discord.ext import commands

from modules.core import c_core
from modules.extensions.components import m_anonfiles as af


class Files(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def anonfiles(self, ctx, operation: str, file_id: Optional[str]):
        """
        Easily upload or check file availability on AnonFiles
        
        ***Usage***: `[p]anonfiles <operation> [file_id]`
        
        ***Note***:
            - ___operation___: Either "check" or "upload"
            - ___file_id___: file to upload or id to check, or reply to the target
            - Uploading multiple files not supported yet
        
        ***Example***:
            `{0}anonfiles upload (file "mynote.txt" attached)`, or
            `{0}anonfiles upload (reply to the message with the file)`, or
            `{0}anonfiles check abcde12345`, or
            `{0}anonfiles check (reply to this bot upload response)`
        """
        embed = None
        if operation.strip().lower() == "upload":
            if ctx.message.attachments:
                file_name = ctx.message.attachments[0].filename
                file_url = ctx.message.attachments[0].url
            
            elif ctx.message.reference:
                message = await ctx.channel.fetch_message(
                    ctx.message.reference.message_id)
                file_name = message.attachments[0].filename
                file_url = message.attachments[0].url
            
            else:
                embed = discord.Embed(
                    title="Invalid input",
                    description="You must attach at least one attachment",
                    colour=discord.Colour.red())
                await ctx.send(embed=embed)
                return
            
            async with ctx.typing():
                # file_content = c_core.read_url_file(file_url)
                saved_file = c_core.save_file(ctx, file_name, file_url)
                data = af.AnonFiles()
                data.upload(file=saved_file)
                if data.success:
                    description = (
                        f"File: ***{data.file_name}***\n"
                        f"ID: {data.file_id}\n"
                        f"Size: {data.file_size} Bytes\n"
                        f"Link: [{data.link}]({data.link})")
                    embed = discord.Embed(
                        title="Uploaded successfully",
                        description=description,
                        colour=discord.Colour.green())
                
                else:
                    embed = discord.Embed(
                        title="Uploaded failed",
                        description=data.msg,
                        colour=discord.Colour.red())
        
        elif operation.strip().lower() == "check":
            if file_id:
                pass
            
            elif ctx.message.reference:
                message = await ctx.channel.fetch_message(
                    ctx.message.reference.message_id)
                content = message.embeds[0].to_dict()
                description = content["description"].splitlines()
                for line in description:
                    if line.startswith("ID: "):
                        file_id = line.replace("ID: ", "")
                        break
            
            else:
                embed = discord.Embed(
                    title="Invalid input",
                    description="You must attach at least one attachment",
                    colour=discord.Colour.red())
                await ctx.send(embed=embed)
                return
            
            async with ctx.typing():
                data = af.AnonFiles()
                data.check_status(file_id=file_id)
                if data.success:
                    description = (
                        f"File: ***{data.file_name}***\n"
                        f"ID: {data.file_id}\n"
                        f"Size: {data.file_size} Bytes\n"
                        f"Link: [{data.link}]({data.link})")
                    embed = discord.Embed(
                        title="Uploaded successfully",
                        description=description,
                        colour=discord.Colour.green())
                
                else:
                    embed = discord.Embed(
                        title="File not found",
                        description="Probably file not uploaded",
                        colour=discord.Colour.red())
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Files(bot))
