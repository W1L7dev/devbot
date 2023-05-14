import json
import os

from nextcord import (Color, Embed, Interaction, Member, SlashOption,
                      slash_command)
from nextcord.ext import commands


class Levelling(commands.Cog):
    """Levelling commands

    Commands:
        rank: Shows a member's rank
        leaderboard: Shows the leaderboard
        reset: Resets your rank
    """
    
    def __init__(self, bot):
        self.dir = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """The event that triggers when a message is sent

        Args:
          message (str): The message that triggered the event
        """
        if message.author.bot:
            return
        with open(f"{self.dir}/json/levels.json", "r") as f:
            users = json.load(f)
        await self.bot.update_data(users, message.author)
        await self.bot.add_experience(users, message.author, 5)
        await self.bot.level_up(users, message.author, message)
        with open(f"{self.dir}/json/levels.json", "w") as f:
            json.dump(users, f)

    @slash_command(name="rank", description="Shows your rank")
    async def rank(
        self,
        inter: Interaction,
        member: Member = SlashOption(
            name="member", description="The member you want to see the rank of"
        ),
    ):
        """Shows a member's rank

        Args:
          inter (Interaction): The interaction
          member (Member): The member you want to see the rank of. Defaults to SlashOption(name="member", description="The member you want to see the rank of")
        """
        with open(f"{self.dir}/json/levels.json", "r") as f:
            users = json.load(f)
        await self.bot.update_data(users, member)
        user_id = str(member.id)
        username = member.name
        level = users[user_id]["level"]
        rank = 1
        for user in users:
            if users[user]["level"] > level:
                rank += 1
        embed = Embed(
            title=f"{username}'s Rank",
            description=f"{username} is level {level}",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        embed.add_field(name="Rank", value=rank)
        embed.set_thumbnail(url=member.avatar.url)
        await inter.response.send_message(embed=embed)

    @slash_command(name="leaderboard", description="Shows the leaderboard")
    async def leaderboard(self, inter: Interaction):
        """Shows the leaderboard

        Args:
          inter (Interaction): The interaction
        """
        with open(f"{self.dir}/json/levels.json", "r") as f:
            users = json.load(f)
        sorted_users = sorted(users.items(), key=lambda x: x[1]["level"], reverse=True)
        embed = Embed(
            title="Leaderboard",
            description="Our top users",
            color=getattr(Color, self.bot.config.get("default_embed_color"))(),
        )
        for index, (user_id, user_data) in enumerate(sorted_users):
            member = self.bot.get_user(int(user_id))
            name = member.name if member else f"Unknown User ({user_id})"
            level = user_data["level"]
            embed.add_field(
                name=f"{index+1}. {name}", value=f"Level: {level}", inline=False
            )
        await inter.response.send_message(embed=embed)

    @slash_command(name="reset", description="Resets your rank")
    async def reset(self, inter: Interaction):
        """Resets your rank

        Args:
          inter (Interaction): The interaction
        """
        with open(f"{self.dir}/json/levels.json", "r") as f:
            users = json.load(f)
        await self.bot.update_data(users, inter.user)
        user_id = str(inter.user.id)
        users[user_id]["level"] = 1
        users[user_id]["experience"] = 0
        with open(f"{self.dir}/json/levels.json", "w") as f:
            json.dump(users, f)
        await self.bot.standard_response(
            inter, title="Reset", description="Your rank has been reset"
        )


def setup(bot):
    bot.add_cog(Levelling(bot))
