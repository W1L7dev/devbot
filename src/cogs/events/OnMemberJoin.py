from nextcord import Color, Embed, Member, utils
from nextcord.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """When a member joins, send a message and give them the member role

        Args:
          member (Member): The member
        """
        channel = self.bot.get_channel(self.bot.config.get("welcome_channel"))
        role = utils.get(
            member.guild.roles, name=self.bot.config.get("member_role_name")
        )
        await channel.send(
            embed=Embed(
                title="Welcome",
                description=f"Welcome to the server, {member.mention}!",
                color=getattr(Color, self.bot.config.get("default_embed_color"))(),
            )
        )
        await self.bot.log(
            title="Member Joined", description=f"{member.mention} joined the server."
        )
        await member.add_roles(role)


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
