import random

from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext import commands

from tasks.morse_code import encrypt
from tasks.zalgo import zalgo


class Fun(commands.Cog):
    """Fun commands

    Commands:
        8ball: Ask the magic 8ball a question
        coinflip: Flip a coin
        dice: Roll a dice
        rps: Play rock paper scissors
        choose: Choose between multiple options
        russianroulette: Play russian roulette
        slots: Play slots
        ruin: Ruin text
        reverse: Reverse text
        morse: Morse code text
    """

    def __init__(self, bot):
        self.bot = bot
        self.responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
            "No.",
        ]
        self.rps_choices = ["rock", "paper", "scissors"]
        self.slots_choices = ["🍎", "🍊", "🍇", "🍒", "🍋", "🍉", "🍌", "🍍", "🍑"]

    @slash_command(name="8ball", description="Ask the magic 8ball a question")
    async def _8ball(
        self,
        inter: Interaction,
        question: str = SlashOption(name="question", description="Your question"),
    ):
        """Ask the magic 8ball a question

        Args:
          inter (Interaction): The interaction
          question (str): The question to ask. Defaults to SlashOption(name="question", description="Your question").
        """
        await self.bot.standard_response(
            inter,
            title="Magic 8ball",
            description=f"Question: {question} \nAnswer: {random.choice(self.responses)}",
        )

    @slash_command(name="coinflip", description="Flip a coin")
    async def coinflip(self, inter: Interaction):
        """Flip a coin

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Coinflip",
            description=f"Result: {random.choice(['Heads', 'Tails'])}",
        )

    @slash_command(name="dice", description="Roll a dice")
    async def dice(self, inter: Interaction):
        """Roll a dice

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter, title="Dice", description=f"Result: {random.randint(1, 6)}"
        )

    @slash_command(name="rps", description="Play rock paper scissors")
    async def rps(
        self,
        inter: Interaction,
        choice: str = SlashOption(
            name="choice",
            description="Your choice",
            choices=["rock", "paper", "scissors"],
        ),
    ):
        """Play rock paper scissors

        Args:
          inter (Interaction): The interaction
          choice (str): Your choice. Defaults to SlashOption(name="choice", description="Your choice", choices=["rock", "paper", "scissors"]).
        """
        bot_choice = random.choice(self.rps_choices)
        if choice == bot_choice:
            result = "Tie"
        elif choice == "rock" and bot_choice == "scissors":
            result = "You win"
        elif choice == "rock" and bot_choice == "paper":
            result = "I win"
        elif choice == "paper" and bot_choice == "rock":
            result = "You win"
        elif choice == "paper" and bot_choice == "scissors":
            result = "I win"
        elif choice == "scissors" and bot_choice == "paper":
            result = "You win"
        elif choice == "scissors" and bot_choice == "rock":
            result = "I win"
        await self.bot.standard_response(
            inter,
            title="Rock Paper Scissors",
            description=f"You chose {choice} \nI chose {bot_choice} \nResult: {result}",
        )

    @slash_command(name="choose", description="Choose between multiple options")
    async def choose(self, inter: Interaction, choices: str):
        """Choose between multiple options

        Args:
          inter (Interaction): The interaction
          choices (str): The choices
        """
        await self.bot.standard_response(
            inter,
            title="Choose",
            description=f"Result: {random.choice(choices.split(','))}",
        )

    @slash_command(name="russianroulette", description="Play russian roulette")
    async def russianroulette(self, inter: Interaction):
        """Play russian roulette

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Russian Roulette",
            description=f"Result: You {random.choice(['died', 'lived'])}",
        )

    @slash_command(name="slots", description="Play slots")
    async def slots(self, inter: Interaction):
        """Play slots

        Args:
          inter (Interaction): The interaction
        """
        await self.bot.standard_response(
            inter,
            title="Slots",
            description="".join(random.choices(self.slots_choices, k=3)),
        )

    @slash_command(name="ruin", description="Ruin text")
    async def ruin(
        self,
        inter: Interaction,
        text: str = SlashOption(name="text", description="Text to ruin"),
    ):
        """Ruin text

        Args:
          inter (Interaction): The interaction
          text (str): The text to ruin. Defaults to SlashOption(name="text", description="Text to ruin").
        """
        await self.bot.standard_response(
            inter,
            title="Ruin",
            description=f"Result: {zalgo(text)}",
        )

    @slash_command(name="reverse", description="Reverse text")
    async def reverse(
        self,
        inter: Interaction,
        text: str = SlashOption(name="text", description="Text to reverse"),
    ):
        """Reverse text

        Args:
          inter (Interaction): The interaction
          text (str): The text to reverse. Defaults to SlashOption(name="text", description="Text to reverse").
        """
        await self.bot.standard_response(
            inter,
            title="Reverse",
            description=f"Result: {text[::-1]}",
        )

    @slash_command(name="morse", description="Morse code text")
    async def morse(
        self,
        inter: Interaction,
        text: str = SlashOption(name="text", description="Text to morse code"),
    ):
        """Morse code text

        Args:
          inter (Interaction): The interaction
          text (str): The text to morse code. Defaults to SlashOption(name="text", description="Text to morse code").
        """
        await self.bot.standard_response(
            inter,
            title="Morse",
            description=f"Result: {encrypt(text)}",
        )


def setup(bot):
    bot.add_cog(Fun(bot))
