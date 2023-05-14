from nextcord import Color, Embed, Interaction
from nextcord.ext import application_checks, commands


class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, inter: Interaction, error):
        """When a command error occurs, log it and send a message to the user

        Args:
          inter (Interaction): The context
          error (Exception): The error
        """
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await inter.send(
                embed=Embed(
                    title="Error",
                    description="Missing Permissions",
                    color=getattr(Color, self.bot.config.get("default_embed_color"))(),
                )
            )
        elif isinstance(error, application_checks.ApplicationBotMissingPermissions):
            await inter.send(
                embed=Embed(
                    title="Error",
                    description="Bot is missing permissions",
                    color=getattr(Color, self.bot.config.get("default_embed_color"))(),
                )
            )
        elif isinstance(error, application_checks.ApplicationNotOwner):
            await inter.send(
                embed=Embed(
                    title="Error",
                    description="You are not the owner of this bot",
                    color=getattr(Color, self.bot.config.get("default_embed_color"))(),
                )
            )
        else:
            await inter.send(
                embed=Embed(
                    title="Error",
                    description="An unknown error occurred, please try again later. If the issue persists, please open a ticket.",
                    color=getattr(Color, self.bot.config.get("default_embed_color"))(),
                )
            )
        return self.bot.logger.log("error", error)


def setup(bot):
    bot.add_cog(OnCommandError(bot))
