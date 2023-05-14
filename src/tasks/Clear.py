import os


def cls():
    """Clears the console"""
    if os.name != "nt":
        os.system("clear")  # For UNIX systems (Linux, MacOS)
    else:
        os.system("cls")  # For Windows systems
