"""
Some example of commands that can be used to interact with the database.
"""
from typing import Optional

from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions

from utils import checks
from utils.cog_class import Cog
from utils.ctx_class import MyContext
from utils.models import get_from_db


class DatabaseCommands(Cog):
    @commands.command()
    async def how_many(self, ctx: MyContext):
        """
        Say hi with a customisable hello message. This is used to demonstrate cogs config usage
        """
        _ = await ctx.get_translate_function()
        db_user = await get_from_db(ctx.author, as_user=True)
        db_user.times_ran_example_command += 1
        await db_user.save()
        await ctx.send(_("You ran that command {times_ran_example_command} times already!",
                         times_ran_example_command=db_user.times_ran_example_command
                         ))

    @commands.command()
    @checks.has_permission("discord.administrator")
    async def prefix(self, ctx: MyContext, new_prefix: Optional[str] = None):
        """
        Change/view the server prefix.
        """
        _ = await ctx.get_translate_function()
        db_guild = await get_from_db(ctx.guild)
        if new_prefix:
            db_guild.prefix = new_prefix
        await db_guild.save()
        if db_guild.prefix:
            await ctx.send(_("The server prefix is set to `{prefix}`.",
                             prefix=escape_mentions(escape_markdown(db_guild.prefix))
                             ))
        else:
            await ctx.send(_("There is no specific prefix set for this guild."))


setup = DatabaseCommands.setup
