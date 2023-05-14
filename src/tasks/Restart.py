import os
import sys


def restart():
    """Restarts the current script"""
    if os.name == "nt":
        os.system("cls")
    os.execv(sys.executable, ["python"] + sys.argv)
