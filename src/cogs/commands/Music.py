import datetime

import lyricsgenius
import mafic
from nextcord import (ChannelType, Color, Embed, Interaction, SlashOption,
                      slash_command)
from nextcord.abc import GuildChannel
from nextcord.ext import commands


class Music(commands.Cog):
    """Music commands

    Commands:
        lyrics: Displays the lyrics of a song.
        music:
            play: Plays a song.
            pause: Pauses the music.
            resume: Resumes the music.
            stop: 	Stops the music.
            nowplaying: Displays the current song.
            volume: Changes the volume.
            connect: Joins a voice channel.
            disconnect: Disconnects from a voice channel.
    """

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="lyrics", description="Displays the lyrics of a song.")
    async def lyrics(
        self,
        inter: Interaction,
        search: str = SlashOption(
            name="search", description="The song you want to get the lyrics of"
        ),
    ):
        """Displays the lyrics of a song.

        Args:
          inter (Interaction): The interaction.
          search (str, optional): The song you want to get the lyrics of. Defaults to SlashOption(name="search", description="The song you want to get the lyrics of").
        """
        genius = lyricsgenius.Genius(self.bot.config.get("genius"))
        try:
            async with inter.channel.typing():
                song = genius.search_song(search)
                await self.bot.standard_response(
                    inter=inter,
                    title="Lyrics",
                    description=f"**{song.title}** by **{song.artist}**\n\n{song.lyrics}",
                )
        except Exception as e:
            await self.bot.standard_response(
                inter=inter,
                title="Error",
                description=f"An error occured: {e}",
                ephemeral=True,
            )

    @slash_command(name="music", description="Music commands")
    async def music(self, inter: Interaction):
        pass

    @music.subcommand(
        name="play",
        description="Plays a song.",
    )
    async def play(
        self,
        inter: Interaction,
        search: str = SlashOption(
            name="search", description="The song you want to play"
        ),
    ):
        """Plays a song..

        Args:
          inter (Interaction): The interaction.
          search (str, optional): The song you want to play. Defaults to SlashOption(name="search", description="The song you want to play").
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client

        tracks = await player.fetch_tracks(search)
        if not tracks:
            return await self.bot.standard_response(
                inter=inter, title="Error", description="No tracks found"
            )
        track = tracks[0]
        await player.play(track)
        await inter.response.send_message(
            embed=Embed(
                title="Playing",
                description=f"**{track.title}** by **{track.author}**",
                color=getattr(Color, self.bot.config.get("default_embed_color"))(),
            )
        )

    @music.subcommand(
        name="pause",
        description="Pauses the music.",
    )
    async def pause(self, inter: Interaction):
        """Pauses the music.

        Args:
          inter (Interaction): The interaction.
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client

        await player.pause()
        await self.bot.standard_response(
            inter=inter,
            title="Paused",
            description="Paused the current song",
        )

    @music.subcommand(
        name="resume",
        description="Resumes the music.",
    )
    async def resume(self, inter: Interaction):
        """Resumes the music.

        Args:
          inter (Interaction): The interaction.
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client

        await player.resume()
        await self.bot.standard_response(
            inter=inter,
            title="Resumed",
            description="Resumed the current song",
        )

    @music.subcommand(
        name="stop",
        description="	Stops the music.",
    )
    async def stop(self, inter: Interaction):
        """	Stops the music.

        Args:
          inter (Interaction): The interaction.
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client
        await player.stop()
        await self.bot.standard_response(
            inter=inter,
            title="Stopped",
            description="Stopped the current song",
        )

    @music.subcommand(
        name="nowplaying",
        description="Displays the current song.",
    )
    async def nowplaying(self, inter: Interaction):
        """Displays the current song.

        Args:
          inter (Interaction): The interaction.
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client

        if not player.current:
            return await self.bot.standard_response(
                inter=inter,
                title="Error",
                description="No song is currently playing",
            )

        await self.bot.standard_response(
            inter=inter,
            title="Now Playing",
            description=f"**{player.current.title}** by **{player.current.author}**",
        )

    @music.subcommand(
        name="volume",
        description="Changes the volume.",
    )
    async def volume(
        self,
        inter: Interaction,
        volume: int = SlashOption(
            name="volume", description="The volume you want to set"
        ),
    ):
        """Changes the volume.

        Args:
          inter (Interaction): The interaction.
          volume (int, optional): The volume you want to set. Defaults to SlashOption(name="volume", description="The volume you want to set").
        """
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=mafic.Player)
        else:
            player = inter.guild.voice_client

        await player.set_volume(volume)
        await self.bot.standard_response(
            inter=inter,
            title="Volume",
            description=f"Set the volume to {volume}",
        )

    @music.subcommand(
        name="connect",
        description="Joins a voice channel.",
    )
    async def connect(
        self,
        inter: Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="The channel you want to connect to",
            required=False,
            channel_types=[ChannelType.voice],
        ),
    ):
        """Joins a voice channel.

        Args:
          inter (Interaction): The interaction.
          channel (str, optional): The channel you want to connect to. Defaults to SlashOption(name="channel", description="The channel you want to connect to", required=False, channel_types=[ChannelType.GUILD_VOICE]).
        """
        if not channel:
            channel = inter.user.voice.channel
            if inter.user not in channel.members:
                return await self.bot.standard_response(
                    inter=inter,
                    title="Error",
                    description="You are not in a voice channel",
                )
        await channel.connect(cls=mafic.Player)
        await self.bot.standard_response(
            inter=inter,
            title="Connected",
            description=f"Connected to {channel}",
        )

    @music.subcommand(
        name="disconnect",
        description="Disconnects from a voice channel.",
    )
    async def disconnect(self, inter: Interaction):
        """Disconnects from a voice channel..

        Args:
          inter (Interaction): The interaction.
        """
        if not inter.guild.voice_client:
            return await self.bot.standard_response(
                inter=inter,
                title="Error",
                description="I am not in a voice channel",
            )
        await inter.guild.voice_client.disconnect()
        await self.bot.standard_response(
            inter=inter,
            title="Disconnected",
            description="Disconnected from the voice channel",
        )


def setup(bot):
    bot.add_cog(Music(bot))
