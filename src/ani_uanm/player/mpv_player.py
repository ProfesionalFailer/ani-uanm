import json
import os
import sys
import time
from os import path

from pypresence import ActivityType, Presence

from .redirector import RedirectServer

if sys.platform.startswith("win"):
    os.environ["PATH"] = (
        path.abspath(path.join(path.dirname(path.abspath(__file__)), "..", "..", ".."))
        + os.pathsep
        + os.environ.get("PATH", "")
    )


from mpv import MPV

from ..model import Anime
from ..utils import DISCORD_RPC, REDIRECT_PORT, singleton
from ..utils.consts import CLIENT_ID


@singleton
class MpvPlayer:
    def __init__(self):
        self.player = MPV(
            ytdl=True,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            user_agent="Mozilla/5.0"
        )

        self.anime_name: str | None = None
        self.start: int = 1

        RedirectServer.start()

        self.discord = Presence(CLIENT_ID) if DISCORD_RPC else None

        @self.player.event_callback("shutdown")
        def on_shutdown(event):
            self.close()
        
        @self.player.event_callback('start-file')
        def on_start_file(event):
            pos = self.player.playlist_pos

            if not isinstance(self.anime, Anime) or not isinstance(pos, int):
                return

            current_track = pos + self.start
            self.player['force-media-title'] = f"{self.anime.title} - Episodio {current_track}"
            if self.discord is not None:
                self.discord.update(
                    activity_type=ActivityType.WATCHING,
                    details=self.anime.title,
                    large_image=self.anime.image_url, 
                    state=f"({current_track} / {len(self.player.playlist)})"
                )


    def load_playlist(self, anime: Anime, episode: int) -> None:
        if not anime or not anime.episodes:
            print(anime)
            raise Exception("Impossibile caricare la playlist")

        if anime.start_from_zero:
            start, end = 0, anime.n_ep - 1
        else:
            start, end = 1, anime.n_ep

        if episode < start or episode > end:
            raise Exception("Numero dell'episodio non valido")

        self.player.playlist_clear()
        for ep in anime.episodes:
            self.player.command(
                "loadfile", f"http://localhost:{REDIRECT_PORT}/{ep.id}", "append"
            )

        self.start = start
        self.anime = anime

        if self.discord is not None:
            self.discord.connect()

        time.sleep(0.05) # Sleep to allow playlist to load before playing
        self.player.playlist_play_index(episode - start)
    

    def close(self):
        RedirectServer.stop()
        self.player.quit()
