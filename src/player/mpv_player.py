import json
import os
import sys
from os import path

from .redirector import RedirectServer

if sys.platform.startswith("win"):
    os.environ["PATH"] = (
        os.path.abspath(path.join(path.dirname(path.abspath(__file__)), "..", ".."))
        + os.pathsep
        + os.environ.get("PATH", "")
    )


from mpv import MPV

from ..model import Anime
from ..utils import REDIRECT_PORT


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


        @self.player.event_callback("shutdown")
        def on_shutdown(event):
            self.close()
        
        @self.player.event_callback('start-file')
        def on_start_file(event):
            pos = self.player.playlist_pos

            if not self.anime_name or not isinstance(pos, int):
                return

            current_track = pos + self.start
            self.player['force-media-title'] = f"{self.anime_name} - Episodio {current_track}"


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
        self.anime_name = anime.title
        self.player.playlist_play_index(episode - start)
    

    def close(self):
        RedirectServer.stop()
        self.player.quit()
