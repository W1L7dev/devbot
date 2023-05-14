import time

import mafic
from nextcord import Activity, ActivityType
from nextcord.ext import commands


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """When the bot is ready, print a message and change the presence"""
        self.bot.logger.log("info", f"Logged in as {self.bot.user}")
        self.bot.uptime = time.time()
        await self.bot.change_presence(
            activity=Activity(type=ActivityType.watching, name="The Dev Community")
        )
        self.bot.loop.create_task(self.bot.add_nodes())

    @commands.Cog.listener()
    async def on_node_ready(self, node: mafic.Node):
        """When a mafic node is ready, print a message

        Args:
          node (mafic.Node): The node
        """
        self.bot.logger.log("info", f"Node {node.label} ready")


def setup(bot):
    bot.add_cog(OnReady(bot))
