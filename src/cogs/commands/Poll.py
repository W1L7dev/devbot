from nextcord import (Color, Embed, Interaction, Message, SlashOption,
                      slash_command)
from nextcord.ext import commands


class Poll(commands.Cog):
    """Poll commands

    Commands:
        poll: Create a poll with custom options
        pollresult: Get the results of a poll
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="poll", description="Create a poll with custom options")
    async def poll(
        self,
        inter: Interaction,
        question: str = SlashOption(name="question", description="The question to ask"),
        options: str = SlashOption(
            name="options", description="The options to choose from"
        ),
    ):
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

    @slash_command(name="pollresult", description="Get the results of a poll")
    async def pollresult(
        self,
        inter: Interaction,
        message_id: str = SlashOption(
            name="message_id", description="The ID of the message to get the results of"
        ),
    ):
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
    bot.add_cog(Poll(bot))
