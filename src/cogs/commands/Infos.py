from nextcord import (ChannelType, Color, Embed, Interaction, Member, Role,
                      SlashOption, slash_command)
from nextcord.abc import GuildChannel
from nextcord.ext import commands

from typing import Optional


class Infos(commands.Cog):
    """Information commands""

    Commands:
        rules:	Displays the server rules.
        userinfo: Displays information about a user.
        serverinfo: Displays information about the server.
        roleinfo: Displays information about a role.
        channelinfo: Displays information about a channel.
        github: Displays information about the bot's GitHub repository.
        website: Displays information about the bot's website.
    """
    OSError
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="rules", description="Displays the server rules.")
    async def rules(self, inter: Interaction):
        rules_embed = Embed(
            title="Rules",
            description="These are the rules of the server",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        for index, rule_title, rule_desc in enumerate(
            self.bot.config.get("rules").items()
        ):
            rules_embed.add_field(
                name=f"{index + 1}. {rule_title}",
                value=rule_desc,
                inline=False,
            )
        rules_embed.set_footer(
            text="These rules are subject to change\nLink to Discord TOS: https://discord.com/terms\nLink to Discord Community Guidelines: https://discord.com/guidelines"
        )
        """Displays the server rules.

    Args:
      inter (Interaction): The interaction
    """
        await inter.response.send_message(embed=rules_embed)

    @slash_command(name="userinfo", description="Displays information about a user.")
    async def userinfo(
        self,
        inter: Interaction,
        member: Optional[Member] = SlashOption(
            name="member",
            description="The member you want to get the info of",
            required=False,
        ),
    ):
        """Displays information about a user.

        Args:
          inter (Interaction): The interaction
          member (Member): The member you want to get the info of. Defaults to None.
        """
        if member is None:
            member = inter.user
        embed = Embed(
            title=f"{member}'s info",
            description=f"Here is the info of {member.name}",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.add_field(name="Name", value=member.name, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Status", value=member.status, inline=False)
        embed.add_field(name="Top Role", value=member.top_role, inline=False)
        embed.add_field(
            name="Joined At",
            value=f"<t:{int(member.joined_at.timestamp())}:d>",
            inline=False,
        )
        embed.add_field(
            name="Created At",
            value=f"<t:{int(member.created_at.timestamp())}:d>",
            inline=False,
        )
        embed.add_field(name="Bot?", value=member.bot, inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="serverinfo", description="Displays information about the server.")
    async def serverinfo(self, inter: Interaction):
        """Displays information about the server.

        Args:
          inter (Interaction): The interaction
        """
        embed = Embed(
            title=f"{inter.guild.name}'s info",
            description=f"Here is the info of {inter.guild.name}",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.add_field(name="Name", value=inter.guild.name, inline=False)
        embed.add_field(name="ID", value=inter.guild.id, inline=False)
        embed.add_field(name="Owner", value=inter.guild.owner, inline=False)
        embed.add_field(
            name="Created At",
            value=f"<t:{int(inter.guild.created_at.timestamp())}:d>",
            inline=False,
        )
        embed.add_field(name="Members", value=inter.guild.member_count, inline=False)
        embed.add_field(
            name="Text Channels", value=len(inter.guild.text_channels), inline=False
        )
        embed.add_field(
            name="Voice Channels", value=len(inter.guild.voice_channels), inline=False
        )
        embed.add_field(name="Roles", value=len(inter.guild.roles), inline=False)
        embed.add_field(
            name="Boosts", value=inter.guild.premium_subscription_count, inline=False
        )
        embed.set_thumbnail(url=inter.guild.icon.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="roleinfo", description="	Displays information about a role.")
    async def roleinfo(
        self,
        inter: Interaction,
        role: Role = SlashOption(
            name="role", description="The role you want to get the info of"
        ),
    ):
        """	Displays information about a role.

        Args:
          inter (Interaction): The interaction
          role (Role): The role you want to get the info of. Defaults to None.
        """
        embed = Embed(
            title=f"{role.name}'s info",
            description=f"Here is the info of {role.name}",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.add_field(name="Name", value=role.name, inline=False)
        embed.add_field(name="ID", value=role.id, inline=False)
        embed.add_field(name="Color", value=role.color, inline=False)
        embed.add_field(name="Position", value=role.position, inline=False)
        embed.add_field(
            name="Created At",
            value=f"<t:{int(role.created_at.timestamp())}:d>",
            inline=False,
        )
        embed.add_field(name="Mentionable", value=role.mentionable, inline=False)
        embed.add_field(name="Hoisted", value=role.hoist, inline=False)
        embed.add_field(name="Managed", value=role.managed, inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.set_thumbnail(url=role.guild.icon.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="channelinfo", description="Displays information about a channel.")
    async def channelinfo(
        self,
        inter: Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="The channel you want to get the info of",
            channel_types=[
                ChannelType.text,
                ChannelType.voice,
                ChannelType.forum,
                ChannelType.news,
                ChannelType.stage_voice,
            ],
        ),
    ):
        """Displays information about a channel.

        Args:
          inter (Interaction): The interaction
          channel (GuildChannel): The channel you want to get the info of. Defaults SlashOption(name="channel", description="The channel you want to get the info of", channel_types=[ChannelType.text, ChannelType.voice, ChannelType.forum, ChannelType.news, ChannelType.stage_voice])
        """
        embed = Embed(
            title=f"{channel.name}'s info",
            description=f"Here is the info of {channel.name}",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.add_field(name="Name", value=channel.name, inline=False)
        embed.add_field(name="ID", value=channel.id, inline=False)
        embed.add_field(name="Category", value=channel.category, inline=False)
        embed.add_field(
            name="Created At",
            value=f"<t:{int(channel.created_at.timestamp())}:d>",
            inline=False,
        )
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=False)
        embed.set_thumbnail(url=channel.guild.icon.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="github", description="Displays information about the bot's GitHub repository.")
    async def github(self, inter: Interaction):
        """Displays information about the bot's GitHub repository.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter, title="Github", description="https://github.com/W1L7dev/Devbot"
        )

    @slash_command(name="website", description="Displays information about the bot's website.")
    async def website(self, inter: Interaction):
        """Displays information about the bot's website.

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter, title="Website", description="https://w1l7dev.github.io/devbot/"
        )


def setup(bot):
    bot.add_cog(Infos(bot))
