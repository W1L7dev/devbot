import datetime
import json
import os
import time

import aiohttp
import logmaster.errors
from logmaster import Logger
from nextcord import (Activity, ActivityType, File, Game, Interaction,
                      SlashOption, Status, slash_command)
from nextcord.ext import application_checks, commands

from tasks.Clear import cls
from tasks.Restart import restart
from tasks.visualize_json import visualize_json


class Dev(commands.Cog):
    """Dev commands

    Commands:
        uptime:-
        cls: Clears the terminal output.
        print: Prints a message to the terminal.
        restart: Restarts the bot.
        shutdown: Shuts down the bot.
        activity: Sets the bot's activity.
        status: Sets the bot's status.
        eval: Evaluates Python code.
        log: Logs a message to the terminal.
        request: Sends an http request to a website.
        jsondiagram: Generates a diagram from a json file/string.
        cog:
            load: Loads a cog.
            unload: Unloads a cog.
            reload: Reloads a cog.
            create: Creates a cog.
        file:
            read: Reads a file.
            create: Creates a file.
            delete: Deletes a file.
            write: Writes to a file.
            clear: Clears a file.
        folder:
            create: Creates a folder.
            delete: Deletes a folder.
            list: Lists the contents of a folder.
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="uptime", description="Displays the bot's uptime.")
    @application_checks.has_guild_permissions(administrator=True)
    async def uptime(self, inter: Interaction):
        """Displays the bot's uptime.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Uptime",
            description=f"Uptime: **{str(datetime.timedelta(seconds=int(round(time.time() - self.bot.uptime))))}**",
        )

    @slash_command(name="cls", description="Clears the terminal output.")
    @application_checks.has_guild_permissions(administrator=True)
    async def cls(self, inter: Interaction):
        """Clears the terminal output.

        Args:
          inter (Interaction): The interaction
        """
        cls()
        await self.bot.standard_reponse(
            inter, title="Clear", description="Cleared the console"
        )

    @slash_command(name="print", description="Prints a message to the terminal.")
    @application_checks.has_permissions(administrator=True)
    async def echo(
        self,
        inter: Interaction,
        text: str = SlashOption(name="text", description="The text to print"),
    ):
        """Prints a message to the terminal.

        Args:
            inter (Interaction): The interaction
            text (str, optional): The text to print. Defaults to SlashOption(name="text", description="The text to print").
        """
        print(text)
        await self.bot.standard_response(
            inter, title="Print", description=f"Printed `{text}` in the terminal"
        )

    @slash_command(name="restart", description="Restarts the bot.")
    @application_checks.has_guild_permissions(administrator=True)
    async def restart(self, inter: Interaction):
        """Restarts the bot.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter, title="Restart", description="Restarting the bot..."
        )
        restart()

    @slash_command(name="shutdown", description="Shuts down the bot.")
    @application_checks.has_guild_permissions(administrator=True)
    async def shutdown(
        self,
        inter: Interaction,
    ):
        """Shuts down the bot.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Shutdown",
            description="Shutting down the bot...",
        )
        await self.bot.close()

    @slash_command(name="cog")
    @application_checks.has_guild_permissions(administrator=True)
    async def cog(self, inter: Interaction):
        pass

    @cog.subcommand(name="load", description="Loads a cog.")
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
        """Loads a cog.

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

    @cog.subcommand(name="unload", description="Unloads a cog.")
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
        """Unloads a cog.

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

    @cog.subcommand(name="reload", description="Reloads a cog.")
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
        """Reloads a cog.

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

    @cog.subcommand(name="create", description="Creates a cog.")
    @application_checks.has_guild_permissions(administrator=True)
    async def cogcreate(
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
        """Creates a cog.

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
        else:
            return
        with open(path, "w") as f:
            f.write(cog)
        await self.bot.standard_response(
            inter, title="Cog", description=f"Created cog **{name}**"
        )

    @slash_command(name="activity", description="Sets the bot's activity.")
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
        """Sets the bot's activity.

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

    @slash_command(name="status", description="Sets the bot's status.")
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
        """Sets the bot's status.

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

    @file.subcommand(name="read", description="Reads a file.")
    @application_checks.has_guild_permissions(administrator=True)
    async def read(
        self,
        inter: Interaction,
        path: str = SlashOption(
            name="path", description="The path of the file to read"
        ),
    ):
        """Reads a file.

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

    @file.subcommand(name="create", description="Creates a file.")
    @application_checks.has_guild_permissions(administrator=True)
    async def create(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
        content: str = SlashOption(
            name="content", description="The content of the file", required=False
        ),
    ):
        """Creates a file.

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

    @file.subcommand(name="delete", description="Deletes a file.")
    @application_checks.has_guild_permissions(administrator=True)
    async def delete(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
    ):
        """Deletes a file.

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

    @file.subcommand(name="write", description="Writes to a file.")
    @application_checks.has_guild_permissions(administrator=True)
    async def write(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the file"),
        content: str = SlashOption(
            name="content", description="The content to write to the file"
        ),
    ):
        """Writes to a file.

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

    @file.subcommand(name="clear", description="Clears a file.")
    @application_checks.has_guild_permissions(administrator=True)
    async def clear(
        self,
        inter: Interaction,
        path: str = SlashOption(
            name="path", description="The path of the file to clear"
        ),
    ):
        """Clears a file.

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

    @folder.subcommand(name="create", description="Creates a folder.")
    @application_checks.has_guild_permissions(administrator=True)
    async def createfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The name of the folder"),
    ):
        """Creates a folder.

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

    @folder.subcommand(name="delete", description="Deletes a folder.")
    @application_checks.has_guild_permissions(administrator=True)
    async def delfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The path of the folder"),
    ):
        """Deletes a folder.

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

    @folder.subcommand(name="list", description="Lists the contents of a folder.")
    @application_checks.has_guild_permissions(administrator=True)
    async def listfolder(
        self,
        inter: Interaction,
        path: str = SlashOption(name="path", description="The path of the folder"),
    ):
        """Lists the contents of a folder.

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

    @slash_command(name="eval", description="Evaluates Python code.")
    @application_checks.has_guild_permissions(administrator=True)
    async def eval(
        self,
        inter: Interaction,
        code: str = SlashOption(
            name="code", description="The code to evaluate (python)"
        ),
    ):
        """Evaluates Python code.

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

    @slash_command(name="log", description="Logs a message to the terminal.")
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
        """Logs a message to the terminal.

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

    @slash_command(name="request", description="Sends an http request to a website.")
    @application_checks.has_guild_permissions(administrator=True)
    async def request(
        self,
        inter: Interaction,
        url: str = SlashOption(
            name="url", description="The url to send the request to"
        ),
        method: str = SlashOption(
            name="method",
            description="The method to use",
            choices=["get", "post"],
        ),
        headers: str = SlashOption(
            name="headers",
            description="The headers to send",
            required=False,
        ),
        data: str = SlashOption(
            name="data",
            description="The data to send",
            required=False,
        ),
    ):
        """Sends an http request to a website.

        Args:
          inter (Interaction): The interaction
          url (str): The url to send the request to. Defaults to SlashOption(name="url", description="The url to send the request to").
          method (str): The method to use. Defaults to SlashOption(name="method", description="The method to use", choices=["get", "post"]).
          headers (str, optional): The headers to send. Defaults to SlashOption(name="headers", description="The headers to send", required=False).
          data (str, optional): The data to send. Defaults to SlashOption(name="data", description="The data to send", required=False).
        """
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
            ) as response:
                desc = f"**{response.status}**"
        await self.bot.standard_response(inter, title="Request", description=desc)
        with open("temp_req.txt", "w") as f:
            f.write(str(response.text))
        await inter.send(file=File("temp_req.txt"))
        os.remove("temp_req.txt")

    @slash_command(name="jsondiagram", description="Generates a diagram from a json file/string.")
    @application_checks.has_guild_permissions(administrator=True)
    async def jsondiagram(
        self,
        inter: Interaction,
        data: str = SlashOption(
            name="data", description="The data to create a diagram of"
        ),
    ):
        """Generates a diagram from a json file/string.

        Args:
          inter (Interaction): The interaction
          data (str): The data to create a diagram of. Defaults to SlashOption(name="data", description="The data to create a diagram of").
        """
        try:
            parsed = json.loads(data)
        except Exception as e:
            return await self.bot.standard_response(
                inter, title="Error", description=f"Error: {e}"
            )
        diagram = visualize_json(data)
        await self.bot.standard_response(
            inter, title="JSON Diagram", description=f"```{diagram}```"
        )


def setup(bot):
    bot.add_cog(Dev(bot))
