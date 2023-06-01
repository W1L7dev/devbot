<p align="center">
  <picture>
    <img src="./assets/banner.png" alt="devbot" width="450">

  </picture>
</p>

<div align="center">

![Version](https://img.shields.io/badge/Version-v4.1-green)
![License](https://img.shields.io/badge/License-MIT-red)
![Python](https://img.shields.io/badge/Python-3.11.2-orange)
![GitHub last commit](https://img.shields.io/github/last-commit/W1L7dev/Devbot?color=blueviolet)

</div>

---

DevBot is a personal Discord bot designed to manage my Discord server, but it can be used for any server. It has a variety of features, including moderation, fun, and utility commands. It also has a leveling system, which allows users to gain experience and level up. The bot is written in Python using the nextcord library. It is currently in development, and new features are being added regularly. If you have any suggestions, feel free to open an issue or pull request.

### NEW WEBSITE: [https://w1l7dev.github.io/devbot/](https://w1l7dev.github.io/Devbot/)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation \& Running](#installation--running)
- [Features \& Commands](#features--commands)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation & Running

To install and use the bot, you'll need the following tools:

- [Python 3.11 or newer](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Java 16 or newer](https://www.java.com/en/download/)
- [PIP](https://pip.pypa.io/en/stable/installation/)

You'll also need to install [Lavalink](https://github.com/freyacodes/Lavalink), but it is included in the repository.

First, You'll need to create a Discord Application. First, head to the [Discord Developer Portal](https://discord.com/developers/applications), and create a new application.

<p align="center">
  <picture>
    <img src="./assets/app.gif" alt="devbot" width="450">
  </picture>
</p>

After, you'll need to create a Genius API account. To do this, head to the [Genius API website](https://genius.com/api-clients) and create a new application.

<p align="center">
  <picture>
    <img src="./assets/genius.gif" alt="devbot" width="450">
  </picture>
</p>

Then, you may install the repository. To do this, open a terminal and run the following commands:

```bash
git clone https://github.com/W1L7dev/Devbot.git
```

Once the repository is cloned, you'll need to install the dependencies. To do this, run one of the following commands:

```bash
pip install -r requirements.txt
```

> **Note**
> Use `python -m`, `pip3` or similar if that is how you install your pakages
> Generally, Windows uses `py -m` and UNIX machines `python3 -m`

Then, you can open a text editor such as Visual Studio Code, Visual Studio, Sublime Text or Jetbrains IDEs, and open the file in the src\ directory called `.env`, inside of it, you'll need to paste your bot's token and your genius api key.

```env
TOKEN=your_bot_token
GENIUS=your_genius_api_key
```

When you'll need to run the bot, make sure to run Lavalink first. To do this, open a terminal and run the following commands:

```bash
cd plugins/Lavalink
java -jar Lavalink.jar
```

Before running the bot, Make sure to check if all python files have the correct path.

Then, you can run the bot. To do this, open src/main.py and run it.
Alternatively, you can run the bot from the terminal. To do this, open a terminal and run one of the following commands:

```bash
cd src
py main.py
```

> **Note**
> You can use `python`, `py3` or similar commands instead of `py` if it doesn't work

---

## Features & Commands

DevBot has a variety of features, including moderation, fun, and utility commands. It also has a leveling system, which allows users to gain experience and level up. The bot is written in Python using the nextcord library. It is currently in development, and new features are being added regularly. If you have any suggestions, feel free to open an issue or pull request.

| Command Name      | Description                                     | Usage                                                             | Category       |
| ----------------- | ----------------------------------------------- | ----------------------------------------------------------------- | -------------- |
| `category create` | Creates a new category with the specified name. | `/category create <name>`                                         | Administration |
| `category delete` | Deletes the specified category.                 | `/category delete <name>`                                         | Administration |
| `category move`   | Moves a channel to a specified category         | `/category move <channel>`                                        | Administration |
| `channel create`  | Creates a new channel with the specified name.  | `/channel create <name>`                                          | Administration |
| `channel delete`  | Deletes the specified channel.                  | `/channel delete <name>`                                          | Administration |
| `role add`        | Adds a role to the specified user.              | `/role add <user> <role>`                                         | Administration |
| `role create`     | Creates a new role with the specified name.     | `/role create <name>`                                             | Administration |
| `role delete`     | Deletes the specified role.                     | `/role delete <name>`                                             | Administration |
| `role remove`     | Removes a role from the specified user.         | `/role remove <user> <role>`                                      | Administration |
| `role rename`     | Renames the specified role.                     | `/role rename <name>`                                             | Administration |
| `uptime`          | Displays the bot's uptime.                      | `/uptime`                                                         | Development    |
| `cls`             | Clears the terminal output.                     | `/cls`                                                            | Development    |
| `print`           | Prints a message to the terminal.               | `/print <message>`                                                | Development    |
| `restart`         | Restarts the bot.                               | `/restart`                                                        | Development    |
| `shutdown`        | Shuts down the bot.                             | `/shutdown`                                                       | Development    |
| `cog load`        | Loads a cog.                                    | `/cog load <cog>`                                                 | Development    |
| `cog unload`      | Unloads a cog.                                  | `/cog unload <cog>`                                               | Development    |
| `cog reload`      | Reloads a cog.                                  | `/cog reload <cog>`                                               | Development    |
| `cog create`      | Creates a cog.                                  | `/cog create <name> <type>`                                       | Development    |
| `activity`        | Sets the bot's activity.                        | `/activity <name>`                                                | Development    |
| `status`          | Sets the bot's status.                          | `/status <online,idle,dnd,invisible>`                             | Development    |
| `file read`       | Reads a file.                                   | `/file read <path>`                                               | Development    |
| `file create`     | Creates a file.                                 | `/file create <path>`                                             | Development    |
| `file write`      | Writes to a file.                               | `/file write <path> <message>`                                    | Development    |
| `file delete`     | Deletes a file.                                 | `/file delete <path>`                                             | Development    |
| `folder create`   | Creates a folder.                               | `/folder create <path>`                                           | Development    |
| `folder delete`   | Deletes a folder.                               | `/folder delete <path>`                                           | Development    |
| `folder list`     | Lists the contents of a folder.                 | `/folder list <path>`                                             | Development    |
| `eval`            | Evaluates Python code.                          | `/eval <expression>`                                              | Development    |
| `log`             | Logs a message to the terminal.                 | `/log <debug,info,warning,error,critical,success,fail> <message>` | Development    |
| `request`         | Sends an http request to a website.             | `/request <url>`                                                  | Development    |
| `jsondiagram`     | Generates a diagram from a json file/string.    | `/jsondiagram <json>`                                             | Development    |
| `8ball`           | Asks the magic 8ball a question.                | `/8ball <question>`                                               | Fun            |
| `coinflip`        | Flips a coin.                                   | `/coinflip`                                                       | Fun            |
| `dice`            | Rolls a dice.                                   | `/dice`                                                           | Fun            |
| `rps`             | Plays rock, paper, scissors.                    | `/rps <rock,paper,scissors>`                                      | Fun            |
| `choose`          | Chooses between multiple options.               | `/choose <option1,option2...>`                                    | Fun            |
| `slots`           | Plays the slots.                                | `/slots`                                                          | Fun            |
| `russianroulette` | Plays russian roulette.                         | `/russianroulette`                                                | Fun            |
| `ruin`            | Ruins text.                                     | `/ruin <text>`                                                    | Fun            |
| `morse`           | Converts text to morse code.                    | `/morse <text>`                                                   | Fun            |
| `reverse`         | Reverses text.                                  | `/reverse <text>`                                                 | Fun            |
| `rules`           | Displays the server rules.                      | `/rules`                                                          | Informations   |
| `userinfo`        | Displays information about a user.              | `/userinfo <user>`                                                | Informations   |
| `serverinfo`      | Displays information about the server.          | `/serverinfo`                                                     | Informations   |
| `roleinfo`        | Displays information about a role.              | `/roleinfo <role>`                                                | Informations   |
| `channelinfo`     | Displays information about a channel.           | `/channelinfo <channel>`                                          | Informations   |
| `github`          | Displays information about the bot's GitHub repository. | `/github <user/repository>`                                       | Informations   |
| `website`         | Displays information about the bot's website.           | `/website <url>`                                                  | Informations   |
| `rank`            | Displays your rank.                             | `/rank <member>`                                                  | Levelling      |
| `leaderboard`     | Displays the server leaderboard.                | `/leaderboard`                                                    | Levelling      |
| `reset`           | Resets your rank.                               | `/reset`                                                          | Levelling      |
| `raidmode`        | Toggles raidmode.                               | `/raidmode <True,False>`                                          | Moderation     |
| `lock`            | Locks a channel.                                | `/lock <channel>`                                                 | Moderation     |
| `unlock`          | Unlocks a channel.                              | `/unlock <channel>`                                               | Moderation     |
| `slowmode`        | Sets the slowmode of a channel.                 | `/slowmode <channel> <time>`                                      | Moderation     |
| `ban`             | Bans a user.                                    | `/ban <user> <reason>`                                            | Moderation     |
| `unban`           | Unbans a user.                                  | `/unban <user>`                                                   | Moderation     |
| `kick`            | Kicks a user.                                   | `/kick <user> <reason>`                                           | Moderation     |
| `clear`           | Clears messages.                                | `/clear <amount>`                                                 | Moderation     |
| `timeout`         | Timeouts a user.                                | `/timeout <user> <time> <reason>`                                 | Moderation     |
| `warn`            | Warns a user.                                   | `/warn <user> <reason>`                                           | Moderation     |
| `warnings`        | Displays a user's warnings.                     | `/warnings <user>`                                                | Moderation     |
| `clearwarns`      | Clears a user's warnings.                       | `/clearwarns <user>`                                              | Moderation     |
| `removewarn`      | Removes a warning from a user.                  | `/removewarn <user> <id>`                                         | Moderation     |
| `play`            | Plays a song.                                   | `/play <song>`                                                    | Music          |
| `pause`           | Pauses the music.                               | `/pause`                                                          | Music          |
| `resume`          | Resumes the music.                              | `/resume`                                                         | Music          |
| `volume`          | Changes the volume.                             | `/volume <volume>`                                                | Music          |
| `nowplaying`      | Displays the current song.                      | `/nowplaying`                                                     | Music          |
| `stop`            | Stops the music.                                | `/stop`                                                           | Music          |
| `connect`         | Joins a voice channel.                          | `/connect`                                                        | Music          |
| `disconnect`      | Disconnects from a voice channel.               | `/disconnect`                                                     | Music          |
| `lyrics`          | Displays the lyrics of a song.                  | `/lyrics <song>`                                                  | Music          |
| `poll`            | Creates a poll.                                 | `/poll <question> <choice1,choice2...>`                           | Utils          |
| `pollresults`     | Displays the results of a poll.                 | `/pollresults <message id>`                                       | Utils          |
| `ping`            | Displays the bot's ping.                        | `/ping`                                                           | Utils          |
| `say`             | Makes the bot say something.                    | `/say <message>`                                                  | Utils          |
| `embed`           | Makes the bot send an embed.                    | `/embed <title> <description>`                                    | Utils          |
| `nick`            | Changes your nickname.                          | `/nick <nickname>`                                                | Utils          |
| `resetnick`       | Resets your nickname.                           | `/resetnick`                                                      | Utils          |
| `avatar`          | Displays a user's avatar.                       | `/avatar <user>`                                                  | Utils          |
| `giveaway`        | Creates a giveaway.                             | `/giveaway <time> <winners> <prize>`                              | Utils          |
| `ticket`          | Creates a ticket message.                       | `/ticket <message id>`                                            | Utils          |
| `math`            | Evaluates a mathematical expression.            | `/math <expression>`                                              | Utils          |
| `img`             | Generates an image with AI.                     | `/img <prompt></prompt>`                                          | Utils          |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. More informations in [CONTRIBUTING.md](CONTRIBUTING.md)

Code of Conduct in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
Contributors in [CONTRIBUTORS.md](CONTRIBUTORS.md)

---

## Contact

Discord: W1L7#9944

Email: w1l7dev@gmail.com

Website: https://w1l7dev.github.io/W1L7/

⬇️⬇️ **[DevLabs](https://discord.gg/aGbpGEDqnT)** ⬇️⬇️

![Discord](https://img.shields.io/discord/1021582244407685200?color=7289DA&label=Discord&logo=Discord&logoColor=white&style=for-the-badge)
