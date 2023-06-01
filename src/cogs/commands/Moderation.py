import asyncio
import datetime
import json
import os

from nextcord import (Color, Embed, ForumChannel, Interaction, Member,
                      NotFound, Object, SlashOption, StageChannel, TextChannel,
                      VoiceChannel, slash_command, utils)
from nextcord.ext import application_checks, commands


class Moderation(commands.Cog):
    """Moderation commands

    Commands:
        raidmode: Toggles raidmode.
        lock: Locks a channel.
        unlock: Unlocks a channel.
        slowmode:	Sets the slowmode of a channel.
        clear: Clears messages.
        ban: Bans a user.
        unban: Unbans a user.
        kick: Kicks a user.
        timeout: Timeouts a user.
        warn: Warns a user.
        warnings: Displays a user's warnings.
        clearwarns: Clears a user's warnings.
        removewarn: Removes a warning from a user.
    """

    def __init__(self, bot):
        self.bot = bot
        self.dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

    @slash_command(name="raidmode", description="Toggles raidmode.")
    @application_checks.has_guild_permissions(manage_guild=True)
    async def raidmode(
        self,
        inter: Interaction,
        toggle: bool = SlashOption(
            name="toggle", description="Whether to turn raid mode on or off"
        ),
    ):
        """Toggles raidmode.

        Args:
          inter (Interaction): The interaction.
          toggle (bool): Sets raidmode to true or false. Defaults to SlashOption(name="toggle", description="Whether to turn raid mode on or off").
        """
        for channel in inter.guild.channels:
            if isinstance(channel, TextChannel):
                await channel.set_permissions(
                    inter.guild.default_role, send_messages=not toggle
                )
            elif isinstance(channel, VoiceChannel):
                await channel.set_permissions(
                    inter.guild.default_role, connect=not toggle
                )
            elif isinstance(channel, StageChannel):
                await channel.set_permissions(
                    inter.guild.default_role, connect=not toggle
                )
            elif isinstance(channel, ForumChannel):
                await channel.set_permissions(
                    inter.guild.default_role, send_messages=not toggle
                )
        await self.bot.standard_response(
            inter,
            title="Raid Mode",
            description=f"Raid mode is now **{'on' if toggle else 'off'}**",
        )
        await self.bot.log(
            title="Raid Mode",
            description=f"Raid mode is now **{'on' if toggle else 'off'}**",
        )

    @slash_command(name="lock", description="Locks a channel.")
    @application_checks.has_guild_permissions(manage_channels=True)
    async def lock(
        self,
        inter: Interaction,
        channel: TextChannel = SlashOption(
            name="channel", description="The channel you want to lock"
        ),
    ):
        """Locks a channel

        Args:
          inter (Interaction): The interaction
          channel (TextChannel): The channel to lock. Defaults to SlashOption(name="channel", description="The channel you want to lock").
        """
        await channel.set_permissions(inter.guild.default_role, send_messages=False)
        await self.bot.standard_response(
            inter, title="Channel Locked", description=f"Locked **{channel.mention}**"
        )
        await self.bot.log(
            title="Channel Locked", description=f"Locked **{channel.mention}**"
        )

    @slash_command(name="unlock", description="Unlocks a channel.")
    @application_checks.has_guild_permissions(manage_channels=True)
    async def unlock(
        self,
        inter: Interaction,
        channel: TextChannel = SlashOption(
            name="channel", description="The channel you want to unlock"
        ),
    ):
        """Unlocks a channel

        Args:
          inter (Interaction): The interaction
          channel (TextChannel): The channel to unlock. Defaults to SlashOption(name="channel", description="The channel you want to unlock").
        """
        await channel.set_permissions(inter.guild.default_role, send_messages=True)
        await self.bot.standard_response(
            inter,
            title="Channel Unlocked",
            description=f"Unlocked **{channel.mention}**",
        )
        await self.bot.log(
            title="Channel Unlocked", description=f"Unlocked **{channel.mention}**"
        )

    @slash_command(name="slowmode", description="Sets the slowmode of a channel.")
    @application_checks.has_guild_permissions(manage_channels=True)
    async def slowmode(
        self,
        inter: Interaction,
        seconds: int = SlashOption(
            name="seconds",
            description="The amount of seconds you want to set the slowmode to",
        ),
        channel: TextChannel = SlashOption(
            name="channel", description="The channel you want to set the slowmode of"
        ),
    ):
        """Sets the slowmode of a channel.

        Args:
          inter (Interaction): The interaction
          seconds (int): The amount of seconds you want to set the slowmode to. Defaults to SlashOption(name="seconds", description="The amount of seconds you want to set the slowmode to").
          channel (TextChannel): The channel you want to set the slowmode of. Defaults to SlashOption(name="channel", description="The channel you want to set the slowmode of").
        """
        await channel.edit(slowmode_delay=seconds)
        await self.bot.standard_response(
            inter,
            title="Slowmode Set",
            description=f"Set the slowmode of **{channel.mention}** to **{seconds}** seconds",
        )
        await self.bot.log(
            title="Slowmode Set",
            description=f"Set the slowmode of **{channel.mention}** to **{seconds}** seconds",
        )

    @slash_command(name="clear", description="Clears messages.")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def clear(
        self,
        inter: Interaction,
        amount: int = SlashOption(
            name="amount", description="The amount of messages you want to clear"
        ),
        channel: TextChannel = SlashOption(
            name="channel", description="The channel you want to clear the messages of"
        ),
    ):
        """Clears messages.

        Args:
          inter (Interaction): The interaction
          amount (int): The amount of messages you want to clear. Defaults to SlashOption(name="amount", description="The amount of messages you want to clear").
          channel (TextChannel): The channel you want to clear the messages of. Defaults to SlashOption(name="channel", description="The channel you want to clear the messages of").
        """
        await channel.purge(limit=amount)
        await self.bot.log(
            title="Messages Cleared",
            description=f"Cleared **{amount}** messages in **{channel.mention}**",
        )
        message = await self.bot.standard_response(
            inter,
            title="Messages Cleared",
            description=f"Cleared **{amount}** messages in **{channel.mention}**",
        )
        await asyncio.sleep(5)
        await message.delete()

    @slash_command(name="ban", description="Bans a user.")
    @application_checks.has_guild_permissions(ban_members=True)
    async def ban(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to ban"
        ),
        reason: str = SlashOption(
            name="reason", description="The reason you want to ban the member for"
        ),
    ):
        """Bans a user.

        Args:
          inter (Interaction): The interaction
          member (Member): The member you want to ban. Defaults to SlashOption(name="member", description="The member you want to ban").
          reason (str): The reason you want to ban the member for. Defaults to SlashOption(name="reason", description="The reason you want to ban the member for").
        """
        await inter.guild.ban(member, reason=reason)
        await self.bot.standard_response(
            inter,
            title="User Banned",
            description=f"Banned user **{member}** for **{reason}**",
        )
        await self.bot.log(
            title="User Banned",
            description=f"Banned user **{member}** for **{reason}**",
        )

    @slash_command(name="unban", description="Unbans a user.")
    @application_checks.has_guild_permissions(ban_members=True)
    async def unban(
        self,
        inter: Interaction,
        user_id: str = SlashOption(
            name="user", description="The user you want to unban"
        ),
    ):
        """Unbans a user.

        Args:
          inter (Interaction): The interaction
          user_id (str): The id of the user you want to unban. Defaults to SlashOption(name="user", description="The user you want to unban").
        """
        try:
            await inter.guild.unban(Object(id=user_id))
            await self.bot.standard_response(
                inter,
                title="User Unbanned",
                description=f"Unbanned user with id **{user_id}**",
            )
            await self.bot.log(
                title="User Unbanned",
                description=f"Unbanned user with id **{user_id}**",
            )
        except NotFound:
            await self.bot.standard_response(
                inter,
                title="User Not Found",
                description=f"Could not find user with id **{user_id}**",
            )

    @slash_command(name="kick", description="Kicks a user.")
    @application_checks.has_guild_permissions(kick_members=True)
    async def kick(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to kick"
        ),
        reason: str = SlashOption(
            name="reason", description="The reason you want to kick the member for"
        ),
    ):
        """Kicks a user.

        Args:
          inter (Interaction): The interaction
          member (Member): The member you want to kick. Defaults to SlashOption(name="member", description="The member you want to kick").
          reason (str): The reason you want to kick the member for. Defaults to SlashOption(name="reason", description="The reason you want to kick the member for").
        """
        await inter.guild.kick(member, reason=reason)
        await self.bot.standard_response(
            inter,
            title="User Kicked",
            description=f"Kicked user **{member}** for **{reason}**",
        )
        await self.bot.log(
            title="User Kicked",
            description=f"Kicked user **{member}** for **{reason}**",
        )

    @slash_command(name="timeout", description="Timeouts a user.")
    @application_checks.has_guild_permissions(manage_roles=True)
    async def timeout(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to timeout"
        ),
        time: int = SlashOption(
            name="time", description="The time you want to timeout the member for"
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
        reason: str = SlashOption(
            name="reason", description="The reason you want to timeout the member for"
        ),
    ):
        """Timeouts a user.

        Args:
          inter (Interaction): The interaction
          member (Member): The member you want to timeout. Defaults to SlashOption(name="member", description="The member you want to timeout").
          time (int): The time you want to timeout the member for. Defaults to SlashOption(name="time", description="The time you want to timeout the member for").
          modifier (str): The modifier for the time. Defaults to SlashOption(name="modifier", description="The modifier for the time", choices={"seconds": "s", "minutes": "m", "hours": "h", "days": "d", "weeks": "w"}).
          reason (str): The reason you want to timeout the member for. Defaults to SlashOption(name="reason", description="The reason you want to timeout the member for").
        """
        seconds = 0
        if modifier == "s":
            seconds = time
        elif modifier == "m":
            seconds = time * 60
        elif modifier == "h":
            seconds = time * 60 * 60
        elif modifier == "d":
            seconds = time * 60 * 60 * 24
        elif modifier == "w":
            seconds = time * 60 * 60 * 24 * 7
        await member.edit(
            timeout=utils.utcnow() + datetime.timedelta(seconds=seconds),
            reason=reason,
        )
        await self.bot.standard_response(
            inter,
            title="Member Timed Out",
            description=f"Timed out **{member}** for **{time}{modifier}** for **{reason}**",
        )
        await self.bot.log(
            title="Member Timed Out",
            description=f"Timed out **{member}** for **{time}{modifier}** for **{reason}**",
        )

    @slash_command(name="warn", description="Warns a user.")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def warn(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to warn"
        ),
        reason=SlashOption(
            name="reason", description="The reason you want to warn the member for"
        ),
    ):
        with open(f"{self.dir}/json/warns.json", "r") as f:
            warns = json.load(f)
        with open(f"{self.dir}/json/warns.json", "w") as f:
            if str(member.id) in warns:
                warns[str(member.id)]["warns"] += 1
                warns[str(member.id)]["reasons"].append(reason)
            else:
                warns[str(member.id)] = {}
                warns[str(member.id)]["warns"] = 1
                warns[str(member.id)]["reasons"] = [reason]
            json.dump(warns, f, indent=4)
        await self.bot.standard_response(
            inter,
            title="Member Warned",
            description=f"Warned **{member}** for **{reason}**",
        )
        await self.bot.log(
            title="Member Warned", description=f"Warned **{member}** for **{reason}**"
        )

    @slash_command(name="warnings", description="Displays a user's warnings.")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def warnings(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to check the warnings of"
        ),
    ):
        with open(f"{self.dir}/json/warns.json", "r") as f:
            warns = json.load(f)
        if str(member.id) in warns:
            embed = Embed(
                description=f"**{warns[str(member.id)]['warns']}** warnings",
                color=getattr(Color, self.bot.config.get("embed_color")),
            )
            for reason in warns[str(member.id)]["reasons"]:
                embed.add_field(name="Reason", value=reason, inline=False)
        else:
            await self.bot.standard_response(
                inter, title=f"Warnings for {member}", description="No warnings"
            )

    @slash_command(name="clearwarns", description="Clears a user's warnings.")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def clearwarns(self, inter: Interaction, member: Member):
        with open(f"{self.dir}/json/warns.json", "r") as f:
            warns = json.load(f)
        with open(f"{self.dir}/json/warns.json", "w") as f:
            if str(member.id) in warns:
                del warns[str(member.id)]
                json.dump(warns, f, indent=4)
        await self.bot.standard_response(
            inter,
            title="Warnings Cleared",
            description=f"Cleared warnings for **{member}**",
        )

    @slash_command(name="removewarn", description="Removes a warning from a user.")
    @application_checks.has_guild_permissions(manage_messages=True)
    async def removewarn(self, inter: Interaction, member: Member, number: int):
        with open(f"{self.dir}/json/warns.json", "r") as f:
            warns = json.load(f)
        with open(f"{self.dir}/json/warns.json", "w") as f:
            if str(member.id) in warns:
                warns[str(member.id)]["warns"] -= 1
                del warns[str(member.id)]["reasons"][number]
            json.dump(warns, f, indent=4)
        await self.bot.standard_response(
            inter,
            title="Warning Removed",
            description=f"Removed warning **{number}** from **{member}**",
        )


def setup(bot):
    bot.add_cog(Moderation(bot))
