import json
import os


class Config:
    def __init__(self) -> None:
        self.load()

    def load(self):
        """Loads the config file into memory."""
        path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        with open(f"{path}/config.cfg", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get(self, key):
        """Gets a value from the config file.

        Args:
          key (str): the key to get the value of

        Returns:
          str: the value of the key
        """
        self.load()
        return self.config.get(key)
