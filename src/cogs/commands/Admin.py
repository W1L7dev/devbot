from nextcord import (CategoryChannel, ChannelType, Color, Interaction, Member,
                      Role, SlashOption, TextChannel, VoiceChannel,
                      slash_command)
from nextcord.abc import GuildChannel
from nextcord.ext import application_checks, commands


class Admin(commands.Cog):
    """Admin Commands

    Commands:
        role:
            add: Add a role to a user
            remove: Remove a role from a user
            create: Create a role
            delete: Delete a role
        category:
            create: Creates a new category with the specified name.
            delete: Deletes the specified category.
            move: Moves a channel to a specified category
        channel:
            create: Create a channel
            delete: Delete a channel
        voice:
            create: Create a voice channel
            delete: Delete a voice channel
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="role", description="Role commands")
    @application_checks.has_permissions(manage_roles=True)
    async def role(self, inter: Interaction):
        pass

    @role.subcommand(name="rename", description="Rename a role")
    @application_checks.has_permissions(manage_roles=True)
    async def renamerole(
        self,
        inter: Interaction,
        role: Role = SlashOption(name="role", description="The role to rename"),
        name: str = SlashOption(name="name", description="The new name of the role"),
    ):
        """Rename a role

        Args:
          inter (Interaction): The interaction
          role (Role): The role to rename. Defaults to SlashOption(name="role", description="The role to rename").
          name (str): The new name of the role. Defaults to SlashOption(name="name", description="The new name of the role").
        """
        await role.edit(name=name)
        await self.bot.standard_response(
            inter,
            title="Role Renamed",
            description=f"Renamed **{role.mention}** to **{name}**",
        )
        await self.bot.log(
            title="Role Renamed",
            description=f"{inter.user.mention} renamed **{role.mention}** to **{name}**",
        )

    @role.subcommand(name="add", description="Add a role to a user")
    @application_checks.has_permissions(manage_roles=True)
    async def addrole(
        self,
        inter: Interaction,
        role: Role = SlashOption(name="role", description="the role to assign"),
        member: Member = SlashOption(
            name="member", description="the member to assign a role"
        ),
    ):
        """Add a role to a user

        Args:
          inter (Interaction): The interaction
          role (Role): The role to add. Defaults to SlashOption(name="role", description="the role to assign").
          member (Member): The member to add the role. Defaults to SlashOption(name="member", description="the member to assign a role").
        """
        await member.add_roles(role)
        await self.bot.standard_response(
            inter,
            title="Role Added",
            description=f"Added **{role.mention}** to **{member.mention}**",
        )
        await self.bot.log(
            title="Role Added",
            description=f"{inter.user.mention} added **{role.mention}** to **{member.mention}**",
        )

    @role.subcommand(name="remove", description="Remove a role from a user")
    @application_checks.has_permissions(manage_roles=True)
    async def removerole(
        self,
        inter: Interaction,
        role: Role = SlashOption(name="role", description="the role to remove"),
        member: Member = SlashOption(
            name="member", description="the member to remove a role"
        ),
    ):
        """Remove a role from a user

        Args:
          inter (Interaction): The interaction
          role (Role): The role to remove. Defaults to SlashOption(name="role", description="the role to remove").
          member (Member): The member to remove the role. Defaults to SlashOption(name="member", description="the member to remove a role").
        """
        await member.remove_roles(role)
        await self.bot.standard_response(
            inter,
            title="Role Removed",
            description=f"Removed **{role.mention}** from **{member.mention}**",
        )
        await self.bot.log(
            title="Role Removed",
            description=f"{inter.user.mention} removed **{role.mention}** from **{member.mention}**",
        )

    @role.subcommand(name="create", description="Create a role")
    @application_checks.has_permissions(manage_roles=True)
    async def createrole(
        self,
        inter: Interaction,
        name: str = SlashOption(name="name", description="The name of the role"),
        color: str = SlashOption(
            name="color",
            description="The color of the role",
            choices=[
                "red",
                "orange",
                "yellow",
                "green",
                "blue",
                "purple",
                "pink",
                "white",
                "black",
                "brown",
                "teal",
                "blurple",
                "greyple",
            ],
        ),
    ):
        """Create a role

        Args:
          inter (Interaction): The interaction
          name (str): The role's name. Defaults to SlashOption(name="name", description="The name of the role").
          color (str): The role's color. Defaults to SlashOption( name="color", description="The color of the role", choices=[ "red", "orange", "yellow", "green", "blue", "purple", "pink", "white", "black", "brown", "teal", "blurple", "greyple" ] ).
        """
        await inter.guild.create_role(name=name, color=getattr(Color, color)())
        await self.bot.standard_response(
            inter,
            title="Role Created",
            description=f"Created **{name}**",
        )
        await self.bot.log(
            title="Role Created",
            description=f"{inter.user.mention} created **{name}**",
        )

    @role.subcommand(name="delete", description="Delete a role")
    @application_checks.has_permissions(manage_roles=True)
    async def delrole(
        self,
        inter: Interaction,
        role: Role = SlashOption(name="role", description="The role to delete"),
    ):
        """Delete a role

        Args:
          inter (Interaction): The interaction
          role (Role): The role to delete. Defaults to SlashOption(name="role", description="The role to delete").
        """
        await role.delete()
        await self.bot.standard_response(
            inter,
            title="Role Deleted",
            description=f"Deleted **{role.mention}**",
        )
        await self.bot.log(
            title="Role Deleted",
            description=f"{inter.user.mention} deleted **{role.name}**",
        )

    @slash_command(name="category", description="Category Commands")
    @application_checks.has_permissions(manage_channels=True)
    async def category(self, inter: Interaction):
        pass

    @category.subcommand(name="create", description="Creates a new category with the specified name.")
    @application_checks.has_permissions(manage_channels=True)
    async def createcategory(
        self,
        inter: Interaction,
        name: str = SlashOption(name="name", description="The name of the category"),
    ):
        """Creates a new category with the specified name.

        Args:
          inter (Interaction): The interaction
          name (str): The category's name. Defaults to SlashOption(name="name", description="The name of the category").
        """
        await inter.guild.create_category(name=name)
        await self.bot.standard_response(
            inter,
            title="Category Created",
            description=f"Created **{name}**",
        )
        await self.bot.log(
            title="Category Created",
            description=f"{inter.user.mention} created **{name}**",
        )

    @category.subcommand(name="delete", description="Deletes the specified category.")
    @application_checks.has_permissions(manage_channels=True)
    async def delcategory(
        self,
        inter: Interaction,
        category: CategoryChannel = SlashOption(
            name="category", description="The category to delete"
        ),
    ):
        """Deletes the specified category.

        Args:
          inter (Interaction): The interaction
          category (CategoryChannel): The category to delete. Defaults to SlashOption(name="category", description="The category to delete").
        """
        await category.delete()
        await self.bot.standard_response(
            inter,
            title="Category Deleted",
            description=f"Deleted **{category.name}**",
        )
        await self.bot.log(
            title="Category Deleted",
            description=f"{inter.user.mention} deleted **{category.name}**",
        )

    @category.subcommand(name="move", description="Moves a channel to a specified category")
    @application_checks.has_permissions(manage_channels=True)
    async def categorymove(
        self,
        inter: Interaction,
        category: CategoryChannel = SlashOption(
            name="category", description="The category to add the channel to"
        ),
        channel: GuildChannel = SlashOption(
            name="channel",
            description="The channel to add to the category",
            channel_types=[
                ChannelType.text,
                ChannelType.voice,
                ChannelType.stage_voice,
                ChannelType.news,
                ChannelType.forum,
            ],
        ),
    ):
        """Moves a channel to a specified category

        Args:
          inter (Interaction): The interaction
          category (CategoryChannel): The category to add the channel to. Defaults to SlashOption(name="category", description="The category to add the channel to").
          channel (GuildChannel): The channel to add to the category. Defaults to SlashOption( name="channel", description="The channel to add to the category", channel_types=[ ChannelType.text, ChannelType.voice, ChannelType.stage_voice, ChannelType.news, ChannelType.forum, ] ).
        """
        await channel.edit(category=category)
        await self.bot.standard_response(
            inter,
            title="Channel Moved",
            description=f"Moved **{channel.mention}** to **{category.name}**",
        )
        await self.bot.log(
            title="Channel Moved",
            description=f"{inter.user.mention} moved **{channel.mention}** to **{category.name}**",
        )

    @slash_command(name="channel", description="Channel Commands")
    @application_checks.has_permissions(manage_channels=True)
    async def channel(self, inter: Interaction):
        pass

    @channel.subcommand(name="create", description="Create a channel")
    @application_checks.has_permissions(manage_channels=True)
    async def createchannel(
        self,
        inter: Interaction,
        name: str = SlashOption(name="name", description="The name of the channel"),
        category: CategoryChannel = SlashOption(
            name="category", description="The category to add the channel to"
        ),
    ):
        """Create a channel

        Args:
          inter (Interaction): The interaction
          name (str): The channel's name. Defaults to SlashOption(name="name", description="The name of the channel").
          category (CategoryChannel): The category to add the channel to. Defaults to SlashOption(name="category", description="The category to add the channel to").
        """
        await inter.guild.create_text_channel(name=name, category=category)
        await self.bot.standard_response(
            inter,
            title="Channel Created",
            description=f"Created **{name}**",
        )
        await self.bot.log(
            title="Channel Created",
            description=f"{inter.user.mention} created **{name}**",
        )

    @channel.subcommand(name="delete", description="Delete a channel")
    @application_checks.has_permissions(manage_channels=True)
    async def delchannel(
        self,
        inter: Interaction,
        channel: TextChannel = SlashOption(
            name="channel", description="The channel to delete"
        ),
    ):
        """Delete a channel

        Args:
          inter (Interaction): The interaction
          channel (TextChannel): The channel to delete. Defaults to SlashOption(name="channel", description="The channel to delete").
        """
        await channel.delete()
        await self.bot.standard_response(
            inter,
            title="Channel Deleted",
            description=f"Deleted **{channel.mention}**",
        )
        await self.bot.log(
            title="Channel Deleted",
            description=f"{inter.user.mention} deleted **{channel.mention}**",
        )

    @slash_command(name="voice", description="Voice Channel Commands")
    @application_checks.has_permissions(manage_channels=True)
    async def voice(self, inter: Interaction):
        pass

    @voice.subcommand(name="create", description="Create a voice channel")
    @application_checks.has_permissions(manage_channels=True)
    async def createvoice(
        self,
        inter: Interaction,
        name: str = SlashOption(name="name", description="The name of the channel"),
        category: CategoryChannel = SlashOption(
            name="category", description="The category to add the channel to"
        ),
    ):
        """Create a voice channel

        Args:
          inter (Interaction): The interaction
          name (str): The channel's name. Defaults to SlashOption(name="name", description="The name of the channel").
          category (CategoryChannel): The category to add the channel to. Defaults to SlashOption(name="category", description="The category to add the channel to").
        """
        await inter.guild.create_voice_channel(name=name, category=category)
        await self.bot.standard_response(
            inter,
            title="Voice Channel Created",
            description=f"Created **{name}**",
        )
        await self.bot.log(
            title="Voice Channel Created",
            description=f"{inter.user.mention} created **{name}**",
        )

    @voice.subcommand(name="delete", description="Delete a voice channel")
    @application_checks.has_permissions(manage_channels=True)
    async def delvoice(
        self,
        inter: Interaction = SlashOption(
            name="channel", description="The channel to delete"
        ),
        channel: VoiceChannel = SlashOption(
            name="channel", description="The channel to delete"
        ),
    ):
        """Delete a voice channel

        Args:
          inter (Interaction): The interaction
          channel (VoiceChannel): The channel to delete. Defaults to SlashOption(name="channel", description="The channel to delete").
        """
        await channel.delete()
        await self.bot.standard_response(
            inter,
            title="Voice Channel Deleted",
            description=f"Deleted **{channel.name}**",
        )
        await self.bot.log(
            title="Voice Channel Deleted",
            description=f"{inter.user.mention} deleted **{channel.name}**",
        )


def setup(bot):
    bot.add_cog(Admin(bot))
