from nextcord import Color, Embed, Message
from nextcord.ext import commands


class OnBotMention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """When the bot is mentioned, send a message

        Args:
          message (Message): The message
        """
        if message.author == self.bot.user:
            return
        bot_mention = False
        for mention in message.mentions:
            if mention == self.bot.user or mention.name == self.bot.user.name:
                bot_mention = True
                break
            if bot_mention:
                await message.reply(
                    embed=Embed(
                        title="Bot Mentioned",
                        description=f"Hello! I'm **__DevBot__**! I use the new **Slash Commands**!",
                        color=getattr(
                            Color, self.bot.config.get("default_embed_color")
                        )(),
                    )
                )


def setup(bot):
    bot.add_cog(OnBotMention(bot))
