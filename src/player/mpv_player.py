import json
import os
import sys
from os import path

# -------------------------------------------------
# Windows-only PATH fix BEFORE importing MPV
# -------------------------------------------------
if sys.platform.startswith("win"):
    os.environ["PATH"] = (
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
        + os.pathsep
        + os.environ.get("PATH", "")
    )


from mpv import MPV

from ..model import Anime
from ..utils import REDIRECT_PORT


class MpvPlayer:
    def __init__(self, state_file: str = "config/state.json"):
        self.player = MPV(
            ytdl=True,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            config=False,
            scripts=path.abspath("scripts"),
        )

        self.state_file = state_file

        self.__load_state()

        @self.player.event_callback("shutdown")
        def on_shutdown(event):
            self.__save_state()

    def __save_state(self) -> bool:
        try:
            with open(self.state_file, "w") as f:
                json.dump(
                    {
                        "volume": self.player.volume,
                        "speed": self.player.speed,
                        "maximize": self.player.window_maximized,
                    },
                    f,
                )
            return True
        except Exception as e:
            return False

    def __load_state(self) -> bool:
        if not path.exists(self.state_file):
            return False

        try:
            with open(self.state_file, "r") as f:
                state = json.load(f)

            if "volume" in state:
                self.player.volume = state["volume"]
            if "speed" in state:
                self.player.speed = state["speed"]
            if "maximize" in state:
                self.player.window_maximized = state["maximize"]

            return True
        except Exception as e:
            return False

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

        for ep in anime.episodes:
            self.player.command(
                "loadfile", f"http://localhost:{REDIRECT_PORT}/{ep.id}", "append"
            )

        self.player.playlist_play_index(episode - start)

    def close(self):
        self.player.quit()
