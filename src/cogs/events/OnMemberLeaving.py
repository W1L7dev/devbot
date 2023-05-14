from nextcord import Color, Embed, Member
from nextcord.ext import commands


class OnMemberLeaving(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        """When a member leaves, send a message

        Args:
          member (Member): The member
        """
        channel = self.bot.get_channel(self.bot.config.get("leaving_channel"))
        await channel.send(
            embed=Embed(
                title="Goodbye",
                description=f"Goodbye, {member.mention}!",
                color=getattr(Color, self.bot.config.get("default_embed_color"))(),
            )
        )
        await self.bot.log(
            title="Member Left", description=f"{member.mention} left the server."
        )


def setup(bot):
    bot.add_cog(OnMemberLeaving(bot))
