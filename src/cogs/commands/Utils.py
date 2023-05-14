import asyncio
import random

from nextcord import (Color, Embed, Interaction, Member, SlashOption,
                      slash_command)
from nextcord.ext import application_checks, commands


class Utils(commands.Cog):
    """Utility commands

    Commands:
        ping: Get the bot's latency
        say: Make the bot say something
        embed: Make the bot send an embed
        nick: Change your nickname
        resetnick: Reset your nickname
        avatar: Get a user's avatar
        giveaway: Start a giveaway
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping", description="Get the bot's latency")
    async def ping(self, inter: Interaction):
        """Get the bot's latency

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Pong 🏓!",
            description=f"Latency: {round(self.bot.latency * 1000)}ms",
        )

    @slash_command(name="say", description="Make the bot say something")
    async def say(
        self,
        inter: Interaction,
        message: str = SlashOption(
            name="message",
            description="The message to send",
        ),
    ):
        """Make the bot say something

        Args:
          inter (Interaction): The interaction
          message (str): The message to send. Defaults to SlashOption(name="message", description="The message to send").
        """
        await inter.response.send_message(message)

    @slash_command(name="embed", description="Make the bot send an embed")
    async def embed(
        self,
        inter: Interaction,
        title: str = SlashOption(name="title", description="The title of the embed"),
        message: str = SlashOption(
            name="message", description="The message of the embed"
        ),
    ):
        """Make the bot send an embed

        Args:
          inter (Interaction): The interaction
          title (str): The title of the embed. Defaults to SlashOption(name="title", description="The title of the embed").
          message (str): The message of the embed. Defaults to SlashOption(name="message", description="The message of the embed").
          color (str): The color of the embed. Defaults to SlashOption(name="color", description="The color of the embed", choices=["red", "orange", "yellow", "green", "blue", "purple", "pink", "white", "black", "brown", "teal", "blurple", "greyple"]).
        """
        await self.bot.standard_response(inter, title=title, description=message)

    @slash_command(name="nick", description="Change your nickname")
    async def nick(
        self,
        inter: Interaction,
        nickname: str = SlashOption(
            name="nickname", description="The nickname to change to"
        ),
    ):
        """Change your nickname

        Args:
          inter (Interaction): The interaction
          nickname (str): The nickname to change to. Defaults to SlashOption(name="nickname", description="The nickname to change to").
        """
        await inter.user.edit(nick=nickname)
        await self.bot.standard_response(
            inter,
            title="Nickname changed",
            description=f"Changed nickname to **{nickname}**",
        )

    @slash_command(name="resetnick", description="Reset your nickname")
    async def resetnick(self, inter: Interaction):
        """Reset your nickname

        Args:
          inter (Interaction): The interaction
        """
        await inter.user.edit(nick=None)
        await self.bot.standard_response(
            inter, title="Nickname reset", description="Reset nickname"
        )

    @slash_command(name="avatar", description="Get a user's avatar")
    async def avatar(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member to get the avatar of", required=False
        ),
    ):
        """Get a user's avatar

        Args:
          inter (Interaction): The interaction
          member (Member, optional): The member to get the avatar of. Defaults to SlashOption(name="member", description="The member to get the avatar of", required=False).
        """
        if not member:
            member = inter.user
        embed = Embed(title=f"**{member.name}**'s avatar", color=Color.blurple())
        embed.set_image(url=member.avatar.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="giveaway", description="Start a giveaway")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def giveaway(
        self,
        inter: Interaction,
        time: int = SlashOption(
            name="time", description="The time the giveaway will last"
        ),
        modifier: str = SlashOption(
            name="modifier",
            description="The modifier for the time",
            choices={
                "seconds": "s",
                "minutes": "m",
                "hours": "h",
                "days": "d",
                "weeks": "w",
            },
        ),
        prize: str = SlashOption(
            name="prize", description="The prize for the giveaway"
        ),
        winners: int = SlashOption(
            name="winners",
            description="The number of winners",
        ),
    ):
        """Start a giveaway

        Args:
          inter (Interaction): The interaction
          time (int): The time the giveaway will last. Defaults to SlashOption(name="time", description="The time the giveaway will last").
          modifier (str): The modifier for the time. Defaults to SlashOption(name="modifier", description="The modifier for the time", choices={"seconds": "s", "minutes": "m", "hours": "h", "days": "d", "weeks": "w"}).
          prize (str): The prize for the giveaway. Defaults to SlashOption(name="prize", description="The prize for the giveaway").
          winners (int): The number of winners. Defaults to SlashOption(name="winners", description="The number of winners").
        """
        embed = Embed(title="Giveaway! 🎉", color=Color.green())
        embed.add_field(name="Prize: ", value=prize, inline=False)
        embed.add_field(name="Hosted by: ", value=inter.user.mention, inline=False)
        embed.add_field(name="Ends in: ", value=f"{time}{modifier}", inline=False)
        embed.add_field(name="Winners: ", value=winners, inline=False)
        msg = await inter.response.send_message(embed=embed)
        f = msg.fetch_message()
        await f.add_reaction("🎉")
        if modifier == "s":
            await asyncio.sleep(time)
        elif modifier == "m":
            await asyncio.sleep(time * 60)
        elif modifier == "h":
            await asyncio.sleep(time * 60 * 60)
        elif modifier == "d":
            await asyncio.sleep(time * 60 * 60 * 24)
        elif modifier == "w":
            await asyncio.sleep(time * 60 * 60 * 24 * 7)
        winner = None
        for reaction in msg.reactions:
            if reaction.emoji == "🎉":
                users = await reaction.users().flatten()
                users.pop(users.index(self.bot.user))
                winner = random.choice(users)
        if winners > 1:
            winners_ = []
            for _ in range(winners):
                for reaction in msg.reactions:
                    if reaction.emoji == "🎉":
                        users = await reaction.users().flatten()
                        users.pop(users.index(self.bot.user))
                        winners_.append(random.choice(users))
        if winner is not None:
            if winners > 1:
                await inter.channel.send(
                    f"Congratulations {', '.join([winner.mention for winner in winners_])}! You won **{prize}**!"
                )
            else:
                await inter.channel.send(
                    f"Congratulations {winner.mention}! You won **{prize}**!"
                )
        else:
            await inter.channel.send(f"Nobody won **{prize}**!")


def setup(bot):
    bot.add_cog(Utils(bot))
