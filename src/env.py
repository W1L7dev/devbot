import os

from dotenv import load_dotenv


class Environment:
    def __init__(self):
        load_dotenv()

        self.token = os.getenv("TOKEN")
        self.genius = os.getenv("GENIUS")
