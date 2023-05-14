import math

from nextcord import Interaction, SlashOption, slash_command
from nextcord.ext import commands


class Math(commands.Cog):
    """Math commands

    Commands:
        math: Do math
        functions: Math functions
    """
    
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="math", description="Do math")
    async def math(
        self,
        inter: Interaction,
        num1: int = SlashOption(name="num1", description="The first number"),
        num2: int = SlashOption(name="num2", description="The second number"),
        op: str = SlashOption(
            name="operation",
            choices={
                "addition": "+",
                "subtraction": "-",
                "multiplication": "*",
                "division": "/",
                "exponentiation": "^",
                "modulus": "%",
                "floor division": "~",
                "greatest common divisor": ">",
                "least common multiple": "<",
            },
        ),
    ):
        """Do math

        Args:
          inter (Interaction): The interaction
          num1 (int): The first number. Defaults to SlashOption(name="num1", description="The first number")
          num2 (int): The second number. Defaults to SlashOption(name="num2", description="The second number")
          op (str): The operation. Defaults to SlashOption(name="operation", choices={"addition": "+", "subtraction": "-", "multiplication": "*", "division": "/", "exponentiation": "^", "modulus": "%", "floor division": "~", "greatest common divisor": ">", "least common multiple": "<"})
        """
        if op == "+":
            result = f"num1 + num2 = {num1 + num2}"
        elif op == "-":
            result = f"num1 - num2 = {num1 - num2}"
        elif op == "*":
            result = f"num1 * num2 = {num1 * num2}"
        elif op == "/":
            result = f"num1 / num2 = {num1 / num2}"
        elif op == "^":
            result = f"num1 ^ num2 = {num1 ** num2}"
        elif op == "%":
            result = f"num1 % num2 = {num1 % num2}"
        elif op == "~":
            result = f"num1 // num2 = {num1 // num2}"
        elif op == ">":
            result = f"gcd({num1}, {num2}) = {math.gcd(num1, num2)}"
        elif op == "<":
            result = f"lcm({num1}, {num2}) = {math.lcm(num1, num2)}"
        await self.bot.standard_response(inter, title="Math", description=result)

    @slash_command(name="functions", description="Math functions")
    async def functions(
        self,
        inter: Interaction,
        func: str = SlashOption(
            name="function",
            choices={
                "square root": "sqrt",
                "cube root": "cbrt",
                "log": "log",
                "sine": "sin",
                "cosine": "cos",
                "tangent": "tan",
                "pi": "pi",
                "e": "e",
            },
        ),
        num: int = SlashOption(
            name="num", description="The first number", required=False
        ),
    ):
        """Math Functions

        Args:
          inter (Interaction): The interaction
          func (str): The function. Defaults to SlashOption(name="function", choices={ "square root": "sqrt", "cube root": "cbrt", "log": "log", "sine": "sin", "cosine": "cos", "tangent": "tan", "pi": "pi", "e": "e" }, ).
          num (int, optional): A number. Defaults to SlashOption(name="num", description="The first number", required=False).
        """
        if func == "sqrt":
            result = f"sqrt({num}) = {math.sqrt(num)}"
        elif func == "cbrt":
            result = f"cbrt({num}) = {math.cbrt(num)}"
        elif func == "log":
            result = f"log({num}) = {math.log(num)}"
        elif func == "sin":
            result = f"sin({num}) = {math.sin(num)}"
        elif func == "cos":
            result = f"cos({num}) = {math.cos(num)}"
        elif func == "tan":
            result = f"tan({num}) = {math.tan(num)}"
        elif func == "pi":
            result = f"pi = {math.pi}"
        elif func == "e":
            result = f"e = {math.e}"
        if func == "pi" and num is not None or func == "e" and num is not None:
            return await self.bot.standard_response(
                inter,
                title="You can't use a number with this function!",
                description="** **",
            )
        if (
            func == "sqrt"
            and num is None
            or func == "cbrt"
            and num is None
            or func == "log"
            and num is None
            or func == "sin"
            and num is None
            or func == "cos"
            and num is None
            or func == "tan"
            and num is None
        ):
            return await self.bot.standard_response(
                inter,
                title="You need to use a number with this function!",
                description="** **",
            )
        await self.bot.standard_response(inter, title="Math", description=result)


def setup(bot):
    bot.add_cog(Math(bot))
