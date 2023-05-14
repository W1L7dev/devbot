from typing import Optional, Union

import mafic
from nextcord import Color, Embed, Guild, Interaction, Member, Message, User
from nextcord.abc import GuildChannel
from nextcord.ext import commands

from config import Config
from env import Environment


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config: Config
        self.env: Environment
        self.logger: ...
        self.pool = mafic.NodePool(self)

    async def getch_guild(self, guild_id: int) -> Union[Guild, bool]:
        """Looks up a guild in cache or fetches if not found.

        Args:
          guild_id (int): the id of the guild

        Returns:
          Union[Guild, bool]: the guild or False if not found
        """
        guild: Union[Guild, None] = self.get_guild(guild_id)
        if guild:
            return guild
        try:
            guild: Union[Guild, None] = await self.fetch_guild(guild_id)
        except:
            return False
        return guild

    async def getch_user(self, user_id: int) -> Union[User, bool]:
        """Looks up a user in cache or fetches if not found.

        Args:
          user_id (int): the id of the user

        Returns:
          Union[User, bool]: the user or False if not found
        """
        user: Union[User, None] = self.get_user(user_id)
        if user:
            return user
        try:
            user: Union[User, None] = await self.fetch_user(user_id)
        except:
            return False
        return user

    async def getch_member(self, guild_id: int, member_id: int) -> Union[Member, bool]:
        """Looks up a member in cache or fetches if not found.

        Args:
          guild_id (int): the id of the guild
          member_id (int): the id of the member

        Returns:
          Union[Member, bool]: the member or False if not found
        """
        guild: Union[Member, None] = await self.getch_guild(guild_id)
        if not guild:
            return False
        member: Union[Member, None] = guild.get_member(member_id)
        if member is not None:
            return member
        try:
            member: Union[Member, None] = await guild.fetch_member(member_id)
        except:
            return False
        return member

    async def getch_channel(self, channel_id: int) -> Union[GuildChannel, bool]:
        """Looks up a channel in cache or fetches if not found.

        Args:
          channel_id (int): the id of the channel

        Returns:
          Union[GuildChannel, bool]: the channel or False if not found
        """
        channel: Union[GuildChannel, None] = self.get_channel(channel_id)
        if channel:
            return channel
        try:
            channel: Union[GuildChannel, None] = await self.fetch_channel(channel_id)
        except:
            return False
        return channel

    async def log(self, title: str, description: str):
        """Sends a message in the logs

        Args:
          title (str): the title of the embed
          description (str): the description of the embed
        """
        log_channel = await self.getch_channel(self.config.get("log_channel"))
        if not log_channel:
            return
        await log_channel.send(
            embed=Embed(
                title=title,
                description=description,
                color=getattr(Color, self.config.get("default_embed_color"))(),
            )
        )

    async def standard_response(
        self,
        inter: Interaction,
        title: str,
        description: str,
        ephemeral: Optional[bool] = None,
    ):
        """Sends the standard response
        Args:
          inter (Interaction): the interaction
          title (str): title of the embed
          description (str): description of the embed
          ephemeral (Optional[bool], optional): whether the message should be ephemeral. Defaults to None.
        """
        await inter.response.send_message(
            embed=Embed(
                title=title,
                description=description,
                color=getattr(Color, self.config.get("default_embed_color"))(),
            ),
            ephemeral=ephemeral if ephemeral is not None else False,
        )

    async def add_nodes(self):
        await self.pool.create_node(
            host=self.config.get("node_host"),
            port=self.config.get("node_port"),
            label=self.config.get("node_label"),
            password=self.config.get("node_password"),
        )

    async def update_data(self, users: dict, user: User):
        """Updates the data of a user

        Args:
          users (dict): The users dict
          user (User): The user to update the data of
        """
        if not str(user.id) in users:
            users[str(user.id)] = {}
            users[str(user.id)]["experience"] = 0
            users[str(user.id)]["level"] = 1

    async def add_experience(self, users: dict, user: User, exp: int):
        """Adds experience to a user

        Args:
          users (dict): The users dict
          user (User): The user to add the experience to
          exp (int): The amount of experience to add
        """
        users[str(user.id)]["experience"] += exp

    async def level_up(self, users: dict, user: User, message: Message):
        """Levels up a user

        Args:
          users (dict): The users dict
          user (User): The user to level up
          message (Message): The message that triggered the level up
        """
        experience = users[str(user.id)]["experience"]
        lvl_start = users[str(user.id)]["level"]
        lvl_end = int(experience ** (1 / 4))
        if lvl_start < lvl_end:
            await message.channel.send(
                f"{user.mention} has leveled up to level {lvl_end}"
            )
            users[str(user.id)]["level"] = lvl_end
