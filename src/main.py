"""
Devbot Discord Bot
~~~~~~~~~~~~~~~~~~

A general purpose bot for discord made with nextcord.

:copyright: (c) 2022-present W1L7dev
:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

__title__ = "Devbot"
__author__ = "W1L7dev"
__license__ = "MIT"
__version__ = "3.7.0"
__copyright__ = "2022-present W1L7dev"

import os

import logmaster
import nextcord

from bot_base import Bot
from config import Config

intents = nextcord.Intents.all()
config = Config()

bot = Bot(intents=intents, default_guild_ids=config.get("guild_id"))
bot.remove_command("help")
logger = logmaster.Logger()

logger.log("info", "Starting bot...")
for file in os.listdir("src/cogs"):
    if file.endswith(".py"):
        logger.log("info", f"Loading {file}...")
        bot.load_extension(f"cogs.{file[:-3]}")
    elif os.path.isdir(f"src/cogs/{file}"):
        for subfile in os.listdir(f"src/cogs/{file}"):
            if subfile.endswith(".py"):
                logger.log("info", f"Loading {file}.{subfile}...")
                bot.load_extension(f"cogs.{file}.{subfile[:-3]}")
logger.log("info", "Cogs Loaded!")

if __name__ == "__main__":
    bot.logger = logger
    bot.config = config
    bot.run(bot.config.get("token"))
