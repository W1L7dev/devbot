import asyncio
import base64
import random
import time
from io import BytesIO

import aiohttp
from nextcord import (Color, Embed, File, Interaction, Member, Message,
                      RawReactionActionEvent, SlashOption, slash_command,
                      utils)
from nextcord.ext import application_checks, commands
from nextcord.interactions import Interaction

from tasks.math import solve_expr


class Utils(commands.Cog):
    """Utility commands

    Commands:
        ticket: Creates a ticket message.
        ping: Displays the bot's ping.
        say: Makes the bot say something.
        embed: Makes the bot send an embed.
        nick: Changes your nickname.
        resetnick: Resets your nickname.
        avatar: Displays a user's avatar.
        giveaway: Creates a giveaway.
        math: Evaluates a mathematical expression.
        img: Generates an image with AI.
        poll: Creates a poll.
        pollresult: Displays the results of a poll.
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ticket", description="Creates a ticket message.")
    @application_checks.has_guild_permissions(manage_channels=True)
    async def ticket(self, inter: Interaction):
        """Creates a ticket message.

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

    @slash_command(name="ping", description="Displays the bot's ping.")
    async def ping(self, inter: Interaction):
        """Displays the bot's ping.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Pong 🏓!",
            description=f"Latency: {round(self.bot.latency * 1000)}ms",
        )

    @slash_command(name="img", description="Generates an image with AI.")
    async def img(
        self,
        inter: Interaction,
        prompt: str = SlashOption(
            name="prompt",
            description="The prompt to generate the image from",
        ),
    ):
        """Generates an image with AI.

        Args:
          inter (Interaction): The interaction
          prompt (str): The prompt to generate the image from. Defaults to SlashOption(name="prompt", description="The prompt to generate the image from").
        """
        ETA = int(time.time() + 60)
        await self.bot.standard_response(
            inter,
            title="Generating image",
            description=f"ETA: <t:{ETA}:R>",
        )
        async with aiohttp.request(
            "POST", "https://backend.craiyon.com/generate", json={"prompt": prompt}
        ) as resp:
            data = await resp.json()
        imgs = data["images"]
        img = BytesIO(base64.decodebytes(imgs[0].encode("utf-8")))
        await inter.send(
            embed=Embed(
                title="Generated image",
                description=f"Prompt: {prompt}",
                color=Color.blurple(),
            ),
            file=File(img, filename="generatedImage.png"),
        )

    @slash_command(name="say", description="Makes the bot say something.")
    async def say(
        self,
        inter: Interaction,
        message: str = SlashOption(
            name="message",
            description="The message to send",
        ),
    ):
        """Makes the bot say something.

        Args:
          inter (Interaction): The interaction
          message (str): The message to send. Defaults to SlashOption(name="message", description="The message to send").
        """
        await inter.response.send_message(message)

    @slash_command(name="embed", description="Makes the bot send an embed.")
    async def embed(
        self,
        inter: Interaction,
        title: str = SlashOption(name="title", description="The title of the embed"),
        message: str = SlashOption(
            name="message", description="The message of the embed"
        ),
    ):
        """Makes the bot send an embed.

        Args:
          inter (Interaction): The interaction
          title (str): The title of the embed. Defaults to SlashOption(name="title", description="The title of the embed").
          message (str): The message of the embed. Defaults to SlashOption(name="message", description="The message of the embed").
          color (str): The color of the embed. Defaults to SlashOption(name="color", description="The color of the embed", choices=["red", "orange", "yellow", "green", "blue", "purple", "pink", "white", "black", "brown", "teal", "blurple", "greyple"]).
        """
        await self.bot.standard_response(inter, title=title, description=message)

    @slash_command(name="nick", description="Changes your nickname.")
    async def nick(
        self,
        inter: Interaction,
        nickname: str = SlashOption(
            name="nickname", description="The nickname to change to"
        ),
    ):
        """Changes your nickname.

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

    @slash_command(name="resetnick", description="Resets your nickname.")
    async def resetnick(self, inter: Interaction):
        """Resets your nickname.

        Args:
          inter (Interaction): The interaction
        """
        await inter.user.edit(nick=None)
        await self.bot.standard_response(
            inter, title="Nickname reset", description="Reset nickname"
        )

    @slash_command(name="avatar", description="Displays a user's avatar.")
    async def avatar(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member to get the avatar of", required=False
        ),
    ):
        """Displays a user's avatar.

        Args:
          inter (Interaction): The interaction
          member (Member, optional): The member to get the avatar of. Defaults to SlashOption(name="member", description="The member to get the avatar of", required=False).
        """
        if not member:
            member = inter.user
        embed = Embed(title=f"**{member.name}**'s avatar", color=Color.blurple())
        embed.set_image(url=member.avatar.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="giveaway", description="Creates a giveawa")
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
        """Creates a giveaway.

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

    @slash_command(name="math", description="Evaluates a mathematical expression.")
    async def math(
        self,
        inter: Interaction,
        expression: str = SlashOption(
            name="expression", description="The expression to evaluate"
        ),
    ):
        await self.bot.standard_response(
            inter,
            title="Math",
            description=f"**{expression}** = **{solve_expr(expression)}**",
        )

    @slash_command(name="poll", description="Creates a poll.")
    async def poll(
        self,
        inter: Interaction,
        question: str = SlashOption(name="question", description="The question to ask"),
        options: str = SlashOption(
            name="options", description="The options to choose from"
        ),
    ):
        """Creates a poll.

        Args:
          inter (Interaction): The interaction
          question (str): The question to ask. Defaults to SlashOption(name="question", description="The question to ask").
          options (str): The options to choose from. Defaults to SlashOption(name="options", description="The options to choose from").
        """
        options = options.split(",")
        if len(options) > 10:
            return await self.bot.standard_response(
                embed=Embed(
                    title="You can only have up to 10 options.",
                    color=self.bot.config.get("default_embed_color"),
                ),
                ephemeral=True,
            )
        if len(options) < 2:
            return await self.bot.standard_response(
                inter, title="Poll", description="You need to have at least 2 options."
            )
        embed = Embed(
            title="Poll",
            description=question,
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for x, option in enumerate(options):
            embed.add_field(name=reactions[x], value=option, inline=False)
        await self.bot.standard_response(embed=embed)
        for reaction in reactions[: len(options)]:
            message: Message
            async for message in inter.channel.history():
                if not message.embeds:
                    continue
                if (
                    message.embeds[0].title == embed.title
                    and message.embeds[0].color == embed.color
                ):
                    vote = message
                    break
                else:
                    return
            await vote.add_reaction(reaction)

    @slash_command(name="pollresult", description="Displays the results of a poll.")
    async def pollresult(
        self,
        inter: Interaction,
        message_id: str = SlashOption(
            name="message_id", description="The ID of the message to get the results of"
        ),
    ):
        """Displays the results of a poll.

        Args:
          inter (Interaction): The interaction
          message_id (str): The ID of the message to get the results of. Defaults to SlashOption(name="message_id", description="The ID of the message to get the results of").
        """
        message = await inter.channel.fetch_message(int(message_id))
        reactions = message.reactions
        total_votes = sum([reaction.count - 1 for reaction in reactions])
        embed = Embed(
            title="Poll Results",
            description=f"**{message.embeds[0].description}**",
            color=Color.blurple(),
        )
        embed.set_footer(text=message.embeds[0].footer.text)
        for reaction in reactions:
            count = reaction.count - 1
            percentage = round(count / total_votes * 100) if total_votes > 0 else 0
            embed.add_field(
                name=f"{reaction.emoji}", value=f"{count}, {percentage}%", inline=True
            )
        await self.bot.standard_response(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))
