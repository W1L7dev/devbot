import logmaster
import mafic
from nextcord import Color, Embed, Interaction, Message, User, TextChannel
from nextcord.ext import commands

from config import Config


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config: Config
        self.pool = mafic.NodePool(self)
        self.logger: logmaster.Logger

    async def log(self, title: str, description: str):
        """Sends a message in the logs

        Args:
          title (str): the title of the embed
          description (str): the description of the embed
        """
        channel = self.get_channel(self.config.get("log_channel"))
        if isinstance(channel, TextChannel):
            log_channel = channel
        else:
            log_channel = None
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
        description: str
    ):
        """Sends the standard response
        Args:
          inter (Interaction): the interaction
          title (str): title of the embed
          description (str): description of the embed
        """
        await inter.response.send_message(
            embed=Embed(
                title=title,
                description=description,
                color=getattr(Color, self.config.get("default_embed_color"))(),
            )
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
