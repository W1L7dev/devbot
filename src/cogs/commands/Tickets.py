from nextcord import (Embed, Interaction, RawReactionActionEvent,
                      slash_command, utils)
from nextcord.ext import application_checks, commands


class Tickets(commands.Cog):
    """Ticket commands

    Commands:
        ticket: Create a ticket
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ticket", description="Create a ticket")
    @application_checks.has_guild_permissions(manage_channels=True)
    async def ticket(self, inter: Interaction):
        """Create a ticket

        Args:
          inter (Interaction): The interaction
        """
        msg = await self.bot.standard_response(
            inter,
            title="Ticket",
            description="React to this message to create a ticket",
        )
        f = await msg.fetch()
        await f.add_reaction("🎟️")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """Create a ticket when a user reacts to a message

        Args:
          payload (RawReactionActionEvent): The reaction event
        """
        if payload.member.bot:
            return
        if payload.emoji.name == "🎟️":
            guild = self.bot.get_guild(payload.guild_id)
            channel = await guild.create_text_channel(
                f"ticket-{payload.member.name}",
                category=utils.get(
                    guild.categories, name=self.bot.config.get("ticket_category")
                ),
            )
            await channel.set_permissions(
                payload.member, read_messages=True, send_messages=True
            )
            msg = await channel.send(
                embed=Embed(
                    title="Ticket",
                    description=f"{payload.member.mention}'s ticket\nClick on ❌ to close the ticket",
                )
            )
            f = await msg.fetch()
            await f.add_reaction("❌")
        elif payload.emoji.name == "❌":
            channel = self.bot.get_channel(payload.channel_id)
            if channel.name.startswith("ticket-"):
                await channel.delete()


def setup(bot):
    bot.add_cog(Tickets(bot))
