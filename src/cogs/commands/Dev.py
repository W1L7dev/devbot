import datetime
import os
import time

import logmaster.errors
from logmaster import Logger
from nextcord import (Activity, ActivityType, Game, Interaction, SlashOption,
                      Status, slash_command)
from nextcord.ext import application_checks, commands

from tasks.clear import cls
from tasks.restart import restart


class Dev(commands.Cog):
    """Dev commands

    Commands:
        uptime: Checks the bot's uptime
        cls: Clears the console
        print: Prints something in the terminal
        restart: Restarts the bot
        shutdown: Shuts down the bot
        cog:
            load: Loads a cog
            unload: Unloads a cog
            reload: Reloads a cog
            create: Creates a cog
        activity: Sets the bot's activity
        status: Sets the bot's status
        file: File commands
        folder: Folder commands
        eval: Evaluates code
        log: Logs a message to the console
        file:
            read: Reads a file
            create: Creates a file
            delete: Deletes a file
            write: Writes to a file
            clear: Clears a file
        folder:
            create: Creates a folder
            delete: Deletes a folder
            list: Lists a folder
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="uptime", description="Shows the uptime of the bot")
    @application_checks.has_guild_permissions(administrator=True)
    async def uptime(self, inter: Interaction):
        """Checks the bot's uptime

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Uptime",
            description=f"Uptime: **{str(datetime.timedelta(seconds=int(round(time.time() - self.bot.uptime))))}**",
        )

    @slash_command(name="cls", description="Clears the console")
    @application_checks.has_guild_permissions(administrator=True)
    async def cls(self, inter: Interaction):
        """Clears the console

        Args:
          inter (Interaction): The interaction
        """
        cls()
        await self.bot.standard_reponse(
            inter, title="Clear", description="Cleared the console"
        )

    @slash_command(name="print", description="Prints something in the terminal")
    @application_checks.has_permissions(administrator=True)
    async def echo(
        self,
        inter: Interaction,
        text: str = SlashOption(name="text", description="The text to print"),
    ):
        """Prints something in the terminal

        Args:
            inter (Interaction): The interaction
            text (str, optional): The text to print. Defaults to SlashOption(name="text", description="The text to print").
        """
        print(text)
        await self.bot.standard_response(
            inter, title="Print", description=f"Printed `{text}` in the terminal"
        )

    @slash_command(name="restart", description="Restarts the bot")
    @application_checks.has_guild_permissions(administrator=True)
    async def restart(self, inter: Interaction):
        """Restarts the bot

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter, title="Restart", description="Restarting the bot..."
        )
        restart()

    @slash_command(name="shutdown", description="Shuts down the bot")
    @application_checks.has_guild_permissions(administrator=True)
    async def shutdown(
        self,
        inter: Interaction,
    ):
        """Shuts down the bot

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Shutdown",
            description="Shutting down the bot...",
        )
        await self.bot.close()

    """    @slash_command(name="cog", description="Cog management")
    @application_checks.has_guild_permissions(administrator=True)
    async def cog(
        self,
        inter: Interaction,
        cog: str = SlashOption(
            name="cog",
            description="The cog to manage",
            choices=[
                "Dev",
                "Math",
                "Fun",
                "Infos",
                "Moderation",
                "Music",
                "Admin",
                "Utils",
                "Ticket",
                "RoleReact",
                "Poll",
                "Levelling",
                "OnBotMention",
                "OnCommandError",
                "OnReady",
                "OnMemberJoin",
                "OnMemberLeaving",
            ],
        ),
        type: str = SlashOption(
            name="type",
            description="The type of cog",
            choices=["events", "commands"],
        ),
        action: str = SlashOption(
            name="action",
            description="The action to perform",
            choices=["load", "unload", "reload"],
        ),
    ):
        if action == "load":
            title = "LoadCog"
            try:
                self.bot.load_extension(f"cogs.{type}.{cog}")
                desc = f"Loaded **{cog}**"
            except Exception as e:
                desc = f"Failed to load **{cog}** due to \n```{e}```"
        elif action == "unload":
            title = "UnloadCog"
            try:
                self.bot.unload_extension(f"cogs.{type}.{cog}")
                desc = f"Unloaded **{cog}**"
            except Exception as e:
                desc = f"Failed to unload **{cog}** due to \n```{e}```"
        elif action == "reload":
            title = "ReloadCog"
            try:
                self.bot.reload_extension(f"cogs.{type}.{cog}")
                desc = f"Reloaded **{cog}**"
            except Exception as e:
                desc = f"Failed to reload **{cog}** due to \n```{e}```"
        await self.bot.standard_response(inter, title=title, description=desc)"""

    @slash_command(name="cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def cog(self, inter: Interaction):
        pass

    @cog.subcommand(name="load", description="Loads a cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def load(
        self,
        inter: Interaction,
        cog: str = SlashOption(
            name="cog",
            description="The cog to load",
            choices=list(
                os.listdir("src/cogs/commands") + os.listdir("src/cogs/events")
            ),
        ),
    ):
        """Loads a cog

        Args:
          inter (Interaction): The interaction
          cog (str): The cog to load. Defaults to SlashOption(name="cog", description="The cog to load", choices=list(os.listdir("src/cogs/commands") + os.listdir("src/cogs/events"))).
        """
        try:
            self.bot.load_extension(f"cogs.commands.{cog}")
            desc = f"Loaded **{cog}**"
        except Exception as e:
            desc = f"Failed to load **{cog}** due to \n```{e}```"
        await self.bot.standard_response(inter, title="Cog", description=desc)

    @cog.subcommand(name="unload", description="Unloads a cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def unload(
        self,
        inter: Interaction,
        cog: str = SlashOption(
            name="cog",
            description="The cog to unload",
            choices=list(
                os.listdir("src/cogs/commands") + os.listdir("src/cogs/events")
            ),
        ),
    ):
        """Unloads a cog

        Args:
          inter (Interaction): The interaction
          cog (str): The cog to unload. Defaults to SlashOption(name="cog", description="The cog to unload", choices=list(os.listdir("src/cogs/commands") + os.listdir("src/cogs/events"))).
        """
        try:
            self.bot.unload_extension(f"cogs.commands.{cog}")
            desc = f"Unloaded **{cog}**"
        except Exception as e:
            desc = f"Failed to unload **{cog}** due to \n```{e}```"
        await self.bot.standard_response(inter, title="Cog", description=desc)

    @cog.subcommand(name="reload", description="Reloads a cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def reload(
        self,
        inter: Interaction,
        cog: str = SlashOption(
            name="cog",
            description="The cog to reload",
            choices=list(
                os.listdir("src/cogs/commands") + os.listdir("src/cogs/events")
            ),
        ),
    ):
        """Reloads a cog

        Args:
          inter (Interaction): The interaction
          cog (str): The cog to reload. Defaults to SlashOption(name="cog", description="The cog to reload", choices=list(os.listdir("src/cogs/commands") + os.listdir("src/cogs/events"))).
        """
        try:
            self.bot.reload_extension(f"cogs.commands.{cog}")
            desc = f"Reloaded **{cog}**"
        except Exception as e:
            desc = f"Failed to reload **{cog}** due to \n```{e}```"
        await self.bot.standard_response(inter, title="Cog", description=desc)

    @cog.subcommand(name="create", description="Creates a cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def create(
        self,
        inter: Interaction,
        name: str = SlashOption(
            name="name", description="The name of the cog to create"
        ),
        type: str = SlashOption(
            name="type",
            description="The type of cog to create",
            choices=["commands", "events"],
        ),
    ):
        """Creates a cog

        Args:
          inter (Interaction): The interaction
          name (str): The name of the cog to create. Defaults to SlashOption(name="name", description="The name of the cog to create").
          type (str): The type of cog to create. Defaults to SlashOption(name="type", description="The type of cog to create", choices=["commands", "events"]).
        """
        if type == "commands":
            path = f"src/cogs/commands/{name}.py"
            cog = f"""
                from nextcord.ext import commands

                class {name}(commands.Cog):
                    \"\"\"{name} commands\"\"\"

                    def __init__(self, bot):
                        self.bot = bot

                def setup(bot):
                    bot.add_cog({name}(bot))

                """
        elif type == "events":
            path = f"src/cogs/events/{name}.py"
            cog = f"""
                from nextcord.ext import commands

                class {name}(commands.Cog):
                    \"\"\"{name} events\"\"\"

                    def __init__(self, bot):
                        self.bot = bot

                def setup(bot):
                    bot.add_cog({name}(bot))

                """
        with open(path, "w") as f:
            f.write(cog)
        await self.bot.standard_response(
            inter, title="Cog", description=f"Created cog **{name}**"
        )

    @slash_command(name="activity", description="Sets the bot's activity")
    @application_checks.has_guild_permissions(administrator=True)
    async def activity(
        self,
        inter: Interaction,
        title: str = SlashOption(name="title", description="The title of the activity"),
        activity: str = SlashOption(
            name="activity",
            description="The activity type",
            choices=["playing", "watching", "listening"],
        ),
    ):
        """Sets the bot's activity

        Args:
          inter (Interaction): The interaction
          title (str): The title of the activity. Defaults to SlashOption(name="title", description="The title of the activity").
          activity (str): The activity type. Defaults to SlashOption(name="activity", description="The activity type", choices=["playing", "watching", "listening"]).
        """
        if activity == "playing":
            await self.bot.change_presence(activity=Game(name=title))
        elif activity == "watching":
            await self.bot.change_presence(
                activity=Activity(type=ActivityType.watching, name=title)
            )
        elif activity == "listening":
            await self.bot.change_presence(
                activity=Activity(type=ActivityType.listening, name=title)
            )
        await self.bot.standard_response(
            inter,
            title="Activity",
            description=f"Set the activity to **{activity} {title}**",
        )

    @slash_command(name="status", description="Sets the bot's status")
    @application_checks.has_guild_permissions(administrator=True)
    async def status(
        self,
        inter: Interaction,
        status: str = SlashOption(
            name="status",
            description="The status to set the bot to",
            choices=["online", "idle", "dnd", "offline"],
        ),
    ):
        """Sets the bot's status

        Args:
          inter (Interaction): The interaction
          status (str): The bot's status. Defaults to SlashOption( name="status", description="The status to set the bot to", choices=["online", "idle", "dnd", "offline"], ).
        """
        if status == "online":
            await self.bot.change_presence(status=Status.online)
        elif status == "idle":
            await self.bot.change_presence(status=Status.idle)
        elif status == "dnd":
            await self.bot.change_presence(status=Status.dnd)
        elif status == "offline":
            await self.bot.change_presence(status=Status.offline)
        await self.bot.standard_response(
            inter, title="Status", description=f"Set the status to **{status}**"
        )

    @slash_command(name="file", description="File commands")
    @application_checks.has_guild_permissions(administrator=True)
    async def file(self, inter: Interaction):
        pass

    @file.subcommand(name="read", description="Reads a file")
    @application_checks.has_guild_permissions(administrator=True)
    async def read(
        self,
        inter: Interaction,
        path: str = SlashOption(
            name="path", description="The path of the file to read"
        ),
    ):
        """Reads a file

        Args:
          inter (Interaction): The interaction
          path (str): The file's path. Defaults to SlashOption(name="path", description="The path of the file to read").
        """
        try:
            with open(path, "r") as f:
                content = f.read()
            desc = f"**{path}**\n{content}"
        except Exception as e:
            desc = f"Failed to read **{path}** due to \n```{e}```"
        await self.bot.standard_response(inter, title="ReadFile", description=desc)

    @file.subcommand(name="create", description="Creates a file")
    @application_checks.has_guild_permissions(administrator=True)
    async def create(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
        content: str = SlashOption(
            name="content", description="The content of the file", required=False
        ),
    ):
        """Creates a file

        Args:
          inter (Interaction): The interaction
          path (str): The file's path. Defaults to SlashOption(name="path", description="The name of the file").
          content (str, optional): The files content. Defaults to SlashOption(name="content", description="The content of the file", required=False).
        """
        with open(path, "w") as f:
            f.write(content or "")
        await self.bot.standard_response(
            inter, title="CreateFile", description=f"Created file **{path}**"
        )

    @file.subcommand(name="delete", description="Deletes a file")
    @application_checks.has_guild_permissions(administrator=True)
    async def delete(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
    ):
        """Deletes a file

        Args:
          inter (Interaction): The interaction
          path (str): The file's path. Defaults to SlashOption(name="path", description="The name of the file").
        """
        try:
            os.remove(path)
            desc = f"Deleted file **{path}**"
        except FileNotFoundError:
            desc = f"File **{path}** not found"
        await self.bot.standard_response(inter, title="DeleteFile", description=desc)

    @file.subcommand(name="write", description="Writes to a file")
    @application_checks.has_guild_permissions(administrator=True)
    async def write(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
        content: str = SlashOption(
            name="content", description="The content to write to the file"
        ),
    ):
        """Writes to a file

        Args:
          inter (Interaction): The interaction
          path (str): The file's path. Defaults to SlashOption(name="path", description="The name of the file").
          content (str): The content to write to the file. Defaults to SlashOption(name="content", description="The content to write to the file").
        """
        try:
            with open(path, "a") as f:
                f.write(content)

            desc = f"Wrote to file **{path}**"
        except FileNotFoundError:
            desc = f"File **{path}** not found"
        await self.bot.standard_response(inter, title="WriteFile", description=desc)

    @file.subcommand(name="clear", description="Clears a file")
    @application_checks.has_guild_permissions(administrator=True)
    async def clear(
        self,
        inter: Interaction,
        path: str = SlashOption(
            name="path", description="The path of the file to clear"
        ),
    ):
        """Clears a file

        Args:
          inter (Interaction): The interaction
          path (str): The file's path. Defaults to SlashOption(name="path", description="The path of the file to clear").
        """
        try:
            with open(path, "w") as f:
                f.write("")
            desc = f"Cleared file **{path}**"
        except FileNotFoundError:
            desc = f"File **{path}** not found"
        await self.bot.standard_response(inter, title="ClearFile", description=desc)

    @slash_command(name="folder", description="Folder commands")
    @application_checks.has_guild_permissions(administrator=True)
    async def folder(self, inter: Interaction):
        pass

    @folder.subcommand(name="create", description="Creates a folder")
    @application_checks.has_guild_permissions(administrator=True)
    async def createfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the folder"),
    ):
        """Creates a folder

        Args:
          inter (Interaction): The interaction
          path (str): The folder's path. Defaults to SlashOption(name="path", description="The name of the folder").
        """
        try:
            os.mkdir(path)
            desc = f"Created folder **{path}**"
        except IsADirectoryError or FileExistsError:
            desc = f"Folder **{path}** already exists"
        await self.bot.standard_response(inter, title="CreateFolder", description=desc)

    @folder.subcommand(name="delete", description="Deletes a folder")
    @application_checks.has_guild_permissions(administrator=True)
    async def delfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The path of the folder"),
    ):
        """Deletes a folder

        Args:
          inter (Interaction): The interaction
          path (str): The folder's path. Defaults to SlashOption(name="path", description="The path of the folder").
        """
        try:
            os.rmdir(path)
            desc = f"Deleted folder **{path}**"
        except FileNotFoundError:
            desc = f"Folder **{path}** not found"
        await self.bot.standard_response(inter, title="DeleteFolder", description=desc)

    @folder.subcommand(name="list", description="Lists a folder")
    @application_checks.has_guild_permissions(administrator=True)
    async def listfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The path of the folder"),
    ):
        """Lists a folder

        Args:
          inter (Interaction): The interaction
          path (str): The folder's path. Defaults to SlashOption(name="path", description="The path of the folder").
        """
        try:
            files = os.listdir(path)
            desc = f"**{path}**\n{files}"
        except NotADirectoryError or FileNotFoundError:
            desc = f"Folder **{path}** not found"
        await self.bot.standard_response(inter, title="ListFolder", description=desc)

    @slash_command(name="eval", description="Evaluates code")
    @application_checks.has_guild_permissions(administrator=True)
    async def eval(
        self,
        inter: Interaction,
        code: str = SlashOption(
            name="code", description="The code to evaluate (python)"
        ),
    ):
        """Evaluates code

        Args:
          inter (Interaction): The interaction
          code (str): The code to evaluate. Defaults to SlashOption(name="code", description="The code to evaluate (python)").
        """
        try:
            exec(code)
            desc = f"Code successfully executed"
        except Exception as e:
            desc = f"Error: {e}"
        await self.bot.standard_response(inter, title="Eval", description=desc)

    @slash_command(name="log", description="Logs a message to the console")
    @application_checks.has_guild_permissions(administrator=True)
    async def log(
        self,
        inter: Interaction,
        type: str = SlashOption(
            name="type",
            description="The type of log",
            choices=Logger().levels,
        ),
        message: str = SlashOption(name="message", description="The message to log"),
    ):
        """Logs a message to the console

        Args:
          inter (Interaction): The interaction
          type (str): The type of log. Defaults to SlashOption( name="type", description="The type of log", choices=[ "debug", "info", "warning", "error", "critical" ] ).
          message (str): The message to log. Defaults to SlashOption(name="message", description="The message to log").
        """

        try:
            self.bot.logger.log(type, message)
        except Exception as e:
            if e == logmaster.errors.InvalidLevel:
                return await self.bot.standard_response(
                    inter,
                    title="InvalidLevel",
                    description=f"Invalid level **{type}**. {e}",
                )
            else:
                return await self.bot.standard_response(
                    inter, title="Error", description=f"Error: {e}"
                )

        await self.bot.standard_response(
            inter, title="Log", description=f"Logged message **{message}**"
        )


def setup(bot):
    bot.add_cog(Dev(bot))


bot = ""
print(Dev(bot).cogs)
